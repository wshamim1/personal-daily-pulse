"""Medium platform tools for fetching trending stories."""

from langchain.tools import tool
from .utils import fetch_xml, parse_rss


@tool
def get_medium_trending():
    """Fetch trending stories from Medium."""
    try:
        url = "https://medium.com/feed/tag/trending"
        xml = fetch_xml(url)
        items = parse_rss(xml)
        
        # Return array of items for frontend compatibility
        return items[:10]  # Return top 10 stories as array
    except Exception as e:
        return []
