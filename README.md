# MCP Learn - Model Context Protocol Server Implementation

A comprehensive learning project for understanding and implementing Model Context Protocol (MCP) servers using Python and the FastMCP library. This repository demonstrates how to build MCP servers that can integrate with AI clients like Claude Desktop to provide custom tools, resources, and prompts.

## 🚀 What is MCP?

The Model Context Protocol (MCP) is an open standard that enables AI models to securely connect to external data sources and tools. It provides a standardized way for AI applications to:

- Access external data and services
- Execute tools and functions
- Provide reusable prompt templates
- Maintain secure, controlled interactions

## 📁 Project Structure

```
MCP_Learn/
├── main.py                          # Simple Python application entry point
├── MCP_Servers/
│   └── test.py                     # Basic MCP server implementation with examples
├── practical_mcp_demo/             # 🆕 Complete hands-on MCP demo
│   ├── server/demo_server.py       #     Advanced MCP server with 4 tools, 2 resources, 2 prompts
│   ├── client/test_client.py       #     Full test client demonstrating all features
│   ├── run_demo.py                 #     Quick demo runner
│   └── README.md                   #     Detailed practical guide
├── pyproject.toml                  # Project configuration and dependencies
├── uv.lock                         # Locked dependencies for reproducible builds
├── .python-version                 # Python version specification (3.13+)
├── CLAUDE.md                       # Claude Code guidance file
└── README.md                       # This file
```

## 🛠 Features

This project includes two MCP server implementations:

### Basic Server (`MCP_Servers/test.py`)
Demonstrates core MCP concepts:
- **Tools**: `add(a, b)` for arithmetic operations
- **Resources**: `status://health` for server health information
- **Prompts**: `greet_user(name, style)` for customizable greetings

### 🆕 **Practical Demo Server (`practical_mcp_demo/`)**
Complete hands-on implementation with:

#### **4 Advanced Tools**
- `calculate` - Full arithmetic operations (add, subtract, multiply, divide)
- `text_transform` - Text manipulation (upper, lower, reverse, count_words, title)
- `manage_counter` - Interactive counter management (increment, decrement, reset)
- `file_info` - File system information and analysis

#### **2 Live Resources**
- `status://server` - Real-time server status and statistics
- `data://users` - Demo user database with sample data

#### **2 AI Prompts**
- `generate_code` - Intelligent code generation templates
- `email_template` - Professional email template generation

#### **Complete Test Suite**
- Full client implementation demonstrating all server features
- Practical examples of MCP protocol communication
- Ready-to-run test scenarios

## 📋 Prerequisites

- Python 3.13 or higher
- `uv` package manager (recommended) or `pip`

## 🔧 Installation

### Option 1: Using uv (Recommended)
```bash
# Clone the repository
git clone <repository-url>
cd MCP_Learn

# Install dependencies
uv install
```

### Option 2: Using pip
```bash
# Install MCP CLI globally
python3 -m pip install "mcp[cli]"

# Install project dependencies
pip install -r requirements.txt  # if available
```

## 🚀 Usage

### Quick Start with Practical Demo

For immediate hands-on experience:

```bash
# Navigate to the practical demo
cd practical_mcp_demo

# Quick test of all features
python run_demo.py

# Full client-server test suite
python client/test_client.py
```

### Running MCP Servers

#### Basic Server
```bash
# Run the basic server
mcp dev MCP_Servers/test.py
```

#### Advanced Demo Server
```bash
# Run the practical demo server
mcp dev practical_mcp_demo/server/demo_server.py
```

Both servers will listen for MCP protocol communications over stdio, ready to integrate with MCP clients.

### Running the Main Application

```bash
python main.py
```

### Testing the Server

Once running, you can test the server functionality:

1. **Tool Testing**: The `add` tool can perform arithmetic operations
2. **Resource Access**: Query the `status://health` endpoint for server status
3. **Prompt Generation**: Use the `greet_user` prompt with different names and styles

## 🔌 Integration with AI Clients

This MCP server can be integrated with AI clients like:

- **Claude Desktop**: Add as a local MCP server
- **Other MCP-compatible clients**: Follow standard MCP integration patterns

### Example Claude Desktop Configuration

#### Basic Server
```json
{
  "mcpServers": {
    "mcp-learn-basic": {
      "command": "python",
      "args": ["path/to/MCP_Learn/MCP_Servers/test.py"]
    }
  }
}
```

#### 🆕 **Practical Demo Server (Recommended)**
```json
{
  "mcpServers": {
    "mcp-learn-demo": {
      "command": "python",
      "args": ["path/to/MCP_Learn/practical_mcp_demo/server/demo_server.py"]
    }
  }
}
```

## 🏗 Development

### Project Architecture

- **FastMCP Framework**: Utilizes the FastMCP library for rapid MCP server development
- **Decorator-based**: Uses Python decorators (`@mcp.tool()`, `@mcp.resource()`, `@mcp.prompt()`) for clean, readable code
- **Stdio Communication**: Implements MCP protocol over standard input/output for client compatibility

### Adding New Features

1. **New Tools**: Add functions with `@mcp.tool()` decorator
2. **New Resources**: Create functions with `@mcp.resource("uri://path")` decorator
3. **New Prompts**: Implement template functions with `@mcp.prompt()` decorator

Example:
```python
@mcp.tool()
def multiply(x: float, y: float) -> float:
    """Multiply two numbers."""
    return x * y

@mcp.resource("data://example")
def get_example_data() -> str:
    """Return example data."""
    return '{"example": "data"}'
```

## 🧪 Testing

Currently, testing is performed manually by running the server and testing integration with MCP clients. Future enhancements may include:

- Unit tests for individual tools and resources
- Integration tests with MCP protocol
- Automated testing with mock clients

## 📚 Learning Resources

- [MCP Specification](https://modelcontextprotocol.io/docs)
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
- [Claude Desktop MCP Integration](https://claude.ai/docs)

## 🤝 Contributing

This is a learning project! Feel free to:

1. Fork the repository
2. Create feature branches for experiments
3. Add new MCP server examples
4. Improve documentation
5. Share learning experiences

## 📄 License

This project is intended for educational purposes. Please refer to the FastMCP and MCP protocol licenses for production use.

## 🔍 Troubleshooting

### Common Issues

1. **Python Version**: Ensure you're using Python 3.13+
2. **Dependencies**: Run `uv install` or reinstall MCP CLI
3. **Server Not Starting**: Check that the server script path is correct
4. **Client Connection**: Verify MCP client configuration points to the correct script

### Getting Help

- Check the MCP specification for protocol details
- Review FastMCP documentation for implementation patterns
- Examine the server logs for error messages

---

**Happy Learning!** 🎓 This project provides a solid foundation for understanding MCP server development and integration with AI clients.