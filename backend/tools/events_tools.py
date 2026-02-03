"""Events tools for fetching nearby events."""

import os
import sys
from pathlib import Path
import requests
from langchain.tools import tool
from typing import Optional, List, Dict

# Add backend to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import APIConfig


@tool
def get_events_nearby(
    location: Optional[str] = None,
    radius: int = 25,
    unit: str = "miles",
    category: Optional[str] = None,
) -> List[Dict]:
    """Fetch nearby events using Ticketmaster (if configured) or return mock data.

    Args:
        location: City or location query (e.g., "New York, NY")
        radius: Search radius
        unit: "miles" or "km"
        category: Category keyword (music, sports, tech, food, arts)
    """
    try:
        if APIConfig.TICKETMASTER_API_KEY:
            url = f"{APIConfig.TICKETMASTER_BASE_URL}/events.json"
            params = {
                "apikey": APIConfig.TICKETMASTER_API_KEY,
                "keyword": category or "",
                "radius": radius,
                "unit": unit,
                "locale": "*",
            }
            if location:
                params["city"] = location

            response = requests.get(url, params=params, timeout=APIConfig.REQUEST_TIMEOUT)
            response.raise_for_status()
            data = response.json()

            events = []
            for item in data.get("_embedded", {}).get("events", [])[:15]:
                venue = (item.get("_embedded", {}).get("venues") or [{}])[0]
                events.append({
                    "name": item.get("name"),
                    "date": item.get("dates", {}).get("start", {}).get("localDate"),
                    "time": item.get("dates", {}).get("start", {}).get("localTime"),
                    "venue": venue.get("name"),
                    "city": venue.get("city", {}).get("name"),
                    "country": venue.get("country", {}).get("countryCode"),
                    "url": item.get("url"),
                    "category": category or "Event",
                })

            return events if events else _get_default_events(location, category)

        return _get_default_events(location, category)
    except Exception:
        return _get_default_events(location, category)


def _get_default_events(location: Optional[str], category: Optional[str]) -> List[Dict]:
    city = location or os.getenv("DEFAULT_LOCATION", "New York, NY")
    label = category or "Community"
    return [
        {
            "name": f"{label} Meetup",
            "date": "2026-02-07",
            "time": "18:30",
            "venue": "Downtown Hall",
            "city": city,
            "country": "US",
            "url": "https://www.meetup.com/",
            "category": label,
        },
        {
            "name": f"{label} Networking Night",
            "date": "2026-02-09",
            "time": "19:00",
            "venue": "City Conference Center",
            "city": city,
            "country": "US",
            "url": "https://www.eventbrite.com/",
            "category": label,
        },
        {
            "name": f"{label} Live Session",
            "date": "2026-02-10",
            "time": "20:00",
            "venue": "Main Theater",
            "city": city,
            "country": "US",
            "url": "https://www.ticketmaster.com/",
            "category": label,
        },
    ]
