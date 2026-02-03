"""LangChain Agent for My Daily Log API."""

import os
import json
from typing import Optional, Any, List, Dict
from langchain_groq import ChatGroq

# Import all tools
from tools.news_tools import get_google_news, get_local_news, get_medium_trending
from tools.tech_tools import get_github_trending, get_tech_news, get_trending_videos
from tools.entertainment_tools import (
    get_trending_books, get_trending_fashion, get_best_food, 
    get_quote_of_day, get_trending_movies, get_now_playing_movies,
    get_trending_shows, search_movies
)
from tools.utility_tools import get_local_weather, get_cheapest_gas, get_store_products
from tools.events_tools import get_events_nearby


class DailyLogAgent:
    """Agent for My Daily Log API using Groq and LangChain."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the agent with Groq API key."""
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        
        # Initialize Groq LLM
        self.llm = ChatGroq(
            api_key=self.api_key,
            model="mixtral-8x7b-32768",  # or other Groq models: "llama2-70b-4096"
            temperature=0.3,
        )
        
        # Define all tools as a dictionary for easy access
        self.tools_dict = {
            "get_google_news": get_google_news,
            "get_local_news": get_local_news,
            "get_medium_trending": get_medium_trending,
            "get_github_trending": get_github_trending,
            "get_tech_news": get_tech_news,
            "get_trending_videos": get_trending_videos,
            "get_trending_books": get_trending_books,
            "get_trending_fashion": get_trending_fashion,
            "get_best_food": get_best_food,
            "get_quote_of_day": get_quote_of_day,
            "get_trending_movies": get_trending_movies,
            "get_now_playing_movies": get_now_playing_movies,
            "get_trending_shows": get_trending_shows,
            "search_movies": search_movies,
            "get_local_weather": get_local_weather,
            "get_cheapest_gas": get_cheapest_gas,
            "get_store_products": get_store_products,
            "get_events_nearby": get_events_nearby,
        }
        
        self.tools = [
            get_google_news,
            get_local_news,
            get_medium_trending,
            get_github_trending,
            get_tech_news,
            get_trending_videos,
            get_trending_books,
            get_trending_fashion,
            get_best_food,
            get_quote_of_day,
            get_trending_movies,
            get_now_playing_movies,
            get_trending_shows,
            search_movies,
            get_local_weather,
            get_cheapest_gas,
            get_store_products,
            get_events_nearby,
        ]

    def _format_result(self, result: Any) -> str:
        """Format tool results consistently as text."""
        if isinstance(result, str):
            return result
        if isinstance(result, list):
            return self._format_list(result)
        if isinstance(result, dict):
            return json.dumps(result, indent=2)
        return str(result)

    def _format_list(self, items: List[Any]) -> str:
        if not items:
            return "No results found."
        lines = []
        for item in items[:10]:
            if isinstance(item, dict):
                title = item.get("title") or item.get("name") or "Item"
                link = item.get("link") or item.get("url") or ""
                line = f"• {title}"
                if link:
                    line += f" ({link})"
                lines.append(line)
            else:
                lines.append(f"• {item}")
        return "\n".join(lines)
    
    def run(self, query: str) -> str:
        """Run the agent with a user query.
        
        Args:
            query: User question or request
        
        Returns:
            Agent's response
        """
        try:
            # Simple implementation - try to match query with tools
            query_lower = query.lower()
            
            # Direct tool matching based on keywords
            if any(word in query_lower for word in ['weather', 'temperature', 'climate']):
                return self._format_result(get_local_weather.invoke({}))
            elif any(word in query_lower for word in ['quote', 'inspiration', 'daily']):
                return self._format_result(get_quote_of_day.invoke({}))
            elif any(word in query_lower for word in ['news', 'google news', 'headlines']):
                return self._format_result(get_google_news.invoke({}))
            elif any(word in query_lower for word in ['tech', 'technology', 'trending tech']):
                return self._format_result(get_tech_news.invoke({}))
            elif any(word in query_lower for word in ['github', 'repository', 'repositories']):
                return self._format_result(get_github_trending.invoke({}))
            elif any(word in query_lower for word in ['medium', 'stories', 'articles']):
                return self._format_result(get_medium_trending.invoke({}))
            elif any(word in query_lower for word in ['event', 'events', 'nearby']):
                return self._format_result(get_events_nearby.invoke({}))
            elif any(word in query_lower for word in ['trending', 'trends']):
                # Return combined trends
                result = "📊 Trending Information:\n\n"
                result += "🔥 Tech: " + self._format_result(get_tech_news.invoke({})) + "\n\n"
                result += "📰 News: " + self._format_result(get_google_news.invoke({})) + "\n\n"
                result += "💭 Quote: " + self._format_result(get_quote_of_day.invoke({}))
                return result
            else:
                # Default to news
                return f"Query: {query}\n\n" + self._format_result(get_google_news.invoke({}))
                
        except Exception as e:
            return f"Error: {str(e)}"
    
    def get_news(self, topic: Optional[str] = None, country: str = "US") -> str:
        """Fetch news using the agent."""
        query = f"Get news about {topic}" if topic else "Get top news"
        if country != "US":
            query += f" from {country}"
        return self.run(query)
    
    def get_weather(self) -> str:
        """Fetch weather using the agent."""
        return self.run("What's the weather like?")
    
    def get_trends(self) -> str:
        """Fetch various trends using the agent."""
        return self.run("Show me trending news, tech, and entertainment")


def get_agent(api_key: Optional[str] = None) -> DailyLogAgent:
    """Factory function to get or create the agent."""
    if not hasattr(get_agent, "_instance"):
        get_agent._instance = DailyLogAgent(api_key)
    return get_agent._instance
