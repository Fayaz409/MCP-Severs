# Practical MCP Demo - Hands-On Learning

This folder contains a practical demonstration of how MCP (Model Context Protocol) works in real-world scenarios. It includes a complete server-client setup that you can run and test immediately.

## 🎯 What You'll Learn

- How MCP servers expose tools, resources, and prompts
- How clients interact with MCP servers
- Practical examples of MCP protocol in action
- Real server-client communication patterns

## 📁 Structure

```
practical_mcp_demo/
├── server/
│   └── demo_server.py      # Complete MCP server with 4 tools, 2 resources, 2 prompts
├── client/
│   └── test_client.py      # Test client that exercises all server features
├── run_demo.py             # Quick demo runner
└── README.md               # This file
```

## 🚀 Quick Start

### 1. Test the Server
```bash
cd practical_mcp_demo
python run_demo.py
```

### 2. Run with MCP CLI
```bash
# Make sure MCP is installed
pip install "mcp[cli]"

# Test the server
mcp dev server/demo_server.py
```

### 3. Run the Client Test Suite
```bash
# Connection test (shows how to connect to server)
python client/test_client.py

# Direct functionality demo (shows all features working)
python client/demo_client.py

# Working MCP client examples
python client/working_client.py
python client/interactive_client.py
```

## 🔧 Server Features

### Tools (4 Available)
1. **`calculate`** - Arithmetic operations (add, subtract, multiply, divide)
2. **`text_transform`** - Text manipulation (upper, lower, reverse, count_words, title)
3. **`manage_counter`** - Simple counter management (increment, decrement, reset, get)
4. **`file_info`** - File system information (size, dates, type)

### Resources (2 Available)
1. **`status://server`** - Live server status and statistics
2. **`data://users`** - Demo user database

### Prompts (2 Available)
1. **`generate_code`** - AI code generation templates
2. **`email_template`** - Email template generation

## 🧪 Testing Examples

### Calculator Tool
```python
# Addition
result = await client.call_tool("calculate", {
    "operation": "add",
    "a": 15.5,
    "b": 24.3
})
# Returns: 39.8
```

### Text Transform Tool
```python
# Reverse text
result = await client.call_tool("text_transform", {
    "text": "Hello MCP World",
    "transformation": "reverse"
})
# Returns: "dlroW PCM olleH"
```

### Counter Management
```python
# Increment counter
result = await client.call_tool("manage_counter", {
    "action": "increment",
    "amount": 5
})
# Returns: 5 (or current value + 5)
```

### Resource Access
```python
# Get server status
result = await client.read_resource("status://server")
# Returns: JSON with server stats, uptime, available tools, etc.
```

### Prompt Generation
```python
# Generate code prompt
result = await client.get_prompt("generate_code", {
    "language": "python",
    "task": "read CSV and calculate averages",
    "style": "commented"
})
# Returns: Detailed prompt for AI code generation
```

## 🔍 How It Works

### Server Side (`demo_server.py`)
- Uses FastMCP for rapid development
- Implements the MCP protocol over stdio
- Exposes tools using `@mcp.tool()` decorator
- Provides resources using `@mcp.resource()` decorator
- Creates prompts using `@mcp.prompt()` decorator

### Client Side (`test_client.py`)
- Connects to server via stdio transport
- Lists available tools, resources, and prompts
- Calls tools with parameters and gets results
- Reads resources for data access
- Generates prompts for AI interactions

## 📊 Example Output

When you run the client test, you'll see output like:

```
🚀 Starting MCP Client Test Suite
==================================================
✅ Connected to MCP server!

📋 Available Tools:
----------------------------------------
🔧 calculate: Perform basic arithmetic operations.
🔧 text_transform: Transform text in various ways.
🔧 manage_counter: Manage a simple counter.
🔧 file_info: Get information about a file.

🧮 Testing Calculator Tool:
----------------------------------------
15.5 + 24.3 = 39.8
7 × 8 = 56
100 ÷ 4 = 25.0
```

## 🔌 Integration with AI Clients

### Claude Desktop Configuration
Add this to your Claude Desktop MCP settings:

```json
{
  "mcpServers": {
    "practical-demo": {
      "command": "python3",
      "args": ["/path/to/practical_mcp_demo/server/demo_server.py"]
    }
  }
}
```

### Other MCP Clients
Any MCP-compatible client can connect to the server by running:
```bash
python3 server/demo_server.py
```

## 🎓 Learning Progression

1. **Start Here**: Run `python run_demo.py` to see what's available
2. **Deep Dive**: Run `python client/test_client.py` to see full client-server interaction
3. **Experiment**: Modify the server to add your own tools and resources
4. **Integrate**: Connect the server to Claude Desktop or other MCP clients

## 🛠 Customization Ideas

### Add Your Own Tools
```python
@mcp.tool()
def my_custom_tool(param1: str, param2: int) -> str:
    """Your custom tool description."""
    # Your logic here
    return f"Processed {param1} with {param2}"
```

### Add Custom Resources
```python
@mcp.resource("data://my-data")
def my_data_source() -> str:
    """Return your custom data."""
    return json.dumps({"custom": "data"})
```

### Add Custom Prompts
```python
@mcp.prompt()
def my_prompt_template(context: str) -> str:
    """Generate custom prompts."""
    return f"Create something based on: {context}"
```

## 🚧 Troubleshooting

### Server Won't Start
- Check Python version (3.13+ recommended)
- Install FastMCP: `pip install fastmcp`
- Verify script permissions: `chmod +x server/demo_server.py`

### Client Can't Connect
- Ensure server path is correct in client script
- Install MCP client: `pip install mcp`
- Check that server script runs without errors

### MCP CLI Issues
- Reinstall MCP: `pip install --upgrade "mcp[cli]"`
- Check MCP version: `mcp --version`

## 📚 Next Steps

- Explore the MCP specification: https://modelcontextprotocol.io/docs
- Try integrating with Claude Desktop
- Build your own custom MCP server for specific use cases
- Contribute to the MCP ecosystem

---

**Happy Learning!** 🎉 This practical demo shows you exactly how MCP works in real applications.