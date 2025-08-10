import os
import json
from google import genai
from google.genai import types
from app.utils.fetch import Fetch

def get_product_info(product_prompt: str) -> str:
    """
    Fetches product information based on a user's prompt.
    """
    search_results = Fetch.search_web(product_prompt, num_results=6)
    
    if not search_results:
        return "Could not find any information about the product."

    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    model = "gemini-2.5-flash"
    
    search_results_json = json.dumps(search_results, indent=2)

    final_prompt = f"""Please analyze the following search results to find the single best product that matches the user's query: '{product_prompt}'.
Your task is to return a single, comprehensive JSON object containing all available specifications and data for the best product.
The JSON object should be complete and well-structured, including all relevant details such as brand, model, price, features, and technical specifications.

Here are the search results with the urls and the titles:
{search_results_json}

If the provided search results are insufficient or irrelevant, you must perform your own Google search to find the necessary information.
Your final output must be only the JSON object for the single best product, without any additional text or explanation. It is very important to only return the JSON object and nothing else.
If you cannot find a suitable product, return an empty JSON object: {{}}.
"""

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
        types.Tool(google_search=types.GoogleSearch()),
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
