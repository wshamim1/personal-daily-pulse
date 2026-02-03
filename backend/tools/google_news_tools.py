"""Google News tools for fetching top news stories."""

from langchain.tools import tool
from .utils import fetch_xml, parse_rss
from typing import Optional


@tool
def get_google_news(topic: Optional[str] = None, country: str = "US", lang: str = "en"):
    """Fetch Google News RSS for trending news.
    
    Args:
        topic: News topic (WORLD, NATION, BUSINESS, TECHNOLOGY, ENTERTAINMENT, SPORTS, SCIENCE, HEALTH). If not provided, gets top news.
        country: Country code (US, GB, IN, etc.)
        lang: Language code (en, es, fr, etc.)
    
    Returns:
        Array of news items with title, link, and pubDate
    """
    try:
        if topic and topic.upper() in {"WORLD", "NATION", "BUSINESS", "TECHNOLOGY", "ENTERTAINMENT", "SPORTS", "SCIENCE", "HEALTH"}:
            url = f"https://news.google.com/rss/topics/{topic.upper()}?hl={lang}&gl={country}&ceid={country}:{lang}"
        else:
            url = f"https://news.google.com/rss?hl={lang}&gl={country}&ceid={country}:{lang}"
        
        xml = fetch_xml(url)
        items = parse_rss(xml)
        
        # Return array of items for frontend compatibility
        return items[:10]
    except Exception as e:
        return []
