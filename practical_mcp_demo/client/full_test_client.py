#!/usr/bin/env python3
"""
Full MCP Client Implementation
Actually calls tools, accesses resources, and uses prompts through JSON-RPC protocol.
"""

import asyncio
import json
# import uuid  # Not needed
import os
from mcp import StdioServerParameters
from mcp.client.stdio import stdio_client


class FullMCPClient:
    def __init__(self, server_script_path):
        self.server_script_path = server_script_path
        self.read_stream = None
        self.write_stream = None
        self.request_id = 0
        
    def next_request_id(self):
        """Generate next request ID."""
        self.request_id += 1
        return self.request_id
    
    async def send_request(self, method, params=None):
        """Send a JSON-RPC request to the server."""
        request = {
            "jsonrpc": "2.0",
            "id": self.next_request_id(),
            "method": method
        }
        if params:
            request["params"] = params
        
        # Send the request
        await self.write_stream.send(json.dumps(request) + "\n")
        
        # Read the response
        response_line = await self.read_stream.receive()
        response = json.loads(response_line.strip())
        
        if "error" in response:
            raise Exception(f"Server error: {response['error']}")
        
        return response.get("result")
    
    async def connect(self):
        """Connect to the MCP server and initialize."""
        server_params = StdioServerParameters(
            command="python3", 
            args=[self.server_script_path]
        )
        
        print("🔌 Connecting to MCP server...")
        self.connection = stdio_client(server_params)
        self.read_stream, self.write_stream = await self.connection.__aenter__()
        
        # Initialize the connection
        await self.send_request("initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {},
                "resources": {},
                "prompts": {}
            },
            "clientInfo": {
                "name": "test-client",
                "version": "1.0.0"
            }
        })
        
        # Send initialized notification
        await self.write_stream.send(json.dumps({
            "jsonrpc": "2.0",
            "method": "notifications/initialized"
        }) + "\n")
        
        print("✅ Connected and initialized!")
    
    async def disconnect(self):
        """Disconnect from the server."""
        if hasattr(self, 'connection'):
            await self.connection.__aexit__(None, None, None)
    
    async def list_tools(self):
        """List available tools."""
        print("\n📋 Listing Tools...")
        result = await self.send_request("tools/list")
        
        print("Available Tools:")
        for tool in result.get("tools", []):
            print(f"  🔧 {tool['name']}: {tool.get('description', 'No description')}")
        
        return result.get("tools", [])
    
    async def list_resources(self):
        """List available resources."""
        print("\n📚 Listing Resources...")
        result = await self.send_request("resources/list")
        
        print("Available Resources:")
        for resource in result.get("resources", []):
            print(f"  📄 {resource['uri']}: {resource.get('description', 'No description')}")
        
        return result.get("resources", [])
    
    async def list_prompts(self):
        """List available prompts."""
        print("\n💭 Listing Prompts...")
        result = await self.send_request("prompts/list")
        
        print("Available Prompts:")
        for prompt in result.get("prompts", []):
            print(f"  ✨ {prompt['name']}: {prompt.get('description', 'No description')}")
        
        return result.get("prompts", [])
    
    async def call_tool(self, name, arguments=None):
        """Call a tool with given arguments."""
        print(f"\n🔧 Calling tool: {name}")
        if arguments:
            print(f"   Arguments: {arguments}")
        
        result = await self.send_request("tools/call", {
            "name": name,
            "arguments": arguments or {}
        })
        
        print(f"   Result: {result}")
        return result
    
    async def read_resource(self, uri):
        """Read a resource by URI."""
        print(f"\n📄 Reading resource: {uri}")
        
        result = await self.send_request("resources/read", {
            "uri": uri
        })
        
        print(f"   Content: {result}")
        return result
    
    async def get_prompt(self, name, arguments=None):
        """Get a prompt with arguments."""
        print(f"\n✨ Getting prompt: {name}")
        if arguments:
            print(f"   Arguments: {arguments}")
        
        result = await self.send_request("prompts/get", {
            "name": name,
            "arguments": arguments or {}
        })
        
        print(f"   Prompt: {result}")
        return result
    
    async def run_comprehensive_tests(self):
        """Run comprehensive tests of all server features."""
        try:
            await self.connect()
            
            # List everything
            await self.list_tools()
            await self.list_resources()
            await self.list_prompts()
            
            print(f"\n" + "="*60)
            print("🧪 TESTING TOOLS")
            print("="*60)
            
            # Test calculator tool
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
            
            # Test text transform tool
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
            
            # Test counter management
            await self.call_tool("manage_counter", {"action": "reset"})
            await self.call_tool("manage_counter", {"action": "increment", "amount": 5})
            await self.call_tool("manage_counter", {"action": "increment", "amount": 3})
            await self.call_tool("manage_counter", {"action": "get"})
            
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
            print("💭 TESTING PROMPTS")
            print("="*60)
            
            # Test prompts
            await self.get_prompt("generate_code", {
                "language": "python",
                "task": "read a CSV file and calculate the average of a numeric column",
                "style": "commented"
            })
            
            await self.get_prompt("email_template", {
                "type": "welcome",
                "recipient_name": "John Doe",
                "context": "New user registration for our MCP learning platform"
            })
            
            print(f"\n" + "="*60)
            print("🎉 ALL TESTS COMPLETED SUCCESSFULLY!")
            print("="*60)
            
        except Exception as e:
            print(f"\n❌ Error during testing: {e}")
            import traceback
            traceback.print_exc()
        finally:
            await self.disconnect()


async def main():
    """Main function."""
    print("🚀 Full MCP Client Test Suite")
    print("=" * 60)
    
    # Get server path
    server_path = os.path.join(os.path.dirname(__file__), "..", "server", "demo_server.py")
    server_path = os.path.abspath(server_path)
    
    print(f"📍 Server: {server_path}")
    
    # Create and run the client
    client = FullMCPClient(server_path)
    await client.run_comprehensive_tests()


if __name__ == "__main__":
    asyncio.run(main())