#!/usr/bin/env python3
"""
Working MCP Client Demo
A simplified client that demonstrates MCP server interaction using the correct API.
"""

import asyncio
import json
from mcp import StdioServerParameters
from mcp.client.stdio import stdio_client
import os


async def test_mcp_server():
    """Test the MCP server with a simple approach."""
    print("🚀 Testing MCP Server")
    print("=" * 40)
    
    # Server path
    server_path = os.path.join("server", "demo_server.py")
    server_path = os.path.abspath(server_path)
    
    print(f"Server script: {server_path}")
    
    # Server parameters
    server_params = StdioServerParameters(
        command="python3",
        args=[server_path]
    )
    
    try:
        print("🔌 Connecting to server...")
        async with stdio_client(server_params) as (read, write):
            print("✅ Connected!")
            
            # Send a simple test message to verify connection
            # For now, just demonstrate the connection works
            print("📡 Server streams established:")
            print(f"  - Read stream: {type(read).__name__}")
            print(f"  - Write stream: {type(write).__name__}")
            
            # Note: Full MCP protocol implementation would require
            # implementing the JSON-RPC protocol over these streams
            print("\n💡 Connection successful!")
            print("   To fully test the server, use:")
            print("   mcp dev server/demo_server.py")
            
    except Exception as e:
        print(f"❌ Error: {e}")


async def test_with_mcp_cli():
    """Show how to test with MCP CLI."""
    print("\n🛠 Testing with MCP CLI:")
    print("=" * 40)
    print("Run these commands to test the server:")
    print()
    print("1. Install MCP CLI if not installed:")
    print("   pip install 'mcp[cli]'")
    print()
    print("2. Test the server:")
    print("   mcp dev server/demo_server.py")
    print()
    print("3. Available features:")
    print("   📋 Tools: calculate, text_transform, manage_counter, file_info")
    print("   📚 Resources: status://server, data://users")
    print("   💭 Prompts: generate_code, email_template")


async def show_server_features():
    """Display what the server offers."""
    print("\n🎯 Server Features:")
    print("=" * 40)
    
    features = {
        "Tools": [
            "calculate - arithmetic operations (add, subtract, multiply, divide)",
            "text_transform - text manipulation (upper, lower, reverse, etc.)",
            "manage_counter - counter management (increment, decrement, reset)",
            "file_info - file system information"
        ],
        "Resources": [
            "status://server - real-time server status",
            "data://users - demo user database"
        ],
        "Prompts": [
            "generate_code - code generation templates",
            "email_template - email template generation"
        ]
    }
    
    for category, items in features.items():
        print(f"\n📋 {category}:")
        for item in items:
            print(f"  • {item}")


async def main():
    """Main function."""
    await test_mcp_server()
    await test_with_mcp_cli()
    await show_server_features()
    
    print("\n" + "=" * 50)
    print("🎓 Next Steps:")
    print("1. Use 'mcp dev server/demo_server.py' for interactive testing")
    print("2. Integrate with Claude Desktop using the server path")
    print("3. Build your own MCP client using the MCP protocol")
    print("4. Explore the server code to understand implementation")


if __name__ == "__main__":
    asyncio.run(main())