from fastapi import FastAPI, Request, Response, HTTPException
from typing import List, Dict, Any, Optional
from . import tools

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/mcp")
async def mcp_metadata(request: Request) -> Dict[str, Any]:
    return {
        "name": "puchai-mcp-hackathon",
        "version": "0.1.0",
        "description": "A smart e-commerce assistant.",
        "tools": [
            {
                "name": "compare_product",
                "description": "Compares two products and returns a recommendation.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "product_a": {"type": "string"},
                        "product_b": {"type": "string"},
                    },
                    "required": ["product_a", "product_b"],
                },
            },
            {
                "name": "fact_check_product",
                "description": "Fact-checks a list of claims about a product.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "product": {"type": "string"},
                        "claims": {"type": "array", "items": {"type": "string"}},
                    },
                    "required": ["product", "claims"],
                },
            }
        ],
        "resources": [],
        "prompts": [],
    }

@app.post("/mcp/tools/{tool_name}")
async def execute_tool(tool_name: str, request: Request):
    tool_function = getattr(tools, tool_name, None)

    if not tool_function:
        raise HTTPException(status_code=404, detail=f"Tool '{tool_name}' not found.")

    try:
        body = await request.json()
        result = tool_function(**body)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

