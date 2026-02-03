"""GitHub tools for fetching trending repositories."""

from langchain.tools import tool
from .utils import fetch_json
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
