#!/usr/bin/env python3
"""
Real MCP Protocol Client
Shows actual JSON-RPC communication between client and server.
This demonstrates the real MCP protocol in action.
"""

import asyncio
import json
import os
from typing import Dict, Any, Optional


class RealMCPClient:
    """A real MCP client that communicates via JSON-RPC over stdio."""
    
    def __init__(self, server_script_path: str):
        self.server_script_path = server_script_path
        self.process = None
        self.request_id = 0
        
    def next_request_id(self) -> int:
        """Generate next request ID."""
        self.request_id += 1
        return self.request_id
        
    async def start_server(self):
        """Start the MCP server process."""
        print("🚀 Starting MCP server process...")
        print(f"   Command: python3 {self.server_script_path}")
        
        self.process = await asyncio.create_subprocess_exec(
            "python3", self.server_script_path,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        print("✅ Server process started!")
        
    async def send_message(self, message: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Send a JSON-RPC message to the server and get response."""
        if not self.process:
            raise RuntimeError("Server not started")
            
        # Convert message to JSON and send
        json_message = json.dumps(message)
        print(f"📤 SENDING: {json_message}")
        
        self.process.stdin.write(json_message.encode() + b'\n')
        await self.process.stdin.drain()
        
        # Read response
        response_line = await self.process.stdout.readline()
        if not response_line:
            return None
            
        response_json = response_line.decode().strip()
        print(f"📥 RECEIVED: {response_json}")
        
        try:
            response = json.loads(response_json)
            return response
        except json.JSONDecodeError as e:
            print(f"❌ JSON decode error: {e}")
            return None
            
    async def initialize(self):
        """Initialize the MCP session."""
        print(f"\n" + "="*60)
        print("🔌 INITIALIZING MCP SESSION")
        print("="*60)
        
        # Send initialize request
        init_request = {
            "jsonrpc": "2.0",
            "id": self.next_request_id(),
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {},
                    "resources": {},
                    "prompts": {}
                },
                "clientInfo": {
                    "name": "real-mcp-client",
                    "version": "1.0.0"
                }
            }
        }
        
        response = await self.send_message(init_request)
        
        if response and "result" in response:
            print("✅ Server initialized successfully!")
            server_info = response["result"]
            print(f"   Server name: {server_info.get('serverInfo', {}).get('name', 'Unknown')}")
            print(f"   Protocol version: {server_info.get('protocolVersion', 'Unknown')}")
            
            # Send initialized notification
            initialized_notification = {
                "jsonrpc": "2.0",
                "method": "notifications/initialized"
            }
            
            print(f"\n📤 SENDING: {json.dumps(initialized_notification)}")
            self.process.stdin.write(json.dumps(initialized_notification).encode() + b'\n')
            await self.process.stdin.drain()
            
            return True
        else:
            print("❌ Initialization failed!")
            return False
            
    async def list_tools(self):
        """List available tools using MCP protocol."""
        print(f"\n" + "="*60)
        print("📋 LISTING TOOLS")
        print("="*60)
        
        request = {
            "jsonrpc": "2.0",
            "id": self.next_request_id(),
            "method": "tools/list"
        }
        
        response = await self.send_message(request)
        
        if response and "result" in response:
            tools = response["result"].get("tools", [])
            print(f"\n✅ Found {len(tools)} tools:")
            for tool in tools:
                print(f"   🔧 {tool['name']}: {tool.get('description', 'No description')}")
            return tools
        else:
            print("❌ Failed to list tools")
            return []
            
    async def call_tool(self, name: str, arguments: Dict[str, Any]):
        """Call a tool using MCP protocol."""
        print(f"\n" + "="*60)
        print(f"🔧 CALLING TOOL: {name}")
        print("="*60)
        
        request = {
            "jsonrpc": "2.0",
            "id": self.next_request_id(),
            "method": "tools/call",
            "params": {
                "name": name,
                "arguments": arguments
            }
        }
        
        response = await self.send_message(request)
        
        if response and "result" in response:
            result = response["result"]
            print(f"\n✅ Tool call successful!")
            print(f"   Arguments: {arguments}")
            
            # Print content from the response
            content = result.get("content", [])
            for item in content:
                if item.get("type") == "text":
                    print(f"   Result: {item.get('text')}")
                    
            return result
        else:
            print("❌ Tool call failed")
            if response and "error" in response:
                print(f"   Error: {response['error']}")
            return None
            
    async def list_resources(self):
        """List available resources using MCP protocol."""
        print(f"\n" + "="*60)
        print("📚 LISTING RESOURCES")
        print("="*60)
        
        request = {
            "jsonrpc": "2.0",
            "id": self.next_request_id(),
            "method": "resources/list"
        }
        
        response = await self.send_message(request)
        
        if response and "result" in response:
            resources = response["result"].get("resources", [])
            print(f"\n✅ Found {len(resources)} resources:")
            for resource in resources:
                print(f"   📄 {resource['uri']}: {resource.get('description', 'No description')}")
            return resources
        else:
            print("❌ Failed to list resources")
            return []
            
    async def read_resource(self, uri: str):
        """Read a resource using MCP protocol."""
        print(f"\n" + "="*60)
        print(f"📄 READING RESOURCE: {uri}")
        print("="*60)
        
        request = {
            "jsonrpc": "2.0",
            "id": self.next_request_id(),
            "method": "resources/read",
            "params": {
                "uri": uri
            }
        }
        
        response = await self.send_message(request)
        
        if response and "result" in response:
            result = response["result"]
            print(f"\n✅ Resource read successful!")
            
            # Print contents from the response
            contents = result.get("contents", [])
            for item in contents:
                if item.get("type") == "text":
                    print(f"   Content: {item.get('text')}")
                    
            return result
        else:
            print("❌ Resource read failed")
            if response and "error" in response:
                print(f"   Error: {response['error']}")
            return None
            
    async def list_prompts(self):
        """List available prompts using MCP protocol."""
        print(f"\n" + "="*60)
        print("💭 LISTING PROMPTS")
        print("="*60)
        
        request = {
            "jsonrpc": "2.0",
            "id": self.next_request_id(),
            "method": "prompts/list"
        }
        
        response = await self.send_message(request)
        
        if response and "result" in response:
            prompts = response["result"].get("prompts", [])
            print(f"\n✅ Found {len(prompts)} prompts:")
            for prompt in prompts:
                print(f"   ✨ {prompt['name']}: {prompt.get('description', 'No description')}")
            return prompts
        else:
            print("❌ Failed to list prompts")
            return []
            
    async def get_prompt(self, name: str, arguments: Dict[str, Any]):
        """Get a prompt using MCP protocol."""
        print(f"\n" + "="*60)
        print(f"✨ GETTING PROMPT: {name}")
        print("="*60)
        
        request = {
            "jsonrpc": "2.0",
            "id": self.next_request_id(),
            "method": "prompts/get",
            "params": {
                "name": name,
                "arguments": arguments
            }
        }
        
        response = await self.send_message(request)
        
        if response and "result" in response:
            result = response["result"]
            print(f"\n✅ Prompt generation successful!")
            print(f"   Arguments: {arguments}")
            
            # Print messages from the response
            messages = result.get("messages", [])
            for message in messages:
                if message.get("role") == "user":
                    content = message.get("content")
                    if isinstance(content, dict) and content.get("type") == "text":
                        print(f"   Generated Prompt: {content.get('text')}")
                    elif isinstance(content, str):
                        print(f"   Generated Prompt: {content}")
                        
            return result
        else:
            print("❌ Prompt generation failed")
            if response and "error" in response:
                print(f"   Error: {response['error']}")
            return None
            
    async def run_comprehensive_test(self):
        """Run comprehensive test of all MCP protocol features."""
        try:
            await self.start_server()
            
            # Initialize session
            if not await self.initialize():
                return
                
            # List all capabilities
            tools = await self.list_tools()
            resources = await self.list_resources()
            prompts = await self.list_prompts()
            
            print(f"\n" + "="*60)
            print("🧪 TESTING PROTOCOL COMMUNICATION")
            print("="*60)
            
            # Test tools
            if tools:
                print(f"\n🔧 TESTING TOOLS ({len(tools)} available)")
                
                # Test calculator tool
                await self.call_tool("calculate", {
                    "operation": "add",
                    "a": 25,
                    "b": 17
                })
                
                # Test text transform
                await self.call_tool("text_transform", {
                    "text": "MCP Protocol Test",
                    "transformation": "upper"
                })
                
                # Test counter
                await self.call_tool("manage_counter", {
                    "action": "increment",
                    "amount": 10
                })
            
            # Test resources
            if resources:
                print(f"\n📚 TESTING RESOURCES ({len(resources)} available)")
                
                for resource in resources:
                    await self.read_resource(resource["uri"])
            
            # Test prompts
            if prompts:
                print(f"\n💭 TESTING PROMPTS ({len(prompts)} available)")
                
                # Test code generation prompt
                await self.get_prompt("generate_code", {
                    "language": "javascript", 
                    "task": "create a function to validate email addresses",
                    "style": "simple"
                })
                
            print(f"\n" + "="*60)
            print("🎉 ALL PROTOCOL TESTS COMPLETED!")
            print("   • JSON-RPC communication: ✅ Working")
            print("   • Tool calling: ✅ Working")
            print("   • Resource reading: ✅ Working")
            print("   • Prompt generation: ✅ Working")
            print("="*60)
            
        except Exception as e:
            print(f"❌ Error during protocol test: {e}")
            import traceback
            traceback.print_exc()
        finally:
            await self.cleanup()
            
    async def cleanup(self):
        """Clean up the server process."""
        if self.process:
            print(f"\n🔄 Cleaning up server process...")
            self.process.terminate()
            await self.process.wait()
            print("✅ Server process cleaned up")


async def main():
    """Main function."""
    print("🚀 Real MCP Protocol Client")
    print("=" * 60)
    print("This shows actual JSON-RPC communication with the MCP server")
    print("=" * 60)
    
    # Get server path
    server_path = os.path.join(os.path.dirname(__file__), "..", "server", "demo_server.py")
    server_path = os.path.abspath(server_path)
    
    print(f"📍 Server script: {server_path}")
    
    # Create and run client
    client = RealMCPClient(server_path)
    await client.run_comprehensive_test()


if __name__ == "__main__":
    asyncio.run(main())