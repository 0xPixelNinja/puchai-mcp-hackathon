# Puchai MCP Hackathon

This project is a smart e-commerce assistant powered by a Model Context Protocol (MCP) server. It provides tools for comparing products and fact-checking product claims.

## Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/puchai-mcp-hackathon.git
   cd puchai-mcp-hackathon
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Server

To run the MCP server, use the following command:

```bash
uvicorn mcp_server.main:app --reload
```

The server will be available at `http://127.0.0.1:8000`.

## Interacting with the Server

You can interact with the server using any MCP-compliant client. The server exposes the following endpoints:

*   **GET /mcp**: Returns the MCP metadata, including the available tools.
*   **POST /mcp/tools/{tool_name}**: Executes a specific tool.

### Example: Comparing Products

To compare two products, send a POST request to `/mcp/tools/compare_product` with the following JSON payload:

```json
{
    "product_a": "iPhone 15",
    "product_b": "Samsung Galaxy S24"
}
```

### Example: Fact-Checking a Product

To fact-check a product, send a POST request to `/mcp/tools/fact_check_product` with the following JSON payload:

```json
{
    "product": "SuperJuice Blender",
    "claims": [
        "extracts 50% more juice",
        "quieter than a library"
    ]
}
```
