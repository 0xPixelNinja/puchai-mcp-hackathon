from typing import Annotated
from pydantic import Field
from app.models.tool_models import RichToolDescription
from app.utils.fetch import Fetch
import base64
import os
from google import genai
from google.genai import types
import json

def product_analyzer_tool(mcp):
    ProductAnalyzerDescription = RichToolDescription(
        description="A powerful product analysis tool that can find, compare, and recommend products based on user requirements. It searches the web for relevant products, analyzes their specifications, prices, and reviews, and provides a structured JSON output.",
        use_when="Use this tool when the user wants to find a product that meets certain criteria (e.g., 'find a gaming laptop under $1500'), compare multiple products, or get a detailed recommendation for a specific type of product. This is the primary tool for any product-related queries.",
        side_effects="Performs a web search, analyzes multiple product pages, and returns a detailed JSON object containing product information, comparisons, and recommendations.",
    )

    @mcp.tool(description=ProductAnalyzerDescription.model_dump_json())
    async def product_analyzer(
        product_prompt: Annotated[str, Field(description="The user's detailed query about the product. This can include the product name, desired features, price range, or a comparison request. For example: 'best gaming headphones under $200 with noise cancellation' or 'compare iPhone 15 vs Samsung S24'.")],
    ) -> str:
        """
        Analyzes a product based on a user's prompt, gathers information, and provides a recommendation.
        """
        
        search_results = Fetch.search_web(product_prompt, num_results=10)
        
        if not search_results:
            return "Could not find any information about the product."

        client = genai.Client(
            api_key=os.environ.get("GEMINI_API_KEY"),
        )

        model = "gemini-2.5-flash"
        
        search_results_json = json.dumps(search_results, indent=2)

        final_prompt = f"""i have enabled your tool like google search grounding and url context, so please go trhough the links find out {product_prompt} and do the work and get me the products/s info in json format only very strict from the following search results:\n\n{search_results_json}, if the search_results_json is irrevalvent do the google search for the product and get the info and return the json format only very strict limt
         limit yourself to 2 products from the search results and do the work and get me the products/s info in json format only very strict """

        print(final_prompt)

        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(text=final_prompt),
                ],  
            ),
        ]
        tools = [
            types.Tool(url_context=types.UrlContext()),
        ]
        generate_content_config = types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(
                thinking_budget=-1,
            ),
            tools=tools,
        )

        response_chunks = []
        for chunk in client.models.generate_content_stream(
            model=model,
            contents=contents,
            config=generate_content_config,
        ):
            response_chunks.append(chunk.text)
            print(chunk.text)
        
        return "".join(response_chunks)

    return product_analyzer
