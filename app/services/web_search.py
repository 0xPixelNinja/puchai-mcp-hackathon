import httpx
from bs4 import BeautifulSoup

from app.utils.helpers import Fetch


async def search_product_reviews(query: str, sites: list[str], num_results: int = 5) -> list[str]:
    """
    Perform a scoped DuckDuckGo search for product reviews on specified sites.
    """
    # Placeholder for product review search logic
    return [f"https://www.reddit.com/r/demoreviews/comments/1", f"https://www.twitter.com/demoreviews/status/1"]


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

    soup = BeautifulSoup(resp.text, "html.parser")
    for a in soup.find_all("a", class_="result__a", href=True):
        href = a["href"]
        if "http" in href:
            links.append(href)
        if len(links) >= num_results:
            break

    return links or ["<error>No results found.</error>"]
