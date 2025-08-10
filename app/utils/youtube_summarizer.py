import app.core.config as config
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi 

YOUTUBE_API_KEY = config.YOUTUBE_API_KEY

def summarize_youtube_videos(product_prompt: str) -> str:
    """
    Summarizes YouTube videos for the given product.
    (Placeholder implementation)
    """

    # Step 1: Search YouTube
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    search_response = youtube.search().list(
        q=product_prompt + " review",
        part="id,snippet",
        maxResults=10,
        type="video"
    ).execute()

    video_data = []
    
    # Step 2: Get captions, descriptions, comments
    for item in search_response.get("items", []):
        video_id = item["id"]["videoId"]
        title = item["snippet"]["title"]
        description = item["snippet"]["description"]

        # Captions
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            captions_text = " ".join([t["text"] for t in transcript])
        except Exception:
            captions_text = ""

        # Comments
        comments_text = ""
        try:
            comments_response = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                textFormat="plainText",
                maxResults=50
            ).execute()
            for comment in comments_response.get("items", []):
                comments_text += comment["snippet"]["topLevelComment"]["snippet"]["textDisplay"] + " "
        except Exception:
            pass

        video_data.append({
            "video_id": video_id,
            "title": title,
            "description": description,
            "captions": captions_text,
            "comments": comments_text
        })
    # # TODO: Implement YouTube search and summarization logic
    # return "YouTube video summarization not implemented yet."
