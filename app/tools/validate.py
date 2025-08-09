from app.core.config import MY_NUMBER

def validate_tool(mcp):
    @mcp.tool
    async def validate() -> str:
        return MY_NUMBER
    return validate
