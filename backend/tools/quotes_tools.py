"""Quotes tools for fetching inspirational and motivational quotes."""

from langchain.tools import tool
from .utils import fetch_json


@tool
def get_quote_of_day():
    """Get the quote of the day."""
    try:
        url = "https://api.quotable.io/random"
        data = fetch_json(url)
        # Return object for frontend compatibility
        return {
            "text": data.get("content", ""),
            "author": data.get("author", "Unknown")
        }
    except Exception as e:
        # Fallback inspirational quotes
        import random
        fallback_quotes = [
            {"text": "The only way to do great work is to love what you do.", "author": "Steve Jobs"},
            {"text": "Success is not final, failure is not fatal: it is the courage to continue that counts.", "author": "Winston Churchill"},
            {"text": "Believe you can and you're halfway there.", "author": "Theodore Roosevelt"},
            {"text": "The future belongs to those who believe in the beauty of their dreams.", "author": "Eleanor Roosevelt"},
            {"text": "It does not matter how slowly you go as long as you do not stop.", "author": "Confucius"},
            {"text": "Everything you've ever wanted is on the other side of fear.", "author": "George Addair"},
            {"text": "Success is walking from failure to failure with no loss of enthusiasm.", "author": "Winston Churchill"},
            {"text": "The only impossible journey is the one you never begin.", "author": "Tony Robbins"}
        ]
        return random.choice(fallback_quotes)
