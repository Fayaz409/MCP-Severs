#!/usr/bin/env python3
"""
MITM + Frida Integration Test for Android Data Scraping
Demonstrates combining network interception with runtime manipulation
Target: dawn.com (news website)
"""

import json
import sqlite3
import threading
import time
from datetime import datetime
from typing import Dict, Any

import requests
from mitmproxy import http
from mitmproxy.tools.dump import DumpMaster
from mitmproxy.options import Options
import frida
import sys


class DataCollector:
    """Handles data collection and storage from both MITM and Frida"""
    
    def __init__(self, db_path: str = "mitm_frida_data.db"):
        self.db_path = db_path
        self.init_database()
        
    def init_database(self):
        """Initialize SQLite database for storing captured data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Network traffic table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS network_traffic (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                method TEXT,
                url TEXT,
                status_code INTEGER,
                request_headers TEXT,
                response_headers TEXT,
                request_body TEXT,
                response_body TEXT,
                source TEXT DEFAULT 'mitm'
            )
        ''')
        
        # Frida hooks data table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS frida_hooks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                hook_type TEXT,
                function_name TEXT,
                parameters TEXT,
                return_value TEXT,
                additional_data TEXT
            )
        ''')
        
        # Scraped news articles table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scraped_articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                title TEXT,
                url TEXT,
                content TEXT,
                metadata TEXT,
                extraction_method TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        
    def log_network_traffic(self, method: str, url: str, status_code: int = None, 
                          request_headers: Dict = None, response_headers: Dict = None,
                          request_body: str = None, response_body: str = None):
        """Log network traffic to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO network_traffic 
            (timestamp, method, url, status_code, request_headers, response_headers, request_body, response_body)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            datetime.now().isoformat(),
            method,
            url,
            status_code,
            json.dumps(request_headers) if request_headers else None,
            json.dumps(response_headers) if response_headers else None,
            request_body,
            response_body
        ))
        
        conn.commit()
        conn.close()
        
    def log_frida_hook(self, hook_type: str, function_name: str, parameters: Dict = None,
                      return_value: Any = None, additional_data: Dict = None):
        """Log Frida hook data to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO frida_hooks 
            (timestamp, hook_type, function_name, parameters, return_value, additional_data)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            datetime.now().isoformat(),
            hook_type,
            function_name,
            json.dumps(parameters) if parameters else None,
            str(return_value) if return_value else None,
            json.dumps(additional_data) if additional_data else None
        ))
        
        conn.commit()
        conn.close()


class MitmAddon:
    """MITM proxy addon for intercepting dawn.com traffic"""
    
    def __init__(self, collector: DataCollector):
        self.collector = collector
        self.target_domains = ['dawn.com', 'www.dawn.com']
        
    def request(self, flow: http.HTTPFlow) -> None:
        """Intercept and log requests"""
        if any(domain in flow.request.pretty_host for domain in self.target_domains):
            print(f"[MITM] Intercepted request: {flow.request.method} {flow.request.pretty_url}")
            
            # Log request
            self.collector.log_network_traffic(
                method=flow.request.method,
                url=flow.request.pretty_url,
                request_headers=dict(flow.request.headers),
                request_body=flow.request.text if flow.request.text else None
            )
            
            # Add custom headers to identify our traffic
            flow.request.headers["X-MITM-Agent"] = "MCP-Learn-Agent"
            
    def response(self, flow: http.HTTPFlow) -> None:
        """Intercept and log responses"""
        if any(domain in flow.request.pretty_host for domain in self.target_domains):
            print(f"[MITM] Intercepted response: {flow.response.status_code} for {flow.request.pretty_url}")
            
            # Log response
            self.collector.log_network_traffic(
                method=flow.request.method,
                url=flow.request.pretty_url,
                status_code=flow.response.status_code,
                request_headers=dict(flow.request.headers),
                response_headers=dict(flow.response.headers),
                request_body=flow.request.text if flow.request.text else None,
                response_body=flow.response.text if flow.response.text else None
            )
            
            # Extract news articles from HTML responses
            if 'text/html' in flow.response.headers.get('content-type', ''):
                self.extract_articles_from_html(flow.response.text, flow.request.pretty_url)
                
    def extract_articles_from_html(self, html_content: str, url: str):
        """Simple HTML parsing to extract article titles and content"""
        # This is a basic implementation - in production you'd use BeautifulSoup
        if not html_content:
            return
            
        # Look for common patterns in dawn.com HTML structure
        import re
        
        # Extract article titles
        title_patterns = [
            r'<title>(.*?)</title>',
            r'<h1[^>]*>(.*?)</h1>',
            r'<h2[^>]*>(.*?)</h2>'
        ]
        
        for pattern in title_patterns:
            titles = re.findall(pattern, html_content, re.IGNORECASE | re.DOTALL)
            for title in titles:
                # Clean HTML tags
                clean_title = re.sub(r'<[^>]+>', '', title).strip()
                if clean_title and len(clean_title) > 10:
                    conn = sqlite3.connect(self.collector.db_path)
                    cursor = conn.cursor()
                    
                    cursor.execute('''
                        INSERT INTO scraped_articles 
                        (timestamp, title, url, extraction_method)
                        VALUES (?, ?, ?, ?)
                    ''', (
                        datetime.now().isoformat(),
                        clean_title[:500],  # Limit title length
                        url,
                        'mitm_html_parsing'
                    ))
                    
                    conn.commit()
                    conn.close()
                    break  # Only take the first good title


class FridaHooker:
    """Frida integration for Android runtime manipulation"""
    
    def __init__(self, collector: DataCollector):
        self.collector = collector
        self.session = None
        self.script = None
        
    def get_frida_script(self) -> str:
        """JavaScript code for Frida hooks"""
        return '''
        console.log("[FRIDA] Script loaded successfully");
        
        // Hook Android WebView
        if (Java.available) {
            Java.perform(function() {
                console.log("[FRIDA] Java runtime available, setting up hooks...");
                
                // Hook WebView loadUrl
                try {
                    var WebView = Java.use("android.webkit.WebView");
                    WebView.loadUrl.overload("java.lang.String").implementation = function(url) {
                        console.log("[FRIDA] WebView.loadUrl called with URL: " + url);
                        
                        // Send data back to Python
                        send({
                            type: "webview_load",
                            url: url,
                            timestamp: new Date().toISOString()
                        });
                        
                        // Call original method
                        return this.loadUrl(url);
                    };
                    
                    console.log("[FRIDA] WebView.loadUrl hooked successfully");
                } catch (e) {
                    console.log("[FRIDA] Could not hook WebView: " + e.message);
                }
                
                // Hook OkHttp (popular HTTP client)
                try {
                    var Request = Java.use("okhttp3.Request");
                    var RequestBuilder = Java.use("okhttp3.Request$Builder");
                    
                    RequestBuilder.build.implementation = function() {
                        var request = this.build();
                        var url = request.url().toString();
                        
                        if (url.includes("dawn.com")) {
                            console.log("[FRIDA] OkHttp request to dawn.com: " + url);
                            
                            send({
                                type: "okhttp_request",
                                url: url,
                                method: request.method(),
                                headers: request.headers().toString(),
                                timestamp: new Date().toISOString()
                            });
                        }
                        
                        return request;
                    };
                    
                    console.log("[FRIDA] OkHttp hooked successfully");
                } catch (e) {
                    console.log("[FRIDA] Could not hook OkHttp: " + e.message);
                }
                
                // Hook SSL Context (for bypassing SSL pinning)
                try {
                    var SSLContext = Java.use("javax.net.ssl.SSLContext");
                    var TrustManager = Java.use("javax.net.ssl.X509TrustManager");
                    var TrustManagerImpl = Java.use("com.android.org.conscrypt.TrustManagerImpl");
                    
                    // Create a custom trust manager that accepts all certificates
                    var CustomTrustManager = Java.registerClass({
                        name: "com.example.CustomTrustManager",
                        implements: [TrustManager],
                        methods: {
                            checkClientTrusted: function(chain, authType) {
                                console.log("[FRIDA] SSL: checkClientTrusted called - bypassed");
                            },
                            checkServerTrusted: function(chain, authType) {
                                console.log("[FRIDA] SSL: checkServerTrusted called - bypassed");
                            },
                            getAcceptedIssuers: function() {
                                return [];
                            }
                        }
                    });
                    
                    console.log("[FRIDA] SSL pinning bypass prepared");
                } catch (e) {
                    console.log("[FRIDA] SSL pinning bypass setup failed: " + e.message);
                }
            });
        } else {
            console.log("[FRIDA] Java runtime not available");
        }
        
        // Hook native HTTP libraries (for apps using native code)
        try {
            var connectPtr = Module.findExportByName("libc.so", "connect");
            if (connectPtr) {
                Interceptor.attach(connectPtr, {
                    onEnter: function(args) {
                        // This is a low-level hook - would need more work to extract meaningful data
                        console.log("[FRIDA] Native connect() called");
                    }
                });
                console.log("[FRIDA] Native connect() hooked");
            }
        } catch (e) {
            console.log("[FRIDA] Could not hook native functions: " + e.message);
        }
        '''
        
    def on_message(self, message, data):
        """Handle messages from Frida script"""
        if message['type'] == 'send':
            payload = message['payload']
            print(f"[FRIDA] Received: {payload['type']} - {payload}")
            
            # Log to database
            self.collector.log_frida_hook(
                hook_type=payload['type'],
                function_name=payload.get('method', 'unknown'),
                parameters={'url': payload.get('url', '')},
                additional_data=payload
            )
        elif message['type'] == 'error':
            print(f"[FRIDA] Error: {message['stack']}")
            
    def attach_to_process(self, process_name: str = None):
        """Attach Frida to Android process"""
        try:
            device = frida.get_usb_device(timeout=10)
            print(f"[FRIDA] Connected to device: {device}")
            
            if process_name:
                # Attach to specific process
                session = device.attach(process_name)
                print(f"[FRIDA] Attached to process: {process_name}")
            else:
                # Try to attach to common browser processes
                processes = ['com.android.chrome', 'org.mozilla.firefox', 'com.opera.browser']
                session = None
                
                for proc in processes:
                    try:
                        session = device.attach(proc)
                        print(f"[FRIDA] Attached to browser process: {proc}")
                        break
                    except frida.ProcessNotFoundError:
                        continue
                        
                if not session:
                    print("[FRIDA] No browser processes found, trying to spawn Chrome")
                    pid = device.spawn(["com.android.chrome"])
                    session = device.attach(pid)
                    device.resume(pid)
                    print(f"[FRIDA] Spawned and attached to Chrome")
            
            self.session = session
            script = session.create_script(self.get_frida_script())
            script.on('message', self.on_message)
            script.load()
            self.script = script
            
            print("[FRIDA] Script loaded and hooks active!")
            return True
            
        except Exception as e:
            print(f"[FRIDA] Failed to attach: {e}")
            return False


class MitmFridaAgent:
    """Main class orchestrating MITM + Frida integration"""
    
    def __init__(self):
        self.collector = DataCollector()
        self.mitm_addon = MitmAddon(self.collector)
        self.frida_hooker = FridaHooker(self.collector)
        self.mitm_thread = None
        
    def start_mitm_proxy(self, port: int = 8080):
        """Start MITM proxy in a separate thread"""
        def run_mitm():
            opts = Options(listen_port=port, confdir="~/.mitmproxy")
            master = DumpMaster(opts)
            master.addons.add(self.mitm_addon)
            
            try:
                print(f"[MITM] Starting proxy on port {port}")
                master.run()
            except KeyboardInterrupt:
                master.shutdown()
                
        self.mitm_thread = threading.Thread(target=run_mitm, daemon=True)
        self.mitm_thread.start()
        
        # Give proxy time to start
        time.sleep(2)
        print(f"[MITM] Proxy running on http://localhost:{port}")
        
    def start_frida_hooks(self, process_name: str = None):
        """Start Frida hooks"""
        success = self.frida_hooker.attach_to_process(process_name)
        if success:
            print("[FRIDA] Hooks are active and monitoring!")
        return success
        
    def test_dawn_com_access(self):
        """Test accessing dawn.com through our proxy"""
        print("\n[TEST] Testing direct access to dawn.com...")
        
        # Configure requests to use our proxy
        proxies = {
            'http': 'http://localhost:8080',
            'https': 'http://localhost:8080'
        }
        
        try:
            # Test HTTP request
            response = requests.get('https://www.dawn.com', 
                                  proxies=proxies, 
                                  verify=False,  # Ignore SSL for testing
                                  timeout=10,
                                  headers={'User-Agent': 'MCP-Learn-Agent/1.0'})
            
            print(f"[TEST] Response code: {response.status_code}")
            print(f"[TEST] Response size: {len(response.text)} bytes")
            
            # Extract some basic info
            if 'dawn' in response.text.lower():
                print("[TEST]  Successfully accessed dawn.com content")
            else:
                print("[TEST] � Unexpected content received")
                
        except Exception as e:
            print(f"[TEST] Failed to access dawn.com: {e}")
            
    def show_statistics(self):
        """Show collected data statistics"""
        conn = sqlite3.connect(self.collector.db_path)
        cursor = conn.cursor()
        
        # Network traffic stats
        cursor.execute("SELECT COUNT(*) FROM network_traffic")
        traffic_count = cursor.fetchone()[0]
        
        # Frida hooks stats  
        cursor.execute("SELECT COUNT(*) FROM frida_hooks")
        hooks_count = cursor.fetchone()[0]
        
        # Scraped articles stats
        cursor.execute("SELECT COUNT(*) FROM scraped_articles")
        articles_count = cursor.fetchone()[0]
        
        print(f"\n=== STATISTICS ===")
        print(f"Network requests captured: {traffic_count}")
        print(f"Frida hooks triggered: {hooks_count}")
        print(f"Articles extracted: {articles_count}")
        
        # Show recent articles
        cursor.execute("SELECT title, url FROM scraped_articles ORDER BY timestamp DESC LIMIT 3")
        recent_articles = cursor.fetchall()
        
        if recent_articles:
            print(f"\nRecent articles:")
            for title, url in recent_articles:
                print(f"  • {title[:80]}{'...' if len(title) > 80 else ''}")
                
        conn.close()
        
    def run_demo(self):
        """Run the complete demo"""
        print("🚀 Starting MITM + Frida Integration Demo")
        print("Target: dawn.com news website")
        print("=" * 50)
        
        # Start MITM proxy
        print("\n1. Starting MITM Proxy...")
        self.start_mitm_proxy()
        
        # Start Frida (optional - requires Android device)
        print("\n2. Starting Frida hooks...")
        frida_success = self.start_frida_hooks()
        
        if not frida_success:
            print("   � Frida failed to attach (normal if no Android device connected)")
            print("   =� To test Frida: Connect Android device and configure proxy to localhost:8080")
        
        # Test dawn.com access
        print("\n3. Testing dawn.com access through proxy...")
        self.test_dawn_com_access()
        
        print("\n4. Demo is running! Try these:")
        print("   • Configure Android device proxy to localhost:8080")
        print("   • Browse to dawn.com on the device")
        print("   • Watch the real-time logs above")
        print("   • Press Ctrl+C to stop and see statistics")
        
        try:
            # Keep running and show periodic stats
            while True:
                time.sleep(10)
                print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Agent is monitoring...")
                self.show_statistics()
                
        except KeyboardInterrupt:
            print("\n\n🛑 Stopping demo...")
            self.show_statistics()
            print("\n Demo completed! Check mitm_frida_data.db for all captured data.")


def main():
    """Main entry point"""
    agent = MitmFridaAgent()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "stats":
            agent.show_statistics()
            return
        elif command == "proxy-only":
            print("Starting MITM proxy only...")
            agent.start_mitm_proxy()
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("Stopping proxy...")
            return
    
    # Run full demo
    agent.run_demo()


if __name__ == "__main__":
    main()