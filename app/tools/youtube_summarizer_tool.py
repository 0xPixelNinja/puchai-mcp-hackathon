from typing import Annotated
from pydantic import Field
from app.models.tool_models import RichToolDescription
from app.utils.youtube_summarizer import summarize_youtube_videos

def youtube_summarizer_tool(mcp):
    YouTubeSummarizerDescription = RichToolDescription(
        description="A tool that summarizes YouTube videos related to a specific product, topic, or a direct YouTube link. It searches YouTube for relevant review videos or a given video link and provides summaries of their content.",
        use_when="Use this tool when the user wants to get insights from YouTube videos about a specific product, topic or when they provide a YouTube link to summarize directly. For example, 'I want YouTube video summaries about Sony WH-1000XM5 headphones.' or 'What are the reviews of the new iPhone15 in this YouTube video: https://youtu.be/abc123'",
        side_effects="Performs a YouTube search for reviews (if given a product/topic) or fetches details from a specific video link. Extracts transcripts, descriptions, and top comments, then returns summaries of relevant videos.",
    )

    @mcp.tool(description=YouTubeSummarizerDescription.model_dump_json())
    async def youtube_summarizer(
        topic: Annotated[str, Field(description="The product, topic or link to search for on YouTube. This should be specific enough to find relevant videos. For example: 'iPhone 15 Pro review' or 'Sony WH-1000XM5 headphones'.")],
    ) -> str:
        """
        Summarizes YouTube videos related to a specific product or topic.
        """
        
        # Get YouTube Video Summaries
        youtube_summaries = summarize_youtube_videos(topic)
        print(youtube_summaries)

        # Generate Final Answer
        final_answer = f"""
        YouTube Video Summaries about {topic}:
        {youtube_summaries}
        """

        print(final_answer)

        return final_answer

    return youtube_summarizer
