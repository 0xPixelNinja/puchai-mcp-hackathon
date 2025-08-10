import app.core.config as config
import json
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi 

YOUTUBE_API_KEY = config.YOUTUBE_API_KEY

def summarize_youtube_videos(product_prompt: str) -> str:
    """
    Summarizes YouTube videos for the given product.
    """

    # Step 1: Search YouTube
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    search_response = youtube.search().list(
        q=product_prompt + " review",
        part="id,snippet",
        maxResults=5,  # Reduced to 5 for performance
        type="video"
    ).execute()

    video_data = []
    
    # Step 2: Get captions, descriptions, comments
    for item in search_response.get("items", []):
        video_id = item["id"]["videoId"]
        title = item["snippet"]["title"]
        description = item["snippet"]["description"]
        video_url = f"https://www.youtube.com/watch?v={video_id}"

        # Captions
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            captions_text = " ".join([t["text"] for t in transcript])[:1000]  # Limit caption text size
        except Exception:
            captions_text = "Transcript not available"

        # Comments (limiting to avoid too much data)
        comments_text = ""
        try:
            comments_response = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                textFormat="plainText",
                maxResults=5  # Reduced for performance
            ).execute()
            for comment in comments_response.get("items", []):
                comment_text = comment["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
                comments_text += comment_text[:200] + "... "  # Limit comment size
        except Exception:
            comments_text = "Comments not available"

        video_data.append({
            "video_id": video_id,
            "url": video_url,
            "title": title,
            "captions_text": captions_text,
            "description": description[:500],  # Limit description size
            "top_comments": comments_text
        })
    
    # Format the response
    if not video_data:
        return "No YouTube videos found for this product."
    
    formatted_result = json.dumps(video_data, indent=2)
    return formatted_result
