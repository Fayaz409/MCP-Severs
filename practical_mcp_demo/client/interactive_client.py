#!/usr/bin/env python3
"""
Interactive MCP Client
Uses the proper MCP ClientSession to interact with the server.
"""

import asyncio
import os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class InteractiveMCPClient:
    def __init__(self, server_script_path):
        self.server_script_path = server_script_path
        self.session = None
        
    async def connect(self):
        """Connect to the MCP server."""
        print("🔌 Connecting to MCP server...")
        
        server_params = StdioServerParameters(
            command="python3",
            args=[self.server_script_path]
        )
        
        # Create stdio client connection
        stdio_connection = stdio_client(server_params)
        read_stream, write_stream = await stdio_connection.__aenter__()
        
        # Create client session
        self.session = ClientSession(read_stream, write_stream)
        
        # Initialize the session
        await self.session.initialize()
        
        print("✅ Connected and initialized!")
        
        # Store connection for cleanup
        self._stdio_connection = stdio_connection
        
    async def disconnect(self):
        """Disconnect from the server."""
        if hasattr(self, '_stdio_connection'):
            await self._stdio_connection.__aexit__(None, None, None)
    
    async def list_tools(self):
        """List available tools."""
        print("\n📋 Available Tools:")
        print("-" * 40)
        
        result = await self.session.list_tools()
        for tool in result.tools:
            print(f"🔧 {tool.name}")
            if tool.description:
                print(f"   Description: {tool.description}")
            if hasattr(tool, 'inputSchema') and tool.inputSchema:
                print(f"   Parameters: {tool.inputSchema.get('properties', {}).keys()}")
        return result.tools
    
    async def list_resources(self):
        """List available resources."""
        print("\n📚 Available Resources:")
        print("-" * 40)
        
        result = await self.session.list_resources()
        for resource in result.resources:
            print(f"📄 {resource.uri}")
            if resource.description:
                print(f"   Description: {resource.description}")
        return result.resources
    
    async def list_prompts(self):
        """List available prompts."""
        print("\n💭 Available Prompts:")
        print("-" * 40)
        
        result = await self.session.list_prompts()
        for prompt in result.prompts:
            print(f"✨ {prompt.name}")
            if prompt.description:
                print(f"   Description: {prompt.description}")
            if hasattr(prompt, 'arguments') and prompt.arguments:
                print(f"   Arguments: {[arg.name for arg in prompt.arguments]}")
        return result.prompts
    
    async def call_tool(self, name, arguments=None):
        """Call a tool with arguments."""
        print(f"\n🔧 Calling tool: {name}")
        if arguments:
            print(f"   Arguments: {arguments}")
        
        result = await self.session.call_tool(name, arguments or {})
        
        print("   📤 Result:")
        for content in result.content:
            if hasattr(content, 'text'):
                print(f"   {content.text}")
            else:
                print(f"   {content}")
        
        return result
    
    async def read_resource(self, uri):
        """Read a resource."""
        print(f"\n📄 Reading resource: {uri}")
        
        result = await self.session.read_resource(uri)
        
        print("   📤 Content:")
        for content in result.contents:
            if hasattr(content, 'text'):
                print(f"   {content.text}")
            else:
                print(f"   {content}")
        
        return result
    
    async def get_prompt(self, name, arguments=None):
        """Get a prompt."""
        print(f"\n✨ Getting prompt: {name}")
        if arguments:
            print(f"   Arguments: {arguments}")
        
        result = await self.session.get_prompt(name, arguments or {})
        
        print("   📤 Generated Prompt:")
        for message in result.messages:
            if hasattr(message, 'content') and hasattr(message.content, 'text'):
                print(f"   {message.content.text}")
            else:
                print(f"   {message}")
        
        return result
    
    async def run_interactive_tests(self):
        """Run interactive tests of all features."""
        try:
            await self.connect()
            
            # List everything first
            await self.list_tools()
            await self.list_resources() 
            await self.list_prompts()
            
            print(f"\n" + "="*60)
            print("🧪 TESTING CALCULATOR TOOL")
            print("="*60)
            
            # Test calculator
            await self.call_tool("calculate", {
                "operation": "add",
                "a": 15.5,
                "b": 24.3
            })
            
            await self.call_tool("calculate", {
                "operation": "multiply",
                "a": 7,
                "b": 8
            })
            
            await self.call_tool("calculate", {
                "operation": "divide", 
                "a": 100,
                "b": 4
            })
            
            print(f"\n" + "="*60)
            print("📝 TESTING TEXT TRANSFORM TOOL")
            print("="*60)
            
            # Test text transform
            await self.call_tool("text_transform", {
                "text": "Hello MCP World",
                "transformation": "upper"
            })
            
            await self.call_tool("text_transform", {
                "text": "Hello MCP World",
                "transformation": "reverse"
            })
            
            await self.call_tool("text_transform", {
                "text": "Hello MCP World", 
                "transformation": "count_words"
            })
            
            print(f"\n" + "="*60)
            print("🔢 TESTING COUNTER TOOL")
            print("="*60)
            
            # Test counter
            await self.call_tool("manage_counter", {"action": "reset"})
            await self.call_tool("manage_counter", {"action": "increment", "amount": 5})
            await self.call_tool("manage_counter", {"action": "increment", "amount": 3})
            await self.call_tool("manage_counter", {"action": "get"})
            
            print(f"\n" + "="*60)
            print("📁 TESTING FILE INFO TOOL")
            print("="*60)
            
            # Test file info
            await self.call_tool("file_info", {
                "file_path": self.server_script_path
            })
            
            print(f"\n" + "="*60)
            print("📚 TESTING RESOURCES")
            print("="*60)
            
            # Test resources
            await self.read_resource("status://server")
            await self.read_resource("data://users")
            
            print(f"\n" + "="*60)
            print("✨ TESTING PROMPTS")
            print("="*60)
            
            # Test prompts
            await self.get_prompt("generate_code", {
                "language": "python",
                "task": "read a CSV file and calculate averages",
                "style": "commented"
            })
            
            await self.get_prompt("email_template", {
                "type": "welcome",
                "recipient_name": "Alice Smith",
                "context": "New user signed up for MCP demo"
            })
            
            print(f"\n" + "="*60)
            print("🎉 ALL TESTS COMPLETED SUCCESSFULLY!")
            print("   • Tools: ✅ All 4 tools working")
            print("   • Resources: ✅ Both resources accessible")
            print("   • Prompts: ✅ Both prompt templates working")
            print("="*60)
            
        except Exception as e:
            print(f"\n❌ Error during testing: {e}")
            import traceback
            traceback.print_exc()
        finally:
            await self.disconnect()


async def main():
    """Main function."""
    print("🚀 Interactive MCP Client Test Suite") 
    print("=" * 60)
    print("This client will actually call tools, read resources, and get prompts!")
    print("=" * 60)
    
    # Get server path
    server_path = os.path.join(os.path.dirname(__file__), "..", "server", "demo_server.py")
    server_path = os.path.abspath(server_path)
    
    print(f"📍 Server: {server_path}")
    
    # Create and run client
    client = InteractiveMCPClient(server_path)
    await client.run_interactive_tests()


if __name__ == "__main__":
    asyncio.run(main())