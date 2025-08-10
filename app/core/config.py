import os
from dotenv import load_dotenv

# --- Load environment variables ---
load_dotenv()

TOKEN = os.environ.get("AUTH_TOKEN")
MY_NUMBER = os.environ.get("MY_NUMBER")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
REDDIT_CLIENT_ID = os.environ.get("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.environ.get("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.environ.get("REDDIT_USER_AGENT", "PuchAI/1.0")
YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY")

assert TOKEN is not None, "Please set AUTH_TOKEN in your .env file"
assert MY_NUMBER is not None, "Please set MY_NUMBER in your .env file"
assert GEMINI_API_KEY is not None, "Please set GEMINI_API_KEY in your .env file"
assert REDDIT_CLIENT_ID is not None, "Please set REDDIT_CLIENT_ID in your .env file"
assert REDDIT_CLIENT_SECRET is not None, "Please set REDDIT_CLIENT_SECRET in your .env file"
assert YOUTUBE_API_KEY is not None, "Please set YOUTUBE_API_KEY in your .env file"