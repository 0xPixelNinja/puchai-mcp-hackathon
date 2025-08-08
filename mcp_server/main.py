from fastapi import FastAPI, Request, Response
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

