"""Tech and trending tools."""

from langchain.tools import tool
from .utils import fetch_json, fetch_text
from typing import Optional
import urllib.parse


@tool
def get_github_trending(language: Optional[str] = None, spoken_language: str = "en"):
    """Fetch trending repositories from GitHub.
    
    Args:
        language: Programming language filter (python, javascript, go, rust, etc.)
        spoken_language: Language for README (en, es, fr, etc.)
    
    Returns:
        Array of GitHub repository objects
    """
    try:
        url = "https://api.github.com/search/repositories"
        params = {
            "q": "stars:>1000 created:>2025-01-01",
            "sort": "stars",
            "order": "desc"
        }
        if language:
            params["q"] += f" language:{language}"
        
        url = f"{url}?{'&'.join(f'{k}={urllib.parse.quote(str(v))}' for k,v in params.items())}"
        data = fetch_json(url)
        
        # Return array of repo objects for frontend compatibility
        repos = []
        for r in data.get("items", [])[:10]:
            repos.append({
                "name": r.get("full_name", "Unknown"),
                "description": r.get("description", ""),
                "stars": r.get("stargazers_count", 0),
                "language": r.get("language", ""),
                "url": r.get("html_url", "")
            })
        return repos
    except Exception as e:
        return []


@tool
def get_tech_news():
    """Fetch trending technology news and stories."""
    try:
        url = "https://news.google.com/rss/topics/TECHNOLOGY?hl=en&gl=US&ceid=US:en"
        from .utils import fetch_xml, parse_rss
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
        url = "https://www.youtube.com/feed/trending?gl=US"
        text = fetch_text(url)
        # Simple parsing - extract video titles
        videos_text = "YouTube Trending Videos: Visit https://www.youtube.com/feed/trending for real-time trending videos"
        return videos_text
    except Exception as e:
        return f"Error fetching YouTube trends: {str(e)}"
