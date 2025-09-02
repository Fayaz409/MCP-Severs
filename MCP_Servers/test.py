# server.py
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Demo Server")

# --- Tool: add two numbers ---
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two integers and return the sum."""
    return a + b

# --- Resource: simple health/status ---
@mcp.resource("status://health")
def health() -> str:
    """Return a simple health report (string or JSON)."""
    return '{"ok": true, "service": "demo", "version": "1.0.0"}'

# --- Prompt: reusable template ---
@mcp.prompt()
def greet_user(name: str, style: str = "friendly") -> str:
    """Create a greeting template the model can fill in/use."""
    styles = {
        "friendly": "Write a warm, friendly greeting",
        "formal":   "Write a formal, professional greeting",
        "casual":   "Write a casual, relaxed greeting"
    }
    return f"""{styles.get(style, styles["friendly"])} for someone named {name}.
Keep it concise, and include a short well-wish."""

if __name__ == "__main__":
    # When run directly, FastMCP will negotiate protocol over stdio.
    # Most clients (Inspector, Claude Desktop) will launch this file as a subprocess.
    mcp.run_stdio()
