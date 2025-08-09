import asyncio
import pprint
import json
from mcp_bearer_token.mcp_starter import Fetch

async def main():
    """
    Tests the youtube_search_and_summarize function by fetching and summarizing
    YouTube video reviews for a given product.
    """
    print("--- Testing youtube_search_and_summarize ---")
    
    query = "Sony WH-1000XM5 headphones"
    print(f"Fetching and summarizing YouTube reviews for: '{query}'")
    
    try:
        summary_json_str = await Fetch.youtube_search_and_summarize(query)
        print("\n--- Summary from YouTube reviews (JSON string) ---")
        pprint.pprint(summary_json_str)
    except Exception as e:
        print(f"\nAn error occurred during the test: {e}")

if __name__ == "__main__":
    # Ensure you have a .env file with your YOUTUBE_API_KEY and GEMINI_API_KEY.
    # This test makes live API calls to YouTube and Google Gemini.
    asyncio.run(main())