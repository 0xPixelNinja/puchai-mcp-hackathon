import asyncio
from mcp_bearer_token.mcp_starter import Fetch

async def test_search_product_reviews():
    query = "best wireless headphones"
    sites = ["reddit.com"]
    results = await Fetch.search_product_reviews(query, sites, num_results=2)
    print("Results:", results)

if __name__ == "__main__":
    asyncio.run(test_search_product_reviews())
    