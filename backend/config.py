"""Configuration for API endpoints and keys."""

import os
from typing import Dict, Any


class APIConfig:
    """Centralized API configuration."""
    
    # Google Books API
    GOOGLE_BOOKS_API_KEY = os.getenv("GOOGLE_BOOKS_API_KEY", "")
    GOOGLE_BOOKS_BASE_URL = "https://www.googleapis.com/books/v1"
    
    # Open Library API (no key required)
    OPEN_LIBRARY_BASE_URL = "https://openlibrary.org"
    
    # NewsAPI
    NEWS_API_KEY = os.getenv("NEWS_API_KEY", "")
    NEWS_API_BASE_URL = "https://newsapi.org/v2"
    
    # TMDB (The Movie Database)
    TMDB_API_KEY = os.getenv("TMDB_API_KEY", "")
    TMDB_BASE_URL = "https://api.themoviedb.org/3"
    
    # OpenWeatherMap API
    WEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")
    WEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5"
    
    # GasBuddy or similar (using free alternative)
    GAS_API_BASE_URL = "https://www.gasbuddy.com/api"
    
    # Yelp API for food/restaurants
    YELP_API_KEY = os.getenv("YELP_API_KEY", "")
    YELP_BASE_URL = "https://api.yelp.com/v3"
    
    # GitHub API
    GITHUB_API_KEY = os.getenv("GITHUB_API_KEY", "")
    GITHUB_BASE_URL = "https://api.github.com"
    
    # YouTube API
    YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "")
    YOUTUBE_BASE_URL = "https://www.googleapis.com/youtube/v3"

    # Ticketmaster Events API
    TICKETMASTER_API_KEY = os.getenv("TICKETMASTER_API_KEY", "")
    TICKETMASTER_BASE_URL = "https://app.ticketmaster.com/discovery/v2"
    
    # Location for local data
    DEFAULT_LOCATION = os.getenv("DEFAULT_LOCATION", "New York, NY")
    DEFAULT_COUNTRY = os.getenv("DEFAULT_COUNTRY", "US")
    
    # Timeouts
    REQUEST_TIMEOUT = 10
    
    @staticmethod
    def get_config() -> Dict[str, Any]:
        """Get all configuration as dictionary."""
        return {
            "google_books_api_key": APIConfig.GOOGLE_BOOKS_API_KEY,
            "news_api_key": APIConfig.NEWS_API_KEY,
            "tmdb_api_key": APIConfig.TMDB_API_KEY,
            "weather_api_key": APIConfig.WEATHER_API_KEY,
            "yelp_api_key": APIConfig.YELP_API_KEY,
            "github_api_key": APIConfig.GITHUB_API_KEY,
            "youtube_api_key": APIConfig.YOUTUBE_API_KEY,
            "ticketmaster_api_key": APIConfig.TICKETMASTER_API_KEY,
            "default_location": APIConfig.DEFAULT_LOCATION,
            "default_country": APIConfig.DEFAULT_COUNTRY,
        }
