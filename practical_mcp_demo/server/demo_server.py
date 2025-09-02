#!/usr/bin/env python3
"""
Simple MCP Server Demo
A practical example showing how MCP servers work with various tools and resources.
"""

from mcp.server.fastmcp import FastMCP
import json
import os
import datetime

# Create the MCP server
mcp = FastMCP("Practical Demo Server")

# Simple data store for demonstration
demo_data = {
    "users": [
        {"id": 1, "name": "Alice", "email": "alice@example.com"},
        {"id": 2, "name": "Bob", "email": "bob@example.com"}
    ],
    "counter": 0
}

# Tool 1: Calculator functions
@mcp.tool()
def calculate(operation: str, a: float, b: float) -> float:
    """Perform basic arithmetic operations.
    
    Args:
        operation: The operation to perform (add, subtract, multiply, divide)
        a: First number
        b: Second number
    
    Returns:
        The result of the calculation
    """
    operations = {
        "add": lambda x, y: x + y,
        "subtract": lambda x, y: x - y,
        "multiply": lambda x, y: x * y,
        "divide": lambda x, y: x / y if y != 0 else float('inf')
    }
    
    if operation not in operations:
        raise ValueError(f"Unknown operation: {operation}")
    
    return operations[operation](a, b)

# Tool 2: Text utilities
@mcp.tool()
def text_transform(text: str, transformation: str) -> str:
    """Transform text in various ways.
    
    Args:
        text: The text to transform
        transformation: Type of transformation (upper, lower, reverse, count_words)
    
    Returns:
        The transformed text or count
    """
    transformations = {
        "upper": lambda t: t.upper(),
        "lower": lambda t: t.lower(),
        "reverse": lambda t: t[::-1],
        "count_words": lambda t: str(len(t.split())),
        "title": lambda t: t.title()
    }
    
    if transformation not in transformations:
        raise ValueError(f"Unknown transformation: {transformation}")
    
    return transformations[transformation](text)

# Tool 3: Counter management
@mcp.tool()
def manage_counter(action: str, amount: int = 1) -> int:
    """Manage a simple counter.
    
    Args:
        action: Action to perform (increment, decrement, reset, get)
        amount: Amount to increment/decrement by (default: 1)
    
    Returns:
        Current counter value
    """
    global demo_data
    
    if action == "increment":
        demo_data["counter"] += amount
    elif action == "decrement":
        demo_data["counter"] -= amount
    elif action == "reset":
        demo_data["counter"] = 0
    elif action == "get":
        pass  # Just return current value
    else:
        raise ValueError(f"Unknown action: {action}")
    
    return demo_data["counter"]

# Tool 4: File operations
@mcp.tool()
def file_info(file_path: str) -> str:
    """Get information about a file.
    
    Args:
        file_path: Path to the file
    
    Returns:
        JSON string with file information
    """
    try:
        stat = os.stat(file_path)
        info = {
            "exists": True,
            "size_bytes": stat.st_size,
            "modified_time": datetime.datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "is_directory": os.path.isdir(file_path),
            "is_file": os.path.isfile(file_path)
        }
    except FileNotFoundError:
        info = {"exists": False}
    except Exception as e:
        info = {"error": str(e)}
    
    return json.dumps(info, indent=2)

# Resource 1: Server status
@mcp.resource("status://server")
def server_status() -> str:
    """Return current server status and statistics."""
    status = {
        "status": "running",
        "timestamp": datetime.datetime.now().isoformat(),
        "demo_data": demo_data,
        "tools_available": ["calculate", "text_transform", "manage_counter", "file_info"],
        "resources_available": ["status://server", "data://users"],
        "uptime": "N/A (demo)"
    }
    return json.dumps(status, indent=2)

# Resource 2: User data
@mcp.resource("data://users")
def get_users() -> str:
    """Return the list of demo users."""
    return json.dumps(demo_data["users"], indent=2)

# Prompt 1: Code generator
@mcp.prompt()
def generate_code(language: str, task: str, style: str = "simple") -> str:
    """Generate code snippet prompts.
    
    Args:
        language: Programming language (python, javascript, etc.)
        task: What the code should do
        style: Code style preference (simple, advanced, commented)
    """
    styles = {
        "simple": "Write simple, clean code",
        "advanced": "Write advanced, optimized code with best practices",
        "commented": "Write well-commented code with explanations"
    }
    
    style_instruction = styles.get(style, styles["simple"])
    
    return f"""Please write a {language} code snippet that {task}.

Requirements:
- {style_instruction}
- Follow {language} conventions
- Include error handling where appropriate
- Make it production-ready

Task: {task}"""

# Prompt 2: Email template
@mcp.prompt()
def email_template(type: str, recipient_name: str, context: str = "") -> str:
    """Generate email templates.
    
    Args:
        type: Type of email (welcome, reminder, thank_you, support)
        recipient_name: Name of the recipient
        context: Additional context for the email
    """
    templates = {
        "welcome": "Create a warm welcome email",
        "reminder": "Write a polite reminder email",
        "thank_you": "Compose a sincere thank you email",
        "support": "Draft a helpful support response email"
    }
    
    template_instruction = templates.get(type, "Write a professional email")
    
    prompt = f"""{template_instruction} for {recipient_name}.

Email type: {type}
Recipient: {recipient_name}"""
    
    if context:
        prompt += f"\nContext: {context}"
    
    prompt += """

Please write a professional email that is:
- Appropriate for the context
- Clear and concise
- Properly formatted
- Engaging and helpful"""
    
    return prompt

if __name__ == "__main__":
    print("Starting Practical MCP Demo Server...")
    print("Available tools: calculate, text_transform, manage_counter, file_info")
    print("Available resources: status://server, data://users")
    print("Available prompts: generate_code, email_template")
    print("\nServer running on stdio...")
    mcp.run()