import praw
import app.core.config as config

REDDIT_CLIENT_ID = config.REDDIT_CLIENT_ID
REDDIT_CLIENT_SECRET = config.REDDIT_CLIENT_SECRET
REDDIT_USER_AGENT = config.REDDIT_USER_AGENT

reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT,
)

def analyze_reviews(product_info: str) -> list:
    """
    Analyzes reviews for the given product.
    Returns a list of dictionaries containing Reddit posts related to the product.
    """
    posts_data = []
    try:
        for submission in reddit.subreddit("all").search(product_info, sort="relevance", limit=5):
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
        return posts_data
    except Exception as e:
        return [{"error": f"Reddit API error: {e}"}]
    
    # # TODO: Implement additional review analysis logic if needed

