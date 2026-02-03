"""News tools for fetching trending news and stories."""

from langchain.tools import tool
from .utils import fetch_xml, fetch_json, parse_rss
from typing import Optional
import urllib.parse
import os


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


@tool
def get_local_news(location: Optional[str] = None, country: str = "US", lang: str = "en"):
    """Fetch local news stories by location keyword search.
    
    Args:
        location: Location keyword (city/state). Defaults to DEFAULT_LOCATION env.
        country: Country code (US, GB, IN, etc.)
        lang: Language code (en, es, fr, etc.)
    """
    try:
        location_query = location or os.getenv("DEFAULT_LOCATION", "New York, NY")
        query = urllib.parse.quote(location_query)
        url = f"https://news.google.com/rss/search?q={query}&hl={lang}&gl={country}&ceid={country}:{lang}"
        xml = fetch_xml(url)
        items = parse_rss(xml)
        return items[:10]
    except Exception as e:
        return []


@tool
def get_country_news(country: str = "US", lang: str = "en"):
    """Fetch country-specific national news (NATION topic)."""
    try:
        url = f"https://news.google.com/rss/topics/NATION?hl={lang}&gl={country}&ceid={country}:{lang}"
        xml = fetch_xml(url)
        items = parse_rss(xml)
        return items[:10]
    except Exception as e:
        return []


@tool
def get_international_news(lang: str = "en", country: str = "US"):
    """Fetch international/world news (WORLD topic)."""
    try:
        url = f"https://news.google.com/rss/topics/WORLD?hl={lang}&gl={country}&ceid={country}:{lang}"
        xml = fetch_xml(url)
        items = parse_rss(xml)
        return items[:10]
    except Exception as e:
        return []


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


@tool
def get_devto_trending(tag: Optional[str] = None):
    """Fetch trending stories from Dev.to.
    
    Args:
        tag: Optional tag to filter by (e.g., "python", "javascript")
    """
    try:
        url = f"https://dev.to/feed/tag/{tag}" if tag else "https://dev.to/feed"
        xml = fetch_xml(url)
        items = parse_rss(xml)
        return items[:10]
    except Exception as e:
        return []


@tool
def get_hashnode_trending():
    """Fetch trending stories from Hashnode."""
    try:
        url = "https://hashnode.com/feed"
        xml = fetch_xml(url)
        items = parse_rss(xml)
        return items[:10]
    except Exception as e:
        return []


@tool
def get_hackernews_top():
    """Fetch top stories from Hacker News (RSS)."""
    try:
        url = "https://hnrss.org/frontpage"
        xml = fetch_xml(url)
        items = parse_rss(xml)
        return items[:10]
    except Exception as e:
        return []


@tool
def get_reddit_programming():
    """Fetch top programming posts from Reddit RSS."""
    try:
        url = "https://www.reddit.com/r/programming/.rss"
        xml = fetch_xml(url)
        items = parse_rss(xml)
        return items[:10]
    except Exception as e:
        return []
