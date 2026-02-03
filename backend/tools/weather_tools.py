"""Weather tools for fetching local and regional weather information."""

from langchain.tools import tool
from .utils import fetch_text
from typing import Optional


@tool
def get_local_weather(format_code: str = "3", units: str = "C") -> str:
    """Get local weather using IP-based location detection.
    
    Args:
        format_code: Weather format (1-4)
        units: Temperature units (C for Celsius, F for Fahrenheit)
    
    Returns:
        String containing weather information
    """
    try:
        unit_param = "m" if units == "C" else "u"
        url = f"https://wttr.in?format={format_code}&{unit_param}"
        weather_text = fetch_text(url)
        return f"Local Weather:\n\n{weather_text}"
    except Exception as e:
        return f"Error fetching weather: {str(e)}"
