#!/usr/bin/env python3
"""
Quick Demo Runner
Simple script to test the MCP server directly.
"""

import subprocess
import sys
import os

def run_server_test():
    """Run the server in test mode to show available features."""
    print("🚀 MCP Practical Demo")
    print("=" * 50)
    
    server_path = os.path.join("server", "demo_server.py")
    
    print(f"Testing server: {server_path}")
    print("\nStarting server (this will show available features)...")
    print("-" * 50)
    
    try:
        # Run the server directly to see its startup message
        result = subprocess.run([
            sys.executable, server_path
        ], capture_output=True, text=True, timeout=2)
        
        print("Server startup output:")
        print(result.stdout)
        if result.stderr:
            print("Errors:")
            print(result.stderr)
            
    except subprocess.TimeoutExpired:
        print("✅ Server started successfully (timed out after 2 seconds as expected)")
        print("The server is designed to run continuously and communicate over stdio.")
    except Exception as e:
        print(f"❌ Error running server: {e}")
    
    print("\n" + "=" * 50)
    print("🔧 Available Tools:")
    print("  • calculate - Perform arithmetic operations")
    print("  • text_transform - Transform text (upper, lower, reverse, etc.)")
    print("  • manage_counter - Increment/decrement/reset a counter")
    print("  • file_info - Get file information")
    
    print("\n📚 Available Resources:")
    print("  • status://server - Server status and statistics")
    print("  • data://users - Demo user data")
    
    print("\n💭 Available Prompts:")
    print("  • generate_code - Generate code snippets")
    print("  • email_template - Generate email templates")
    
    print("\n🎯 How to use:")
    print("1. Install MCP: pip install 'mcp[cli]'")
    print("2. Test server: mcp dev server/demo_server.py")
    print("3. Use with Claude Desktop or other MCP clients")
    print("4. Run client test: python client/test_client.py")

if __name__ == "__main__":
    run_server_test()