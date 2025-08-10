import praw
import app.core.config as config
import json

REDDIT_CLIENT_ID = config.REDDIT_CLIENT_ID
REDDIT_CLIENT_SECRET = config.REDDIT_CLIENT_SECRET
REDDIT_USER_AGENT = config.REDDIT_USER_AGENT

reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT,
)

def analyze_reviews(product_info: str) -> str:
    """
    Analyzes reviews for the given product.
    Returns a formatted string of Reddit posts related to the product.
    """
    posts_data = []
    try:
        for submission in reddit.subreddit("all").search(product_info, sort="relevance", limit=5):
            comments = []
            submission.comments.replace_more(limit=0)
            for top_comment in submission.comments[:3]:  # Reduced to 3 comments per post
                # Limit comment length to avoid overwhelming responses
                comment_text = top_comment.body
                if len(comment_text) > 300:
                    comment_text = comment_text[:300] + "..."
                comments.append(comment_text)
            
            # Limit post description length
            description = submission.selftext
            if len(description) > 500:
                description = description[:500] + "..."
                
            posts_data.append({
                "url": f"https://www.reddit.com{submission.permalink}",
                "title": submission.title,
                "description": description,
                "comments": comments
            })
        
        if not posts_data:
            return "No Reddit discussions found for this product."
        
        # Format as JSON string for better readability
        return json.dumps(posts_data, indent=2)
        
    except Exception as e:
        return json.dumps([{"error": f"Reddit API error: {e}"}], indent=2)

