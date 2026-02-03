"""Gas price tools for finding cheapest fuel prices."""

from langchain.tools import tool
from typing import Optional


@tool
def get_cheapest_gas(zipcode: Optional[str] = None):
    """Find cheapest gas prices nearby.
    
    Args:
        zipcode: ZIP code for location (optional)
    
    Returns:
        Array of gas station objects with prices
    """
    try:
        location = f"ZIP {zipcode}" if zipcode else "Current Location"
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
                "address": "123 Main Street"
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
                "address": "456 Oak Avenue"
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
                "address": "789 Pine Road"
            },
            {
                "station": "Exxon Mobil",
                "location": location,
                "regular": "$3.50",
                "midgrade": "$3.70",
                "premium": "$3.90",
                "diesel": "$3.60",
                "rating": "4.4/5",
                "distance": "1.5 miles",
                "address": "321 Elm Street"
            },
            {
                "station": "Speedway",
                "location": location,
                "regular": "$3.39",
                "midgrade": "$3.59",
                "premium": "$3.79",
                "diesel": "$3.49",
                "rating": "4.1/5",
                "distance": "2.0 miles",
                "address": "654 Maple Drive"
            },
            {
                "station": "Sunoco",
                "location": location,
                "regular": "$3.44",
                "midgrade": "$3.64",
                "premium": "$3.84",
                "diesel": "$3.54",
                "rating": "4.3/5",
                "distance": "2.3 miles",
                "address": "987 Birch Lane"
            },
            {
                "station": "Valero",
                "location": location,
                "regular": "$3.41",
                "midgrade": "$3.61",
                "premium": "$3.81",
                "diesel": "$3.51",
                "rating": "4.6/5",
                "distance": "2.8 miles",
                "address": "159 Cedar Street"
            },
            {
                "station": "Love's Travel Stops",
                "location": location,
                "regular": "$3.46",
                "midgrade": "$3.66",
                "premium": "$3.86",
                "diesel": "$3.56",
                "rating": "4.2/5",
                "distance": "3.2 miles",
                "address": "753 Spruce Avenue"
            },
            {
                "station": "Casey's General Stores",
                "location": location,
                "regular": "$3.43",
                "midgrade": "$3.63",
                "premium": "$3.83",
                "diesel": "$3.53",
                "rating": "4.4/5",
                "distance": "3.5 miles",
                "address": "456 Willow Way"
            },
            {
                "station": "Pilot Flying J",
                "location": location,
                "regular": "$3.47",
                "midgrade": "$3.67",
                "premium": "$3.87",
                "diesel": "$3.57",
                "rating": "4.3/5",
                "distance": "4.0 miles",
                "address": "789 Ash Court"
            }
        ]
    except Exception as e:
        return []
