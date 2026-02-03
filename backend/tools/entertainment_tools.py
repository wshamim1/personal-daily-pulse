"""Entertainment and lifestyle tools with real API integration."""

import requests
import random
import sys
from pathlib import Path
from langchain.tools import tool
from typing import Optional, Dict, Any

# Add backend to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import APIConfig


@tool
def get_trending_books(query: str = "trending"):
    """Fetch trending books from Open Library API.
    
    Args:
        query: Search query for books (default: 'trending')
    
    Returns:
        List of book objects
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
    ]


@tool
def get_trending_fashion():
    """Fetch trending fashion items and styles."""
    try:
        # Return array of fashion trends
        return [
            {
                "title": "Minimalist Fashion",
                "link": "https://www.vogue.com/fashion/trends",
                "pubDate": "2026-02-02"
            },
            {
                "title": "Sustainable & Eco-Friendly Clothing",
                "link": "https://www.vogue.com/fashion/sustainability",
                "pubDate": "2026-02-01"
            },
            {
                "title": "Retro 90s Revival",
                "link": "https://www.vogue.com/fashion/90s-trends",
                "pubDate": "2026-02-01"
            },
        ]
    except Exception as e:
        return []


@tool
def get_best_food(cuisine: Optional[str] = None):
    """Fetch best food restaurants using Yelp API.
    
    Args:
        cuisine: Type of cuisine (italian, asian, indian, mexican, vegan, seafood, etc.)
    
    Returns:
        Array of restaurant objects
    """
    try:
        if not APIConfig.YELP_API_KEY:
            print("Yelp API key not configured, using mock data")
            return _get_default_restaurants(cuisine)
        
        headers = {
            "Authorization": f"Bearer {APIConfig.YELP_API_KEY}"
        }
        
        url = f"{APIConfig.YELP_BASE_URL}/businesses/search"
        params = {
            "location": APIConfig.DEFAULT_LOCATION,
            "categories": cuisine or "restaurants",
            "limit": 10,
            "sort_by": "rating"
        }
        
        response = requests.get(url, headers=headers, params=params, timeout=APIConfig.REQUEST_TIMEOUT)
        response.raise_for_status()
        data = response.json()
        
        restaurants = []
        for business in data.get("businesses", []):
            restaurant = {
                "name": business.get("name", ""),
                "cuisine": cuisine or "Restaurant",
                "rating": f"{business.get('rating', 0)}/5",
                "reviews": business.get("review_count", 0),
                "price": business.get("price", "$$"),
                "address": " ".join(business.get("location", {}).get("display_address", [])),
                "phone": business.get("phone", ""),
                "link": business.get("url", ""),
            }
            restaurants.append(restaurant)
        
        return restaurants if restaurants else _get_default_restaurants(cuisine)
        
    except Exception as e:
        print(f"Error fetching restaurants: {str(e)}")
        return _get_default_restaurants(cuisine)


def _get_default_restaurants(cuisine: Optional[str] = None):
    """Return default restaurants when API fails."""
    if cuisine == "italian":
        return [
            {
                "name": "Bella Italia",
                "cuisine": "Italian",
                "rating": "4.8/5",
                "reviews": 324,
                "price": "$$$",
            },
        ]
    elif cuisine == "thai":
        return [
            {
                "name": "Bangkok Street",
                "cuisine": "Thai",
                "rating": "4.8/5",
                "reviews": 301,
                "price": "$$",
            },
            {
                "name": "Siam Garden",
                "cuisine": "Thai",
                "rating": "4.7/5",
                "reviews": 245,
                "price": "$$",
            },
        ]
    elif cuisine == "chinese":
        return [
            {
                "name": "Golden Wok",
                "cuisine": "Chinese",
                "rating": "4.6/5",
                "reviews": 278,
                "price": "$$",
            },
            {
                "name": "Dragon Palace",
                "cuisine": "Chinese",
                "rating": "4.7/5",
                "reviews": 342,
                "price": "$$",
            },
        ]
    else:
        return [
            {
                "name": "The Gourmet Kitchen",
                "cuisine": "Contemporary",
                "rating": "4.9/5",
                "reviews": 421,
                "price": "$$$",
            },
        ]


@tool
def get_quote_of_day() -> Dict[str, str]:
    """Get the quote of the day from Quotable API."""
    try:
        url = "https://api.quotable.io/random"
        response = requests.get(url, timeout=APIConfig.REQUEST_TIMEOUT)
        response.raise_for_status()
        data = response.json()
        
        return {
            "text": data.get("content", ""),
            "author": data.get("author", "Unknown")
        }
    except Exception as e:
        print(f"Error fetching quote: {str(e)}")
        return _get_default_quote()


def _get_default_quote() -> Dict[str, str]:
    """Return default inspirational quote when API fails."""
    fallback_quotes = [
        {"text": "The only way to do great work is to love what you do.", "author": "Steve Jobs"},
        {"text": "Success is not final, failure is not fatal: it is the courage to continue that counts.", "author": "Winston Churchill"},
        {"text": "Believe you can and you're halfway there.", "author": "Theodore Roosevelt"},
    ]
    return random.choice(fallback_quotes)


@tool
def get_trending_movies() -> str:
    """Fetch trending movies from TMDB API."""
    try:
        if not APIConfig.TMDB_API_KEY:
            print("TMDB API key not configured")
            return _get_default_movies_info()
        
        url = f"{APIConfig.TMDB_BASE_URL}/trending/movie/week"
        params = {
            "api_key": APIConfig.TMDB_API_KEY,
            "language": "en-US"
        }
        
        response = requests.get(url, params=params, timeout=APIConfig.REQUEST_TIMEOUT)
        response.raise_for_status()
        data = response.json()
        
        movies = data.get("results", [])[:10]
        result = "🎬 Trending Movies:\n\n"
        for movie in movies:
            result += f"• {movie.get('title', 'N/A')} (⭐ {movie.get('vote_average', 'N/A')}/10)\n"
        
        return result if result != "🎬 Trending Movies:\n\n" else _get_default_movies_info()
        
    except Exception as e:
        print(f"Error fetching trending movies: {str(e)}")
        return _get_default_movies_info()


@tool
def get_now_playing_movies() -> str:
    """Get movies currently playing in theaters from TMDB API."""
    try:
        if not APIConfig.TMDB_API_KEY:
            return _get_default_now_playing()
        
        url = f"{APIConfig.TMDB_BASE_URL}/movie/now_playing"
        params = {
            "api_key": APIConfig.TMDB_API_KEY,
            "region": APIConfig.DEFAULT_COUNTRY
        }
        
        response = requests.get(url, params=params, timeout=APIConfig.REQUEST_TIMEOUT)
        response.raise_for_status()
        data = response.json()
        
        movies = data.get("results", [])[:8]
        result = "🎭 Movies Now Playing:\n\n"
        for movie in movies:
            result += f"• {movie.get('title', 'N/A')}\n"
        
        return result if result != "🎭 Movies Now Playing:\n\n" else _get_default_now_playing()
        
    except Exception as e:
        print(f"Error fetching now playing movies: {str(e)}")
        return _get_default_now_playing()


@tool
def get_trending_shows() -> str:
    """Fetch trending TV shows from TMDB API."""
    try:
        if not APIConfig.TMDB_API_KEY:
            return _get_default_shows_info()
        
        url = f"{APIConfig.TMDB_BASE_URL}/trending/tv/week"
        params = {
            "api_key": APIConfig.TMDB_API_KEY,
            "language": "en-US"
        }
        
        response = requests.get(url, params=params, timeout=APIConfig.REQUEST_TIMEOUT)
        response.raise_for_status()
        data = response.json()
        
        shows = data.get("results", [])[:10]
        result = "📺 Trending TV Shows:\n\n"
        for show in shows:
            result += f"• {show.get('name', 'N/A')} (⭐ {show.get('vote_average', 'N/A')}/10)\n"
        
        return result if result != "📺 Trending TV Shows:\n\n" else _get_default_shows_info()
        
    except Exception as e:
        print(f"Error fetching trending shows: {str(e)}")
        return _get_default_shows_info()


@tool
def search_movies(query: str) -> str:
    """Search for movies by title or keyword using TMDB API.
    
    Args:
        query: Movie title or keyword to search
    
    Returns:
        String containing search results
    """
    try:
        if not APIConfig.TMDB_API_KEY:
            return f"Search results for '{query}': Configure TMDB_API_KEY to enable real search"
        
        url = f"{APIConfig.TMDB_BASE_URL}/search/movie"
        params = {
            "api_key": APIConfig.TMDB_API_KEY,
            "query": query,
            "language": "en-US"
        }
        
        response = requests.get(url, params=params, timeout=APIConfig.REQUEST_TIMEOUT)
        response.raise_for_status()
        data = response.json()
        
        movies = data.get("results", [])[:5]
        result = f"🔍 Search results for '{query}':\n\n"
        for movie in movies:
            result += f"• {movie.get('title', 'N/A')} ({movie.get('release_date', 'N/A')[:4]})\n"
        
        return result if movies else f"No results found for '{query}'"
        
    except Exception as e:
        print(f"Error searching movies: {str(e)}")
        return f"Error searching for '{query}'"


def _get_default_movies_info() -> str:
    """Return default movies info when API fails."""
    return "🎬 Trending Movies:\n\nConfigure TMDB_API_KEY for real trending data\n• Visit https://www.themoviedb.org/ for API key"


def _get_default_now_playing() -> str:
    """Return default now playing info when API fails."""
    return "🎭 Movies Now Playing:\n\nConfigure TMDB_API_KEY to see current theater releases"


def _get_default_shows_info() -> str:
    """Return default shows info when API fails."""
    return "📺 Trending TV Shows:\n\nConfigure TMDB_API_KEY for real trending show data"
