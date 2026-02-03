"""Movies tools for fetching movie information and recommendations."""

from langchain.tools import tool


@tool
def get_trending_movies() -> str:
    """Fetch trending movies."""
    try:
        return "Trending Movies:\n\n• Check upcoming releases and popular films at TMDB or IMDb"
    except Exception as e:
        return f"Error fetching trending movies: {str(e)}"


@tool
def get_now_playing_movies() -> str:
    """Get movies currently playing in theaters."""
    try:
        return "Movies Now Playing:\n\n• Visit your local cinema or streaming platforms for current showings"
    except Exception as e:
        return f"Error fetching now playing movies: {str(e)}"


@tool
def get_trending_shows() -> str:
    """Fetch trending TV shows."""
    try:
        return "Trending TV Shows:\n\n• Check popular series on major streaming platforms"
    except Exception as e:
        return f"Error fetching trending shows: {str(e)}"


@tool
def search_movies(query: str) -> str:
    """Search for movies by title or keyword.
    
    Args:
        query: Movie title or keyword to search
    
    Returns:
        String containing search results
    """
    try:
        return f"Movie search results for '{query}': Check TMDB or IMDb for detailed results"
    except Exception as e:
        return f"Error searching movies: {str(e)}"
