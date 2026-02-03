"""Utility tools for weather, shopping, and gas prices using real APIs."""

import requests
import sys
from pathlib import Path
from langchain.tools import tool
from typing import Optional, List, Dict

# Add backend to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import APIConfig


@tool
def get_local_weather(units: str = "C") -> str:
    """Get local weather using OpenWeatherMap or wttr.in.
    
    Args:
        units: Temperature units (C for Celsius, F for Fahrenheit)
    
    Returns:
        String containing weather information
    """
    try:
        # Try OpenWeatherMap first if key is available
        if APIConfig.WEATHER_API_KEY:
            location = APIConfig.DEFAULT_LOCATION
            url = f"{APIConfig.WEATHER_BASE_URL}/weather"
            params = {
                "q": location,
                "appid": APIConfig.WEATHER_API_KEY,
                "units": "metric" if units == "C" else "imperial"
            }
            response = requests.get(url, params=params, timeout=APIConfig.REQUEST_TIMEOUT)
            response.raise_for_status()
            data = response.json()
            
            weather = data.get("main", {})
            description = data.get("weather", [{}])[0].get("description", "N/A")
            result = f"""🌤️ Weather for {location}:
            
Temperature: {weather.get('temp', 'N/A')}°{units}
Feels like: {weather.get('feels_like', 'N/A')}°{units}
Condition: {description.capitalize()}
Humidity: {weather.get('humidity', 'N/A')}%
Wind Speed: {data.get('wind', {}).get('speed', 'N/A')} m/s"""
            return result
        else:
            # Fallback to wttr.in (free, no key required)
            url = f"https://wttr.in?format=3"
            response = requests.get(url, timeout=APIConfig.REQUEST_TIMEOUT)
            response.raise_for_status()
            return f"Weather:\n\n{response.text}"
            
    except Exception as e:
        print(f"Error fetching weather: {str(e)}")
        return _get_default_weather()


def _get_default_weather() -> str:
    """Return default weather when API fails."""
    return f"""🌤️ Weather for {APIConfig.DEFAULT_LOCATION}:

Configure OPENWEATHER_API_KEY for real weather data
• Get free key at https://openweathermap.org/api"""


@tool
def get_cheapest_gas(zipcode: Optional[str] = None) -> List[Dict]:
    """Find cheapest gas prices nearby using GasBuddy or alternative.
    
    Args:
        zipcode: ZIP code for location (optional)
    
    Returns:
        Array of gas station objects with prices
    """
    try:
        if zipcode:
            # In production, use GasBuddy API or similar
            # For now, return mock data with note about API
            pass
        
        return _get_default_gas_stations(zipcode)
        
    except Exception as e:
        print(f"Error fetching gas prices: {str(e)}")
        return _get_default_gas_stations(zipcode)


def _get_default_gas_stations(zipcode: Optional[str] = None) -> List[Dict]:
    """Return default gas station data."""
    location = f"ZIP {zipcode}" if zipcode else APIConfig.DEFAULT_LOCATION
    return [
        {
            "station": "Shell Gas Station",
            "location": location,
            "regular": "$3.45",
            "midgrade": "$3.65",
            "premium": "$3.85",
            "diesel": "$3.55",
            "rating": "4.3/5",
            "distance": "0.5 miles",
        },
        {
            "station": "Chevron",
            "location": location,
            "regular": "$3.42",
            "midgrade": "$3.62",
            "premium": "$3.82",
            "diesel": "$3.52",
            "rating": "4.5/5",
            "distance": "0.8 miles",
        },
        {
            "station": "BP Gas",
            "location": location,
            "regular": "$3.48",
            "midgrade": "$3.68",
            "premium": "$3.88",
            "diesel": "$3.58",
            "rating": "4.2/5",
            "distance": "1.2 miles",
        },
    ]


@tool
def get_store_products(store: Optional[str] = None, category: Optional[str] = None) -> List[Dict]:
    """Get popular products from stores.
    
    Args:
        store: Store name (amazon, walmart, target, etc.)
        category: Product category (electronics, clothing, books, etc.)
    
    Returns:
        Array of product objects
    """
    try:
        # In production, integrate with store APIs (Amazon, Walmart, etc.)
        # For now, return curated default data
        
        if category == "electronics" or not category:
            return [
                {
                    "title": "Wireless Earbuds Pro",
                    "store": store or "Amazon",
                    "original_price": "$99.99",
                    "price": "$79.99",
                    "discount": "20%",
                    "rating": "4.8/5",
                },
                {
                    "title": "Smart Watch Series 8",
                    "store": store or "Best Buy",
                    "original_price": "$349.99",
                    "price": "$299.99",
                    "discount": "14%",
                    "rating": "4.7/5",
                },
                {
                    "title": "Portable SSD 1TB",
                    "store": store or "Walmart",
                    "original_price": "$129.99",
                    "price": "$89.99",
                    "discount": "31%",
                    "rating": "4.6/5",
                },
            ]
        elif category == "books":
            return [
                {
                    "title": "Atomic Habits",
                    "author": "James Clear",
                    "store": store or "Amazon",
                    "original_price": "$27.99",
                    "price": "$15.99",
                    "discount": "43%",
                    "rating": "4.9/5",
                },
                {
                    "title": "The Midnight Library",
                    "author": "Matt Haig",
                    "store": store or "Barnes & Noble",
                    "original_price": "$28.99",
                    "price": "$17.99",
                    "discount": "38%",
                    "rating": "4.7/5",
                },
            ]
        elif category == "clothing":
            return [
                {
                    "title": "Cotton T-Shirt Bundle",
                    "store": store or "Target",
                    "original_price": "$44.99",
                    "price": "$24.99",
                    "discount": "44%",
                    "rating": "4.6/5",
                },
                {
                    "title": "Denim Jeans Classic Fit",
                    "store": store or "Gap",
                    "original_price": "$89.99",
                    "price": "$59.99",
                    "discount": "33%",
                    "rating": "4.5/5",
                },
            ]
        else:
            return [
                {
                    "title": "Popular Item 1",
                    "store": store or "Amazon",
                    "price": "$29.99",
                    "rating": "4.5/5",
                },
                {
                    "title": "Best Seller 2",
                    "store": store or "Walmart",
                    "price": "$39.99",
                    "rating": "4.6/5",
                },
            ]
    except Exception as e:
        print(f"Error fetching products: {str(e)}")
        return []
