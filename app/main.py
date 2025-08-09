import asyncio
from fastmcp import FastMCP
from app.core.auth import SimpleBearerAuthProvider
from app.core.config import TOKEN
from app.tools.validate import validate_tool
from app.tools.archives.job_finder import job_finder_tool
from app.tools.archives.image_tool import image_tool
from app.tools.product_analyzer import product_analyzer_tool

# --- MCP Server Setup ---
mcp = FastMCP(
    "Job Finder MCP Server",
    auth=SimpleBearerAuthProvider(TOKEN),
)

# --- Register Tools ---
validate_tool(mcp)
#job_finder_tool(mcp)
#image_tool(mcp)
product_analyzer_tool(mcp)

# --- Run MCP Server ---
async def main():
    print("🚀 Starting MCP server on http://0.0.0.0:8086")
    await mcp.run_async("streamable-http", host="0.0.0.0", port=8086)

if __name__ == "__main__":
    asyncio.run(main())
