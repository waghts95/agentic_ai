from mcp.server.fastmcp import FastMCP

mcp = FastMCP("SimpleCalculator")

@mcp.tool()
def add_numbers(a: int, b: int) -> int:
    """Add two integer numbers and return the sum."""
    return a + b

if __name__ == "__main__":
    print("Starting MCP Server on http://localhost:8000")
    mcp.run(transport="sse")