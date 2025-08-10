from typing import Annotated
from pydantic import Field
from app.models.tool_models import RichToolDescription
from app.utils.review_analyzer import analyze_reviews

def review_analyzer_tool(mcp):
    ReviewAnalyzerDescription = RichToolDescription(
        description="A tool that analyzes reviews and discussions about a specific product from Reddit. It searches for relevant posts and comments to provide insights into user experiences and opinions.",
        use_when="Use this tool when the user wants to know what people are saying about a specific product or topic on Reddit. For example, 'What do people think about the Sony WH-1000XM5?' or 'Show me reviews for the MacBook Pro M3'.",
        side_effects="Searches Reddit for relevant posts and comments, and returns a summary of user opinions.",
    )

    @mcp.tool(description=ReviewAnalyzerDescription.model_dump_json())
    async def review_analyzer(
        product: Annotated[str, Field(description="The product or topic to search for reviews on Reddit. This should be specific enough to find relevant discussions. For example: 'iPhone 15 Pro reviews' or 'Sony WH-1000XM5 opinions'.")],
    ) -> str:
        """
        Analyzes Reddit reviews and discussions about a specific product.
        """
        
        # Get Product Reviews from Reddit
        product_reviews = analyze_reviews(product)
        print(product_reviews)

        # Generate Final Answer
        final_answer = f"""
        Reddit Discussions about {product}:
        {product_reviews}
        """

        print(final_answer)

        return final_answer

    return review_analyzer
