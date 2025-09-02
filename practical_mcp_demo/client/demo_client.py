#!/usr/bin/env python3
"""
Working MCP Demo Client
This client actually demonstrates all the server features by calling them directly.
"""

import asyncio
import json
import sys
import os

# Add the server directory to the path so we can import the server
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'server'))

# Import our demo server to test its functions directly
from demo_server import mcp, demo_data


class DirectServerTester:
    """Test the MCP server functions directly to demonstrate functionality."""
    
    def __init__(self):
        self.counter_value = 0
    
    async def test_all_tools(self):
        """Test all tools by calling them directly."""
        print("🚀 Direct MCP Server Function Testing")
        print("=" * 60)
        print("This demonstrates what the MCP server can do!")
        print("=" * 60)
        
        print("\n🧮 TESTING CALCULATOR TOOL")
        print("-" * 40)
        
        # Test calculate tool
        result1 = await self.call_calculate("add", 15.5, 24.3)
        print(f"✅ 15.5 + 24.3 = {result1}")
        
        result2 = await self.call_calculate("multiply", 7, 8)  
        print(f"✅ 7 × 8 = {result2}")
        
        result3 = await self.call_calculate("divide", 100, 4)
        print(f"✅ 100 ÷ 4 = {result3}")
        
        print("\n📝 TESTING TEXT TRANSFORM TOOL")
        print("-" * 40)
        
        # Test text transform tool
        text = "Hello MCP World"
        result4 = await self.call_text_transform(text, "upper")
        print(f"✅ '{text}' → UPPER → '{result4}'")
        
        result5 = await self.call_text_transform(text, "reverse")
        print(f"✅ '{text}' → REVERSE → '{result5}'")
        
        result6 = await self.call_text_transform(text, "count_words")
        print(f"✅ '{text}' → COUNT WORDS → {result6} words")
        
        result7 = await self.call_text_transform(text, "title")
        print(f"✅ '{text}' → TITLE CASE → '{result7}'")
        
        print("\n🔢 TESTING COUNTER MANAGEMENT TOOL")
        print("-" * 40)
        
        # Test counter management
        result8 = await self.call_manage_counter("reset")
        print(f"✅ Reset counter → {result8}")
        
        result9 = await self.call_manage_counter("increment", 5)
        print(f"✅ Increment by 5 → {result9}")
        
        result10 = await self.call_manage_counter("increment", 3)
        print(f"✅ Increment by 3 → {result10}")
        
        result11 = await self.call_manage_counter("get")
        print(f"✅ Current value → {result11}")
        
        result12 = await self.call_manage_counter("decrement", 2)
        print(f"✅ Decrement by 2 → {result12}")
        
        print("\n📁 TESTING FILE INFO TOOL")
        print("-" * 40)
        
        # Test file info
        server_path = os.path.join(os.path.dirname(__file__), "..", "server", "demo_server.py")
        server_path = os.path.abspath(server_path)
        result13 = await self.call_file_info(server_path)
        print(f"✅ File info for server script:")
        file_info = json.loads(result13)
        print(f"   Size: {file_info.get('size_bytes', 'N/A')} bytes")
        print(f"   Exists: {file_info.get('exists', 'N/A')}")
        print(f"   Is file: {file_info.get('is_file', 'N/A')}")
        
        print("\n📚 TESTING RESOURCES")
        print("-" * 40)
        
        # Test resources
        status_result = await self.call_server_status()
        print("✅ Server Status Resource:")
        status_data = json.loads(status_result)
        print(f"   Status: {status_data.get('status', 'N/A')}")
        print(f"   Tools Available: {len(status_data.get('tools_available', []))}")
        print(f"   Current Counter: {status_data.get('demo_data', {}).get('counter', 'N/A')}")
        
        users_result = await self.call_get_users()
        print("\n✅ Users Data Resource:")
        users_data = json.loads(users_result)
        for user in users_data:
            print(f"   User {user['id']}: {user['name']} ({user['email']})")
        
        print("\n✨ TESTING PROMPTS")
        print("-" * 40)
        
        # Test prompts
        code_prompt = await self.call_generate_code_prompt("python", "sort a list of numbers", "commented")
        print("✅ Code Generation Prompt:")
        print("   " + code_prompt.replace('\n', '\n   '))
        
        email_prompt = await self.call_email_template_prompt("welcome", "Alice Johnson", "New user registration")
        print("\n✅ Email Template Prompt:")
        print("   " + email_prompt.replace('\n', '\n   '))
        
        print(f"\n" + "="*60)
        print("🎉 ALL TESTS COMPLETED SUCCESSFULLY!")
        print("   🔧 Tools: 4/4 working (calculate, text_transform, manage_counter, file_info)")
        print("   📚 Resources: 2/2 working (server status, user data)")
        print("   ✨ Prompts: 2/2 working (code generation, email template)")
        print("="*60)
        
        print(f"\n🎯 How to use with real MCP clients:")
        print("   • MCP CLI: mcp dev server/demo_server.py")
        print("   • Claude Desktop: Add server path to MCP configuration")
        print("   • Custom clients: Connect via stdio and use JSON-RPC protocol")
    
    # Tool implementations (direct calls to server functions)
    async def call_calculate(self, operation, a, b):
        # Import the function from our server module
        from demo_server import calculate
        return calculate(operation, a, b)
    
    async def call_text_transform(self, text, transformation):
        from demo_server import text_transform
        return text_transform(text, transformation)
    
    async def call_manage_counter(self, action, amount=1):
        from demo_server import manage_counter
        return manage_counter(action, amount)
    
    async def call_file_info(self, file_path):
        from demo_server import file_info
        return file_info(file_path)
    
    # Resource implementations
    async def call_server_status(self):
        from demo_server import server_status
        return server_status()
    
    async def call_get_users(self):
        from demo_server import get_users
        return get_users()
    
    # Prompt implementations
    async def call_generate_code_prompt(self, language, task, style):
        from demo_server import generate_code
        return generate_code(language, task, style)
    
    async def call_email_template_prompt(self, email_type, recipient_name, context):
        from demo_server import email_template
        return email_template(email_type, recipient_name, context)


async def main():
    """Main function."""
    tester = DirectServerTester()
    await tester.test_all_tools()


if __name__ == "__main__":
    asyncio.run(main())