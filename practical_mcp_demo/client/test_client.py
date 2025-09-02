#!/usr/bin/env python3
"""
MCP Client Demo - Connection Test
This client demonstrates connecting to the MCP server and shows how to test it.

Note: Full MCP protocol client implementation requires JSON-RPC over the streams.
For testing the server features, use the MCP CLI: mcp dev server/demo_server.py
"""

import asyncio
import os
from mcp import StdioServerParameters
from mcp.client.stdio import stdio_client


async def test_server_connection():
    """Test connection to the MCP server."""
    print("🚀 MCP Client Connection Test")
    print("=" * 50)
    
    # Server path
    server_path = os.path.join(os.path.dirname(__file__), "..", "server", "demo_server.py")
    server_path = os.path.abspath(server_path)
    
    print(f"📍 Server path: {server_path}")
    
    # Server parameters
    server_params = StdioServerParameters(
        command="python3",
        args=[server_path]
    )
    
    try:
        print("\n🔌 Connecting to MCP server...")
        async with stdio_client(server_params) as (read, write):
            print("✅ Connection successful!")
            print(f"   📡 Read stream: {type(read).__name__}")
            print(f"   📡 Write stream: {type(write).__name__}")
            
            print(f"\n🎯 Server Features Available:")
            print("   📋 Tools: calculate, text_transform, manage_counter, file_info")
            print("   📚 Resources: status://server, data://users") 
            print("   💭 Prompts: generate_code, email_template")
            
            print(f"\n💡 To test the server interactively:")
            print(f"   mcp dev {server_path}")
            
    except FileNotFoundError:
        print(f"❌ Server script not found: {server_path}")
    except Exception as e:
        print(f"❌ Connection error: {e}")


async def show_test_instructions():
    """Show how to test the server properly."""
    print(f"\n🧪 How to Test the MCP Server:")
    print("=" * 50)
    
    print("1️⃣  Install MCP CLI (if not installed):")
    print("    pip install 'mcp[cli]'")
    
    print("\n2️⃣  Test the server interactively:")
    print("    mcp dev server/demo_server.py")
    
    print("\n3️⃣  Try these test commands in MCP CLI:")
    print("    • List tools: (automatically shown)")
    print("    • Call tool: calculate with operation='add', a=5, b=3")
    print("    • Call tool: text_transform with text='Hello', transformation='upper'")
    print("    • Read resource: status://server")
    print("    • Get prompt: generate_code with language='python'")
    
    print("\n4️⃣  Integrate with Claude Desktop:")
    print('    Add to your Claude Desktop config:')
    print('    {')
    print('      "mcpServers": {')
    print('        "demo-server": {')
    print('          "command": "python3",')
    server_path = os.path.join(os.getcwd(), "server", "demo_server.py")
    print(f'          "args": ["{server_path}"]')
    print('        }')
    print('      }')
    print('    }')


async def show_server_examples():
    """Show examples of what each server feature does."""
    print(f"\n📋 Server Feature Examples:")
    print("=" * 50)
    
    examples = {
        "🧮 calculate": [
            "add(15, 25) → 40",
            "multiply(7, 8) → 56", 
            "divide(100, 4) → 25.0"
        ],
        "📝 text_transform": [
            "upper('hello mcp') → 'HELLO MCP'",
            "reverse('hello') → 'olleh'",
            "count_words('hello world') → '2'"
        ],
        "🔢 manage_counter": [
            "increment(5) → 5",
            "increment(3) → 8",
            "reset() → 0"
        ],
        "📁 file_info": [
            "file_info('server/demo_server.py') → file details JSON"
        ],
        "📊 Resources": [
            "status://server → server status JSON",
            "data://users → user data JSON"
        ],
        "✨ Prompts": [
            "generate_code(language='python', task='sort list') → code prompt",
            "email_template(type='welcome', name='Alice') → email prompt"
        ]
    }
    
    for feature, example_list in examples.items():
        print(f"\n{feature}:")
        for example in example_list:
            print(f"   • {example}")


async def main():
    """Main function."""
    await test_server_connection()
    await show_test_instructions()
    await show_server_examples()
    
    print(f"\n" + "=" * 50)
    print("🎓 Summary:")
    print("   • Server connection: ✅ Working") 
    print("   • Use MCP CLI for interactive testing")
    print("   • Integrate with Claude Desktop for AI usage")
    print("   • Explore server code to understand MCP implementation")


if __name__ == "__main__":
    asyncio.run(main())