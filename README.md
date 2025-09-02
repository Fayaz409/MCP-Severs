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
├── main.py                 # Simple Python application entry point
├── MCP_Servers/
│   └── test.py            # MCP server implementation with examples
├── pyproject.toml         # Project configuration and dependencies
├── uv.lock               # Locked dependencies for reproducible builds
├── .python-version       # Python version specification (3.13+)
└── README.md             # This file
```

## 🛠 Features

This MCP server implementation showcases three core MCP concepts:

### 1. **Tools** - Callable Functions
- `add(a, b)`: Demonstrates basic arithmetic operations
- Tools can be invoked by AI clients to perform computations

### 2. **Resources** - Data Endpoints
- `status://health`: Provides server health and status information
- Resources offer structured data access for AI clients

### 3. **Prompts** - Reusable Templates
- `greet_user(name, style)`: Creates customizable greeting templates
- Supports multiple styles: friendly, formal, casual
- Helps AI models generate consistent, contextual responses

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

### Running the MCP Server

To start the MCP server in development mode:

```bash
# Navigate to the project directory
cd MCP_Learn

# Run the server in development mode
mcp dev MCP_Servers/test.py
```

The server will start and listen for MCP protocol communications over stdio, making it ready to integrate with MCP clients.

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

Add to your Claude Desktop configuration:

```json
{
  "mcpServers": {
    "mcp-learn": {
      "command": "python",
      "args": ["path/to/MCP_Learn/MCP_Servers/test.py"]
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