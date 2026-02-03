#!/usr/bin/env python3
"""FastAPI backend for My Daily Log - aggregates all data sources using LangChain agents."""

import os
import sys
import json
from typing import Optional
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the LangChain agent
from agent import get_agent

# Import individual tool functions from refactored modules
from tools.entertainment_tools import (
    get_trending_books, 
    get_trending_fashion, 
    get_best_food, 
    get_quote_of_day,
    get_trending_movies, 
    get_now_playing_movies, 
    get_trending_shows, 
    search_movies
)
from tools.utility_tools import (
    get_local_weather, 
    get_cheapest_gas, 
    get_store_products
)

# Import other specialized tools
from tools.google_news_tools import get_google_news
from tools.medium_tools import get_medium_trending
from tools.local_news_tools import get_local_news
from tools.github_tools import get_github_trending
from tools.tech_news_tools import get_tech_news, get_trending_videos

app = FastAPI(
    title="My Daily Log API",
    description="AI-powered agent using LangChain with Groq for daily information",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str


@app.get("/")
async def home():
    """API home endpoint."""
    return {
        "message": "My Daily Log API - Powered by LangChain + Groq",
        "version": "2.0.0",
        "description": "AI-powered agent that uses LangChain with Groq for fetching and aggregating daily information",
        "endpoints": {
            "query": "/api/query?q=<your_question>",
            "news": "/api/news?topic=<topic>",
            "weather": "/api/weather",
            "trends": "/api/trends",
            "github": "/api/github?language=<language>",
        },
        "examples": [
            "/api/query?q=What's the latest news?",
            "/api/query?q=Show me trending tech news",
            "/api/weather",
            "/api/news?topic=TECHNOLOGY",
            "/api/trends",
        ],
        "docs": "/docs"
    }


@app.get("/api/query")
async def query_get(q: str = Query(..., description="Your question")):
    """Universal query endpoint using LangChain agent (GET)."""
    try:
        agent = get_agent()
        response = agent.run(q)
        
        return {
            "success": True,
            "query": q,
            "response": response
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/query")
async def query_post(request: QueryRequest):
    """Universal query endpoint using LangChain agent (POST)."""
    try:
        agent = get_agent()
        response = agent.run(request.query)
        
        return {
            "success": True,
            "query": request.query,
            "response": response
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/news")
async def news(topic: Optional[str] = None, country: str = "US"):
    """Get news using the agent."""
    try:
        agent = get_agent()
        if topic:
            response = agent.run(f"Get {topic} news from {country}")
        else:
            response = agent.run(f"Get top news from {country}")
        
        return {
            "success": True,
            "topic": topic or "general",
            "country": country,
            "response": response
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/weather")
async def weather():
    """Get local weather with caching and fallback."""
    import httpx
    import time
    
    # Simple cache with 5-minute TTL
    cache_key = "weather_data"
    cache_ttl_key = "weather_ttl"
    
    # Check cache
    if hasattr(weather, '_cache') and cache_key in weather._cache:
        if time.time() < weather._cache.get(cache_ttl_key, 0):
            return weather._cache[cache_key]
    
    try:
        async with httpx.AsyncClient(timeout=2.0) as client:
            response = await client.get("https://wttr.in/?format=j1")
            response.raise_for_status()
            data = response.json()
        
        current = data.get("current_condition", [{}])[0]
        
        result = {
            "success": True,
            "data": {
                "condition": current.get("weatherDesc", [{}])[0].get("value", "Unknown"),
                "temp_c": current.get("temp_C", "0"),
                "temp_f": current.get("temp_F", "0"),
                "feels_like_c": current.get("FeelsLikeC", "0"),
                "feels_like_f": current.get("FeelsLikeF", "0"),
                "humidity": current.get("humidity", "0")
            }
        }
        
        # Cache result for 5 minutes (300 seconds)
        if not hasattr(weather, '_cache'):
            weather._cache = {}
        weather._cache[cache_key] = result
        weather._cache[cache_ttl_key] = time.time() + 300
        
        return result
    except Exception as e:
        # Return cached data if available, even if expired
        if hasattr(weather, '_cache') and cache_key in weather._cache:
            return weather._cache[cache_key]
        
        # Fallback to mock weather data
        result = {
            "success": True,
            "data": {
                "condition": "Partly Cloudy",
                "temp_c": "20",
                "temp_f": "68",
                "feels_like_c": "19",
                "feels_like_f": "66",
                "humidity": "65"
            }
        }
        
        # Cache fallback for 5 minutes
        if not hasattr(weather, '_cache'):
            weather._cache = {}
        weather._cache[cache_key] = result
        weather._cache[cache_ttl_key] = time.time() + 300
        
        return result


@app.get("/api/trends")
async def trends():
    """Get various trends using the agent."""
    try:
        agent = get_agent()
        response = agent.get_trends()
        
        return {
            "success": True,
            "response": response
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/github")
async def github_trending(language: Optional[str] = None):
    """Get trending GitHub repos using the agent."""
    try:
        agent = get_agent()
        
        if language:
            response = agent.run(f"Show me trending {language} repositories on GitHub")
        else:
            response = agent.run("Show me trending repositories on GitHub")
        
        return {
            "success": True,
            "language": language or "all",
            "response": response
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/agent/info")
async def agent_info():
    """Get information about available agent tools."""
    try:
        agent = get_agent()
        tools_info = []
        
        for tool in agent.tools:
            tools_info.append({
                "name": tool.name,
                "description": tool.description,
            })
        
        return {
            "success": True,
            "model": "Groq (mixtral-8x7b-32768)",
            "tools_count": len(tools_info),
            "tools": tools_info
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Backward compatibility endpoints for old frontend
@app.get("/api/medium/trending")
async def medium_trending():
    """Get Medium trending stories (backward compatibility)."""
    try:
        from tools.news_tools import get_medium_trending
        result = get_medium_trending.invoke({})
        return {
            "success": True,
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/articles/medium")
async def articles_medium():
    """Get Medium trending stories."""
    try:
        from tools.news_tools import get_medium_trending
        result = get_medium_trending.invoke({})
        return {
            "success": True,
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/articles/devto")
async def articles_devto(tag: Optional[str] = None):
    """Get Dev.to trending stories."""
    try:
        from tools.news_tools import get_devto_trending
        result = get_devto_trending.invoke({"tag": tag} if tag else {})
        return {
            "success": True,
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/articles/hashnode")
async def articles_hashnode():
    """Get Hashnode trending stories."""
    try:
        from tools.news_tools import get_hashnode_trending
        result = get_hashnode_trending.invoke({})
        return {
            "success": True,
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/articles/hackernews")
async def articles_hackernews():
    """Get Hacker News top stories."""
    try:
        from tools.news_tools import get_hackernews_top
        result = get_hackernews_top.invoke({})
        return {
            "success": True,
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/articles/reddit")
async def articles_reddit():
    """Get Reddit programming stories."""
    try:
        from tools.news_tools import get_reddit_programming
        result = get_reddit_programming.invoke({})
        return {
            "success": True,
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/news/google")
async def google_news(topic: Optional[str] = None):
    """Get Google News (backward compatibility)."""
    try:
        from tools.news_tools import get_google_news
        result = get_google_news.invoke({"topic": topic} if topic else {})
        return {
            "success": True,
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/news/country")
async def country_news(country: str = "US", lang: str = "en"):
    """Get country-specific news (Google News RSS)."""
    try:
        from tools.news_tools import get_country_news
        result = get_country_news.invoke({"country": country, "lang": lang})
        return {
            "success": True,
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/news/international")
async def international_news(lang: str = "en", country: str = "US"):
    """Get international/world news (Google News RSS)."""
    try:
        from tools.news_tools import get_international_news
        result = get_international_news.invoke({"lang": lang, "country": country})
        return {
            "success": True,
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/news/local")
async def local_news(location: Optional[str] = None, country: str = "US", lang: str = "en"):
    """Get local news (backward compatibility)."""
    try:
        from tools.news_tools import get_local_news
        payload = {"location": location, "country": country, "lang": lang}
        result = get_local_news.invoke(payload)
        return {
            "success": True,
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/books/trending")
async def books_trending():
    """Get trending books (backward compatibility)."""
    try:
        from tools.entertainment_tools import get_trending_books
        result = get_trending_books.invoke({})
        return {
            "success": True,
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/github/trending")
async def github_trending_old(language: Optional[str] = None):
    """Get GitHub trending (backward compatibility)."""
    try:
        from tools.tech_tools import get_github_trending
        result = get_github_trending.invoke({"language": language} if language else {})
        return {
            "success": True,
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/tech/trending")
async def tech_trending():
    """Get tech trending (backward compatibility)."""
    try:
        from tools.tech_tools import get_tech_news
        result = get_tech_news.invoke({})
        return {
            "success": True,
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/quotes/daily")
async def quotes_daily():
    """Get quote of the day (backward compatibility)."""
    try:
        from tools.entertainment_tools import get_quote_of_day
        result = get_quote_of_day.invoke({})
        return {
            "success": True,
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/fashion/trending")
async def fashion_trending():
    """Get fashion trending (backward compatibility)."""
    try:
        from tools.entertainment_tools import get_trending_fashion
        result = get_trending_fashion.invoke({})
        return {
            "success": True,
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/shopping/products")
async def shopping_products(store: Optional[str] = None, category: Optional[str] = None):
    """Get shopping products by store and category."""
    try:
        from tools.utility_tools import get_store_products
        result = get_store_products.invoke({"store": store, "category": category})
        return {
            "success": True,
            "store": store or "All Stores",
            "category": category or "All",
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/shopping/electronics")
async def shopping_electronics():
    """Get trending electronics."""
    try:
        from tools.utility_tools import get_store_products
        result = get_store_products.invoke({"store": None, "category": "electronics"})
        return {
            "success": True,
            "category": "Electronics",
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/shopping/books")
async def shopping_books():
    """Get popular books for shopping."""
    try:
        from tools.utility_tools import get_store_products
        result = get_store_products.invoke({"store": None, "category": "books"})
        return {
            "success": True,
            "category": "Books",
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/shopping/clothing")
async def shopping_clothing():
    """Get trending clothing items."""
    try:
        from tools.utility_tools import get_store_products
        result = get_store_products.invoke({"store": None, "category": "clothing"})
        return {
            "success": True,
            "category": "Clothing",
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/gas/prices")
async def gas_prices(zipcode: Optional[str] = None):
    """Get cheapest gas prices nearby."""
    try:
        from tools.utility_tools import get_cheapest_gas
        result = get_cheapest_gas.invoke({"zipcode": zipcode})
        return {
            "success": True,
            "location": zipcode or "Current Location",
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/events/nearby")
async def events_nearby(
    location: Optional[str] = None,
    radius: int = 25,
    unit: str = "miles",
    category: Optional[str] = None,
):
    """Get nearby events by location, radius, and category."""
    try:
        from tools.events_tools import get_events_nearby
        payload = {
            "location": location,
            "radius": radius,
            "unit": unit,
            "category": category,
        }
        result = get_events_nearby.invoke(payload)
        return {
            "success": True,
            "data": result,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/gas/cheapest")
async def gas_cheapest(zipcode: Optional[str] = None):
    """Get the cheapest gas station nearby."""
    try:
        from tools.utility_tools import get_cheapest_gas
        result = get_cheapest_gas.invoke({"zipcode": zipcode})
        if result and len(result) > 0:
            # Find the cheapest regular gas
            cheapest = min(result, key=lambda x: float(x.get("regular", "$9.99").strip("$")))
            return {
                "success": True,
                "cheapest_station": cheapest,
                "all_nearby": result
            }
        return {
            "success": False,
            "error": "No gas stations found"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/food/restaurants")
async def food_restaurants(cuisine: Optional[str] = None):
    """Get best restaurants by cuisine type."""
    try:
        from tools.entertainment_tools import get_best_food
        result = get_best_food.invoke({"cuisine": cuisine})
        return {
            "success": True,
            "cuisine": cuisine or "All",
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/food/italian")
async def food_italian():
    """Get Italian restaurants."""
    try:
        from tools.entertainment_tools import get_best_food
        result = get_best_food.invoke({"cuisine": "italian"})
        return {
            "success": True,
            "cuisine": "Italian",
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/food/asian")
async def food_asian():
    """Get Asian restaurants."""
    try:
        from tools.entertainment_tools import get_best_food
        result = get_best_food.invoke({"cuisine": "asian"})
        return {
            "success": True,
            "cuisine": "Asian",
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/food/thai")
async def food_thai():
    """Get Thai restaurants."""
    try:
        from tools.entertainment_tools import get_best_food
        result = get_best_food.invoke({"cuisine": "thai"})
        return {
            "success": True,
            "cuisine": "Thai",
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/food/chinese")
async def food_chinese():
    """Get Chinese restaurants."""
    try:
        from tools.entertainment_tools import get_best_food
        result = get_best_food.invoke({"cuisine": "chinese"})
        return {
            "success": True,
            "cuisine": "Chinese",
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/food/indian")
async def food_indian():
    """Get Indian restaurants."""
    try:
        from tools.entertainment_tools import get_best_food
        result = get_best_food.invoke({"cuisine": "indian"})
        return {
            "success": True,
            "cuisine": "Indian",
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/food/vegan")
async def food_vegan():
    """Get Vegan restaurants."""
    try:
        from tools.entertainment_tools import get_best_food
        result = get_best_food.invoke({"cuisine": "vegan"})
        return {
            "success": True,
            "cuisine": "Vegan",
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/social/twitter")
async def social_twitter():
    """Get trending content from Twitter/X (uses tech news as placeholder)."""
    try:
        from tools.tech_tools import get_tech_news
        result = get_tech_news.invoke({})
        return {
            "success": True,
            "source": "twitter",
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/social/linkedin")
async def social_linkedin():
    """Get trending content from LinkedIn (uses tech news as placeholder)."""
    try:
        from tools.tech_tools import get_tech_news
        result = get_tech_news.invoke({})
        return {
            "success": True,
            "source": "linkedin",
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    
    # Ensure Groq API key is set
    if not os.getenv("GROQ_API_KEY"):
        print("WARNING: GROQ_API_KEY environment variable not set!")
        print("Please set your Groq API key: export GROQ_API_KEY='your-key-here'")
    
    port = int(os.environ.get("PORT", 5000))
    uvicorn.run(app, host="0.0.0.0", port=port, reload=True)

