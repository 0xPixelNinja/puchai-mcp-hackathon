from typing import Annotated
from pydantic import Field
from app.models.tool_models import RichToolDescription
from app.utils.youtube_summarizer import summarize_youtube_videos

def youtube_summarizer_tool(mcp):
    YouTubeSummarizerDescription = RichToolDescription(
        description="A tool that summarizes YouTube videos related to a specific product or topic. It searches YouTube for relevant videos and provides summaries of their content.",
        use_when="Use this tool when the user wants to get insights from YouTube videos about a specific product or topic. For example, 'What do YouTubers say about the new iPhone 15?' or 'I want YouTube video summaries about Sony WH-1000XM5 headphones.'",
        side_effects="Performs a YouTube search, analyzes video content, and returns summaries of relevant videos.",
    )

    @mcp.tool(description=YouTubeSummarizerDescription.model_dump_json())
    async def youtube_summarizer(
        topic: Annotated[str, Field(description="The product or topic to search for on YouTube. This should be specific enough to find relevant videos. For example: 'iPhone 15 Pro review' or 'Sony WH-1000XM5 headphones'.")],
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
