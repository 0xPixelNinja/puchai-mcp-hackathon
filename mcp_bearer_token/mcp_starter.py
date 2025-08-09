import asyncio
from typing import Annotated
import os
from dotenv import load_dotenv
from fastmcp import FastMCP
from fastmcp.server.auth.providers.bearer import BearerAuthProvider, RSAKeyPair
from mcp import ErrorData, McpError
from mcp.server.auth.provider import AccessToken
from mcp.types import TextContent, ImageContent, INVALID_PARAMS, INTERNAL_ERROR
from pydantic import BaseModel, Field, AnyUrl
from bs4 import BeautifulSoup
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi 

import praw
import markdownify
import httpx
import readabilipy
import google.generativeai as genai
import json

# --- Load environment variables ---
load_dotenv()

TOKEN = os.environ.get("AUTH_TOKEN")
MY_NUMBER = os.environ.get("MY_NUMBER")
REDDIT_CLIENT_ID = os.environ.get("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.environ.get("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.environ.get("REDDIT_USER_AGENT", "PuchAI/1.0")


assert TOKEN is not None, "Please set AUTH_TOKEN in your .env file"
assert MY_NUMBER is not None, "Please set MY_NUMBER in your .env file"
assert REDDIT_CLIENT_ID is not None, "Please set REDDIT_CLIENT_ID in your .env file"
assert REDDIT_CLIENT_SECRET is not None, "Please set REDDIT_CLIENT_SECRET in your .env file"

# - - - Reddit API Setup ---
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT,
)

# --- Auth Provider ---
class SimpleBearerAuthProvider(BearerAuthProvider):
    def __init__(self, token: str):
        k = RSAKeyPair.generate()
        super().__init__(public_key=k.public_key, jwks_uri=None, issuer=None, audience=None)
        self.token = token

    async def load_access_token(self, token: str) -> AccessToken | None:
        if token == self.token:
            return AccessToken(
                token=token,
                client_id="puch-client",
                scopes=["*"],
                expires_at=None,
            )
        return None

# --- Rich Tool Description model ---
class RichToolDescription(BaseModel):
    description: str
    use_when: str
    side_effects: str | None = None

# --- Fetch Utility Class ---
class Fetch:
    USER_AGENT = "Puch/1.0 (Autonomous)"

    @classmethod
    async def fetch_url(
        cls,
        url: str,
        user_agent: str,
        force_raw: bool = False,
    ) -> tuple[str, str]:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    url,
                    follow_redirects=True,
                    headers={"User-Agent": user_agent},
                    timeout=30,
                )
            except httpx.HTTPError as e:
                raise McpError(ErrorData(code=INTERNAL_ERROR, message=f"Failed to fetch {url}: {e!r}"))

            if response.status_code >= 400:
                raise McpError(ErrorData(code=INTERNAL_ERROR, message=f"Failed to fetch {url} - status code {response.status_code}"))

            page_raw = response.text

        content_type = response.headers.get("content-type", "")
        is_page_html = "text/html" in content_type

        if is_page_html and not force_raw:
            return cls.extract_content_from_html(page_raw), ""

        return (
            page_raw,
            f"Content type {content_type} cannot be simplified to markdown, but here is the raw content:\n",
        )

    @staticmethod
    def extract_content_from_html(html: str) -> str:
        """Extract and convert HTML content to Markdown format."""
        ret = readabilipy.simple_json.simple_json_from_html_string(html, use_readability=True)
        if not ret or not ret.get("content"):
            return "<error>Page failed to be simplified from HTML</error>"
        content = markdownify.markdownify(ret["content"], heading_style=markdownify.ATX)
        return content

    @staticmethod
    async def understand_user_prompt(prompt: str) -> str:
        """
        Understand the user's prompt and determine the intent.
        """
        if "compare" in prompt.lower():
            return "compare_product"
        elif "fact-check" in prompt.lower():
            return "fact_check_product"
        elif "find" in prompt.lower():
            return "find_product"
        else:
            return "unknown"

    @staticmethod
    async def get_product_info(query: str) -> dict:
        """
        Get product information based on the query.
        """
        return {"product_name": "XM5 6000", "price": "$100", "features": ["Feature A", "Feature B"]}

    @staticmethod
    async def search_product_reviews(query: str, sites: list[str], num_results: int = 5) -> list[dict]:
        """
        Search Reddit for product reviews using Reddit API, fetch top posts and comments, summarize via Gemini API, and return JSON.
        """
        # Step 1: Use Reddit API to search for relevant posts
        posts_data = []
        try:
            for submission in reddit.subreddit("all").search(query, sort="relevance", limit=num_results):
                comments = []
                submission.comments.replace_more(limit=0)
                for top_comment in submission.comments[:5]:
                    comments.append(top_comment.body)
                posts_data.append({
                    "url": f"https://www.reddit.com{submission.permalink}",
                    "title": submission.title,
                    "description": submission.selftext,
                    "comments": comments
                })
        except Exception as e:
            return [{"error": f"Reddit API error: {e}"}]

        # Step 2: Summarize using Gemini API
        summaries = []
        for post in posts_data:
            prompt = (
                f"Summarize the following Reddit product review post and its comments in JSON format with pros, cons, and main points:\n"
                f"Title: {post['title']}\n"
                f"Description: {post['description']}\n"
                f"Comments: {json.dumps(post['comments'])}\n"
            )
            try:
                genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content(prompt)
                summaries.append({
                    "url": post["url"],
                    "summary_json": response.text
                })
            except Exception as e:
                summaries.append({
                    "url": post["url"],
                    "summary_json": f"Error summarizing: {e}"
                })

        return summaries

    
    @staticmethod
    async def youtube_search_and_summarize(query: str) -> str:
        """
        Search for a YouTube video and return a summary.
        """
        # Placeholder for YouTube search and summarization logic
        return "This is a summary of a YouTube video about the product."
        
    @staticmethod
    async def generate_recommendation(product_info: dict, reviews: list[str], youtube_summary: str) -> str:
        """
        Generate a final product recommendation based on the gathered information.
        """
        # Placeholder for recommendation generation logic
        return f"Based on the information gathered, we recommend the {product_info['product_name']}."

    @staticmethod
    async def web_search(query: str, num_results: int = 5) -> list[str]:
        """
        Perform a scoped DuckDuckGo search and return a list of job posting URLs.
        (Using DuckDuckGo because Google blocks most programmatic scraping.)
        """
        ddg_url = f"https://html.duckduckgo.com/html/?q={query.replace(' ', '+')}"
        links = []

        async with httpx.AsyncClient() as client:
            resp = await client.get(ddg_url, headers={"User-Agent": Fetch.USER_AGENT})
            if resp.status_code != 200:
                return ["<error>Failed to perform search.</error>"]

        from bs4 import BeautifulSoup
        soup = BeautifulSoup(resp.text, "html.parser")
        for a in soup.find_all("a", class_="result__a", href=True):
            href = a["href"]
            if "http" in href:
                links.append(href)
            if len(links) >= num_results:
                break

        return links or ["<error>No results found.</error>"]

# --- MCP Server Setup ---
mcp = FastMCP(
    "E-commerce Product Finder MCP Server",
    auth=SimpleBearerAuthProvider(TOKEN),
)

# --- Tool: validate (required by Puch) ---
@mcp.tool
async def validate() -> str:
    return MY_NUMBER

# --- Tool: product_finder ---
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
    intent = await Fetch.understand_user_prompt(user_goal)

    if intent == "unknown" and not product_url:
        raise McpError(ErrorData(code=INVALID_PARAMS, message="Could not determine intent. Please provide a user_goal, e.g., 'find the best wireless headphones' or 'compare iPhone 15 vs Samsung S24'."))

    if product_url:
        content, _ = await Fetch.fetch_url(str(product_url), Fetch.USER_AGENT, force_raw=raw)
        return (
            f"🔗 **Fetched Product Page from URL**: {product_url}\n\n"
            f"---\n{content.strip()}\n---\n\n"
            f"User Goal: **{user_goal}**"
        )

    product_info = await Fetch.get_product_info(user_goal)
    reviews = await Fetch.search_product_reviews(user_goal, sites=["reddit.com", "twitter.com"])
    youtube_summary = await Fetch.youtube_search_and_summarize(user_goal)
    recommendation = await Fetch.generate_recommendation(product_info, reviews, youtube_summary)

    return recommendation

# --- Run MCP Server ---
async def main():
    print("🚀 Starting MCP server on http://0.0.0.0:8086")
    await mcp.run_async("streamable-http", host="0.0.0.0", port=8086)

if __name__ == "__main__":
    asyncio.run(main())
