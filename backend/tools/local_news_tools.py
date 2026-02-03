"""Local news tools for fetching regional news stories."""

from langchain.tools import tool
from .utils import fetch_xml, parse_rss


@tool
def get_local_news():
    """Fetch local news stories."""
    try:
        url = "https://news.google.com/rss?hl=en&gl=US&ceid=US:en"
        xml = fetch_xml(url)
        items = parse_rss(xml)
        
        # Return array of items for frontend compatibility
        return items[:10]
    except Exception as e:
        return []
