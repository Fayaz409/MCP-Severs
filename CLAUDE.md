# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an MCP (Model Context Protocol) learning repository that demonstrates how to build MCP servers using Python and the fastmcp library. The project includes:

- A main Python application (`main.py`) with a simple hello world function
- An MCP server implementation in `MCP_Servers/test.py` that showcases tools, resources, and prompts
- Uses `uv` for dependency management with Python 3.13+

## Architecture

The MCP server (`MCP_Servers/test.py`) implements three key MCP concepts:
1. **Tools**: Functions that can be called by the client (e.g., `add()` function for arithmetic)
2. **Resources**: Data endpoints that can be accessed (e.g., health status endpoint)
3. **Prompts**: Reusable templates for AI interactions (e.g., greeting generator)

## Common Commands

### Running the MCP Server
```bash
mcp dev MCP_Servers/test.py
```

### Installing Dependencies
```bash
# Using uv (preferred)
uv install

# Or using pip
python3 -m pip install "mcp[cli]"
```

### Running the Main Application
```bash
python main.py
```

## Development Environment

- Python version: 3.13+ (specified in `.python-version`)
- Package manager: `uv` (uses `uv.lock` for reproducible builds)
- Dependencies managed in `pyproject.toml`
- Virtual environment in `.venv/`

## MCP Server Development

When developing MCP servers:
- Use the `@mcp.tool()` decorator for callable functions
- Use `@mcp.resource("uri://path")` for data endpoints
- Use `@mcp.prompt()` for reusable AI templates
- Always call `mcp.run_stdio()` in the `if __name__ == "__main__"` block for proper protocol negotiation