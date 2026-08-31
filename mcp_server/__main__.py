"""
CLI entrypoint to run the MCP Server over stdio transport.
Usage:
    python -m mcp_server
"""
from mcp_server.server import mcp

def main():
    print("Starting AI Trip Planner MCP Server on stdio transport...", flush=True)
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()
