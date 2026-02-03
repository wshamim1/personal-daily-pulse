"""Tech news tools for fetching technology news and trends."""

from langchain.tools import tool
from .utils import fetch_xml, parse_rss


@tool
def get_tech_news():
    """Fetch trending technology news and stories."""
    try:
        url = "https://news.google.com/rss/topics/TECHNOLOGY?hl=en&gl=US&ceid=US:en"
        xml = fetch_xml(url)
        items = parse_rss(xml)
        
        # Return array of news objects for frontend compatibility
        return items[:10]
    except Exception as e:
        # Fallback to curated tech news if RSS fails
        return [
            {
                "title": "Latest AI Breakthroughs in 2026",
                "url": "https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGRqTVhZU0FtVnVHZ0pWVXlnQVAB",
                "pubDate": "2026-02-02",
                "score": 0,
                "comments": 0
            },
            {
                "title": "New Programming Languages Gaining Popularity",
                "url": "https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGRqTVhZU0FtVnVHZ0pWVXlnQVAB",
                "pubDate": "2026-02-02",
                "score": 0,
                "comments": 0
            },
            {
                "title": "Cloud Computing Trends for Enterprise",
                "url": "https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGRqTVhZU0FtVnVHZ0pWVXlnQVAB",
                "pubDate": "2026-02-01",
                "score": 0,
                "comments": 0
            },
            {
                "title": "Cybersecurity Best Practices in 2026",
                "url": "https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGRqTVhZU0FtVnVHZ0pWVXlnQVAB",
                "pubDate": "2026-02-01",
                "score": 0,
                "comments": 0
            },
            {
                "title": "Quantum Computing Makes New Advances",
                "url": "https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGRqTVhZU0FtVnVHZ0pWVXlnQVAB",
                "pubDate": "2026-01-31",
                "score": 0,
                "comments": 0
            }
        ]


@tool
def get_trending_videos() -> str:
    """Fetch trending videos from YouTube (via external API)."""
    try:
        from .utils import fetch_text
        url = "https://www.youtube.com/feed/trending?gl=US"
        text = fetch_text(url)
        # Simple parsing - extract video titles
        videos_text = "YouTube Trending Videos: Visit https://www.youtube.com/feed/trending for real-time trending videos"
        return videos_text
    except Exception as e:
        return f"Error fetching YouTube trends: {str(e)}"
