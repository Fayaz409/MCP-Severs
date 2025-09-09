# MITM + Frida Integration Test

This test demonstrates the powerful combination of MITM proxy and Frida for Android data scraping and analysis.

## What This Demonstrates

**MITM Proxy** intercepts network traffic between your Android device and dawn.com:
- Captures all HTTP/HTTPS requests and responses
- Modifies headers and payloads in real-time
- Extracts article titles and content from HTML
- Logs everything to SQLite database

**Frida** hooks into Android app runtime:
- Monitors WebView URL loading
- Intercepts OkHttp network requests
- Bypasses SSL certificate pinning
- Extracts data directly from app memory

**Combined Power**:
- Complete visibility into both network and application layer
- Ability to modify requests and app behavior simultaneously
- Perfect for building intelligent scraping agents

## Setup

1. **Install Dependencies**:
   ```bash
   cd /Users/fayazali/Desktop/MCP_Learn
   uv sync
   ```

2. **Android Device Setup** (for Frida):
   - Enable USB debugging
   - Install Frida server on device
   - Connect via USB
   - Configure device proxy to point to your computer's IP:8080

## Usage

### Full Demo (MITM + Frida):
```bash
python MITM_FRIDA/test.py
```

### MITM Proxy Only:
```bash
python MITM_FRIDA/test.py proxy-only
```

### View Statistics:
```bash
python MITM_FRIDA/test.py stats
```

## How It Works

1. **MITM Proxy** starts on port 8080
2. **Frida** attempts to attach to browser processes on connected Android device
3. **Test request** is made to dawn.com to demonstrate traffic capture
4. Real-time monitoring begins - all dawn.com traffic is logged

## Testing Without Android Device

The demo works without an Android device! It will:
- Start the MITM proxy
- Show Frida connection attempts (which will fail gracefully)
- Make a test HTTP request to dawn.com through the proxy
- Demonstrate traffic interception and article extraction

## What You'll See

```
🚀 Starting MITM + Frida Integration Demo
Target: dawn.com news website
==================================================

1. Starting MITM Proxy...
[MITM] Proxy running on http://localhost:8080

2. Starting Frida hooks...
[FRIDA] Failed to attach: no USB device found
   ⚠ Frida failed to attach (normal if no Android device connected)

3. Testing dawn.com access through proxy...
[MITM] Intercepted request: GET https://www.dawn.com
[MITM] Intercepted response: 200 for https://www.dawn.com
[TEST] ✓ Successfully accessed dawn.com content

=== STATISTICS ===
Network requests captured: 15
Frida hooks triggered: 0
Articles extracted: 3

Recent articles:
  • Dawn.com | Latest Pakistan News, World News, Business, Sport and Multimedia
```

## Database Schema

Data is stored in `mitm_frida_data.db` with tables:
- **network_traffic**: All HTTP requests/responses
- **frida_hooks**: Runtime data from app hooks
- **scraped_articles**: Extracted news articles

## Real Android Testing

To test with real Android device:

1. **Setup Android**:
   ```bash
   # Download Frida server for your Android architecture
   # Push to device and run as root
   adb push frida-server /data/local/tmp/
   adb shell chmod 755 /data/local/tmp/frida-server
   adb shell su -c /data/local/tmp/frida-server
   ```

2. **Configure Proxy**:
   - Android Settings → WiFi → Long press network → Modify
   - Set proxy to your computer's IP:8080
   - Install MITM certificate if needed

3. **Browse dawn.com** on Android device and watch the logs!

## Advanced Usage

- Modify `target_domains` in `MitmAddon` to target other websites
- Add custom Frida hooks in `get_frida_script()` method
- Extend HTML parsing in `extract_articles_from_html()`
- Add more data extraction patterns

## Security Note

This is for educational/testing purposes only. Use responsibly and only on your own devices or with proper authorization.