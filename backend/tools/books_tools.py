"""Books tools for fetching trending books."""

import requests
import sys
from pathlib import Path
from langchain.tools import tool

# Add backend to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import APIConfig


@tool
def get_trending_books(query: str = "trending"):
    """Fetch trending books from Open Library API.
    
    Args:
        query: Search query for books (default: 'trending')
    
    Returns:
        List of book objects with title, authors, publication date, etc.
    """
    try:
        # Use Open Library API (free, no key required)
        url = f"{APIConfig.OPEN_LIBRARY_BASE_URL}/search.json"
        params = {
            "title": query,
            "limit": 10,
            "sort": "-key"
        }
        
        response = requests.get(url, params=params, timeout=APIConfig.REQUEST_TIMEOUT)
        response.raise_for_status()
        data = response.json()
        
        books = []
        for doc in data.get("docs", [])[:10]:
            book = {
                "title": doc.get("title", "Unknown"),
                "authors": doc.get("author_name", ["Unknown"]),
                "publishedDate": doc.get("first_publish_year", "N/A"),
                "link": f"https://openlibrary.org{doc.get('key', '')}" if doc.get('key') else "",
                "isbn": doc.get("isbn", ["N/A"])[0] if doc.get("isbn") else "N/A",
                "cover_id": doc.get("cover_i"),
            }
            books.append(book)
        
        return books if books else _get_default_books()
        
    except Exception as e:
        print(f"Error fetching books: {str(e)}")
        return _get_default_books()


def _get_default_books():
    """Return default books when API fails."""
    return [
        {
            "title": "The Psychology of Money",
            "authors": ["Morgan Housel"],
            "link": "https://openlibrary.org/works/OL19953894W",
            "publishedDate": "2020"
        },
        {
            "title": "Atomic Habits",
            "authors": ["James Clear"],
            "link": "https://openlibrary.org/works/OL19629461W",
            "publishedDate": "2018"
        },
        {
            "title": "The Midnight Library",
            "authors": ["Matt Haig"],
            "link": "https://openlibrary.org/works/OL20449494W",
            "publishedDate": "2020"
        },
    ]
