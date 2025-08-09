from typing import Annotated
from pydantic import Field
from app.models.tool_models import RichToolDescription
from app.utils.product_info_fetcher import get_product_info
from app.utils.review_analyzer import analyze_reviews
from app.utils.youtube_summarizer import summarize_youtube_videos

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
        
        # 1. Get Product Information
        product_info = get_product_info(product_prompt)

        # 2. Get Product Reviews
        product_reviews = analyze_reviews(product_info)

        # 3. Get YouTube Video Summaries
        youtube_summaries = summarize_youtube_videos(product_info)

        # 4. Generate Final Answer
        final_answer = f"""
        Product Information:
        {product_info}

        Product Reviews:
        {product_reviews}

        YouTube Summaries:
        {youtube_summaries}
        """

        return final_answer

    return product_analyzer
