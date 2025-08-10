from typing import Annotated
from pydantic import Field
from app.models.tool_models import RichToolDescription
from app.utils.product_info_fetcher import get_product_info

def product_analyzer_tool(mcp):
    ProductAnalyzerDescription = RichToolDescription(
        description="A tool that finds product information based on user requirements. It searches the web for relevant products, analyzes their specifications and prices, and provides detailed information about the best matching product.",
        use_when="Use this tool when the user wants to find a product that meets certain criteria (e.g., 'find a gaming laptop under $1500'), or get detailed information about a specific product.",
        side_effects="Performs a web search, analyzes product pages, and returns detailed product information.",
    )

    @mcp.tool(description=ProductAnalyzerDescription.model_dump_json())
    async def product_analyzer(
        product_prompt: Annotated[str, Field(description="The user's detailed query about the product. This can include the product name, desired features, price range, or a comparison request. For example: 'best gaming headphones under $200 with noise cancellation' or 'compare iPhone 15 vs Samsung S24'.")],
    ) -> str:
        """
        Analyzes a product based on a user's prompt and gathers basic product information.
        """
        
        # Get Product Information
        product_info = get_product_info(product_prompt)
        print(product_info)

        # Generate Final Answer with product info only
        final_answer = f"""
        Product Information:
        {product_info}
        
        Note: If you'd like to see reviews of this product or YouTube video summaries, please ask in a follow-up question.
        """

        print(final_answer)

        return final_answer

    return product_analyzer
