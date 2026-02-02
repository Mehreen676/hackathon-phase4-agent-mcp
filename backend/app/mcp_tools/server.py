from mcp.server.fastmcp import FastMCP
from app.mcp_tools.tools import register_tools

mcp = FastMCP("todo-mcp-server")

register_tools(mcp)

if __name__ == "__main__":
    mcp.run()
