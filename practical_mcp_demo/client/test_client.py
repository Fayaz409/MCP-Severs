#!/usr/bin/env python3
"""
Simple MCP Client Demo
Tests the practical MCP server by calling its tools and accessing resources.
"""

import asyncio
from mcp import StdioServerParameters, stdio_client
from mcp.client.stdio import StdioClientTransport


class MCPTestClient:
    def __init__(self, server_script_path):
        self.server_script_path = server_script_path
        self.client = None
        
    async def connect(self):
        """Connect to the MCP server."""
        server_params = StdioServerParameters(
            command="python3",
            args=[self.server_script_path]
        )
        
        transport = StdioClientTransport(server_params)
        self.client = await stdio_client(transport)
        print("✅ Connected to MCP server!")
        
    async def list_tools(self):
        """List available tools from the server."""
        print("\n📋 Available Tools:")
        print("-" * 40)
        
        tools = await self.client.list_tools()
        for tool in tools.tools:
            print(f"🔧 {tool.name}: {tool.description}")
        
    async def list_resources(self):
        """List available resources from the server."""
        print("\n📚 Available Resources:")
        print("-" * 40)
        
        resources = await self.client.list_resources()
        for resource in resources.resources:
            print(f"📄 {resource.uri}: {resource.description}")
    
    async def list_prompts(self):
        """List available prompts from the server."""
        print("\n💭 Available Prompts:")
        print("-" * 40)
        
        prompts = await self.client.list_prompts()
        for prompt in prompts.prompts:
            print(f"✨ {prompt.name}: {prompt.description}")
    
    async def test_calculator(self):
        """Test the calculator tool."""
        print("\n🧮 Testing Calculator Tool:")
        print("-" * 40)
        
        # Test addition
        result = await self.client.call_tool("calculate", {
            "operation": "add",
            "a": 15.5,
            "b": 24.3
        })
        print(f"15.5 + 24.3 = {result.content[0].text}")
        
        # Test multiplication
        result = await self.client.call_tool("calculate", {
            "operation": "multiply",
            "a": 7,
            "b": 8
        })
        print(f"7 × 8 = {result.content[0].text}")
        
        # Test division
        result = await self.client.call_tool("calculate", {
            "operation": "divide",
            "a": 100,
            "b": 4
        })
        print(f"100 ÷ 4 = {result.content[0].text}")
    
    async def test_text_transform(self):
        """Test the text transformation tool."""
        print("\n📝 Testing Text Transform Tool:")
        print("-" * 40)
        
        test_text = "Hello MCP World"
        
        # Test uppercase
        result = await self.client.call_tool("text_transform", {
            "text": test_text,
            "transformation": "upper"
        })
        print(f"Uppercase: {result.content[0].text}")
        
        # Test reverse
        result = await self.client.call_tool("text_transform", {
            "text": test_text,
            "transformation": "reverse"
        })
        print(f"Reversed: {result.content[0].text}")
        
        # Test word count
        result = await self.client.call_tool("text_transform", {
            "text": test_text,
            "transformation": "count_words"
        })
        print(f"Word count: {result.content[0].text}")
    
    async def test_counter(self):
        """Test the counter management tool."""
        print("\n🔢 Testing Counter Tool:")
        print("-" * 40)
        
        # Reset counter
        result = await self.client.call_tool("manage_counter", {"action": "reset"})
        print(f"Reset counter: {result.content[0].text}")
        
        # Increment counter
        result = await self.client.call_tool("manage_counter", {
            "action": "increment",
            "amount": 5
        })
        print(f"Increment by 5: {result.content[0].text}")
        
        # Increment again
        result = await self.client.call_tool("manage_counter", {
            "action": "increment",
            "amount": 3
        })
        print(f"Increment by 3: {result.content[0].text}")
        
        # Get current value
        result = await self.client.call_tool("manage_counter", {"action": "get"})
        print(f"Current value: {result.content[0].text}")
    
    async def test_file_info(self):
        """Test the file info tool."""
        print("\n📁 Testing File Info Tool:")
        print("-" * 40)
        
        # Test with the server script itself
        result = await self.client.call_tool("file_info", {
            "file_path": self.server_script_path
        })
        print("Server script info:")
        print(result.content[0].text)
    
    async def test_resources(self):
        """Test accessing resources."""
        print("\n📊 Testing Resources:")
        print("-" * 40)
        
        # Get server status
        result = await self.client.read_resource("status://server")
        print("Server Status:")
        print(result.contents[0].text)
        
        print("\n" + "="*50)
        
        # Get user data
        result = await self.client.read_resource("data://users")
        print("User Data:")
        print(result.contents[0].text)
    
    async def test_prompts(self):
        """Test the prompt templates."""
        print("\n✨ Testing Prompts:")
        print("-" * 40)
        
        # Test code generation prompt
        result = await self.client.get_prompt("generate_code", {
            "language": "python",
            "task": "read a CSV file and calculate the average of a numeric column",
            "style": "commented"
        })
        print("Code Generation Prompt:")
        print(result.messages[0].content.text)
        
        print("\n" + "="*50)
        
        # Test email template prompt
        result = await self.client.get_prompt("email_template", {
            "type": "welcome",
            "recipient_name": "John Doe",
            "context": "New user registration for our MCP learning platform"
        })
        print("Email Template Prompt:")
        print(result.messages[0].content.text)
    
    async def run_all_tests(self):
        """Run all test methods."""
        try:
            await self.connect()
            
            # List everything available
            await self.list_tools()
            await self.list_resources()
            await self.list_prompts()
            
            # Test all tools
            await self.test_calculator()
            await self.test_text_transform()
            await self.test_counter()
            await self.test_file_info()
            
            # Test resources
            await self.test_resources()
            
            # Test prompts
            await self.test_prompts()
            
            print("\n🎉 All tests completed successfully!")
            
        except Exception as e:
            print(f"❌ Error during testing: {e}")
        finally:
            if self.client:
                await self.client.close()


async def main():
    """Main function to run the MCP client tests."""
    print("🚀 Starting MCP Client Test Suite")
    print("=" * 50)
    
    # Path to the server script (adjust if needed)
    import os
    server_path = os.path.join(os.path.dirname(__file__), "..", "server", "demo_server.py")
    server_path = os.path.abspath(server_path)
    
    print(f"Server script path: {server_path}")
    
    # Create and run the test client
    test_client = MCPTestClient(server_path)
    await test_client.run_all_tests()


if __name__ == "__main__":
    asyncio.run(main())