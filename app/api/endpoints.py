import os
from typing import Annotated
from pydantic import Field, AnyUrl
from mcp import ErrorData, McpError
from mcp.types import INVALID_PARAMS

from app.utils.helpers import RichToolDescription, Fetch
from app.core.prompt_analysis import understand_user_prompt
from app.core.recommendations import get_product_info, generate_recommendation
from app.services.web_search import search_product_reviews
from app.services.youtube import youtube_search_and_summarize

MY_NUMBER = os.environ.get("MY_NUMBER")

def register_tools(mcp):
    @mcp.tool
    async def validate() -> str:
        return MY_NUMBER

    ProductFinderDescription = RichToolDescription(
        description="Smart product tool: analyzes user queries to find, compare, or fact-check products.",
        use_when="Use this to get unbiased, user-centric product recommendations based on web search, reviews, and video summaries.",
        side_effects="Returns a detailed product recommendation based on real user feedback and expert analysis.",
    )

    @mcp.tool(description=ProductFinderDescription.model_dump_json())
    async def product_finder(
        user_goal: Annotated[str, Field(description="The user's freeform query about a product, e.g., 'find the best wireless headphones' or 'compare iPhone 15 vs Samsung S24'")],
        product_url: Annotated[AnyUrl | None, Field(description="A URL to a specific product page for analysis.")] = None,
        raw: Annotated[bool, Field(description="Return raw HTML content if True")] = False,
    ) -> str:
        """
        Handles user queries for product finding, comparison, and fact-checking.
        """
        intent = await understand_user_prompt(user_goal)

        if intent == "unknown" and not product_url:
            raise McpError(ErrorData(code=INVALID_PARAMS, message="Could not determine intent. Please provide a user_goal, e.g., 'find the best wireless headphones' or 'compare iPhone 15 vs Samsung S24'."))

        if product_url:
            content, _ = await Fetch.fetch_url(str(product_url), Fetch.USER_AGENT, force_raw=raw)
            return (
                f"🔗 **Fetched Product Page from URL**: {product_url}\n\n"
                f"---\n{content.strip()}\n---\n\n"
                f"User Goal: **{user_goal}**"
            )

        product_info = await get_product_info(user_goal)
        reviews = await search_product_reviews(user_goal, sites=["reddit.com", "twitter.com"])
        youtube_summary = await youtube_search_and_summarize(user_goal)
        recommendation = await generate_recommendation(product_info, reviews, youtube_summary)

        return recommendation
