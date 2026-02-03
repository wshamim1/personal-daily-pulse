"""Food and restaurant tools for finding restaurants and dining recommendations."""

from langchain.tools import tool
from typing import Optional


@tool
def get_best_food(cuisine: Optional[str] = None):
    """Fetch best food restaurants and recommendations.
    
    Args:
        cuisine: Type of cuisine (italian, asian, indian, mexican, vegan, seafood, etc.)
    
    Returns:
        Array of restaurant objects
    """
    try:
        if cuisine == "italian":
            return [
                {
                    "name": "Bella Italia",
                    "cuisine": "Italian",
                    "rating": "4.8/5",
                    "reviews": 324,
                    "price": "$$$",
                    "address": "123 Main Street",
                    "hours": "5PM - 11PM",
                    "specialties": ["Pasta", "Risotto", "Tiramisu"],
                    "link": "https://www.yelp.com/search?find_desc=italian+restaurants"
                },
                {
                    "name": "Trattoria Roma",
                    "cuisine": "Italian",
                    "rating": "4.7/5",
                    "reviews": 287,
                    "price": "$$",
                    "address": "456 Oak Avenue",
                    "hours": "5PM - 10:30PM",
                    "specialties": ["Pizza", "Carbonara", "Seafood"],
                    "link": "https://www.yelp.com/search?find_desc=italian+restaurants"
                },
                {
                    "name": "Ristorante Napoli",
                    "cuisine": "Italian",
                    "rating": "4.6/5",
                    "reviews": 215,
                    "price": "$$",
                    "address": "789 Pine Road",
                    "hours": "5:30PM - 11PM",
                    "specialties": ["Ravioli", "Lasagna", "Panna Cotta"],
                    "link": "https://www.yelp.com/search?find_desc=italian+restaurants"
                }
            ]
        elif cuisine == "asian":
            return [
                {
                    "name": "Dragon Palace",
                    "cuisine": "Asian Fusion",
                    "rating": "4.7/5",
                    "reviews": 342,
                    "price": "$$",
                    "address": "321 Elm Street",
                    "hours": "11AM - 11PM",
                    "specialties": ["Sushi", "Dim Sum", "Pad Thai"],
                    "link": "https://www.yelp.com/search?find_desc=asian+restaurants"
                },
                {
                    "name": "Tokyo Express",
                    "cuisine": "Japanese",
                    "rating": "4.6/5",
                    "reviews": 298,
                    "price": "$$$",
                    "address": "654 Maple Drive",
                    "hours": "5PM - 10:30PM",
                    "specialties": ["Ramen", "Udon", "Tempura"],
                    "link": "https://www.yelp.com/search?find_desc=asian+restaurants"
                },
                {
                    "name": "Bangkok Street",
                    "cuisine": "Thai",
                    "rating": "4.8/5",
                    "reviews": 301,
                    "price": "$",
                    "address": "987 Birch Lane",
                    "hours": "11AM - 10PM",
                    "specialties": ["Green Curry", "Tom Yum", "Mango Sticky Rice"],
                    "link": "https://www.yelp.com/search?find_desc=asian+restaurants"
                }
            ]
        elif cuisine == "indian":
            return [
                {
                    "name": "Taj Mahal",
                    "cuisine": "Indian",
                    "rating": "4.7/5",
                    "reviews": 267,
                    "price": "$$",
                    "address": "159 Cedar Street",
                    "hours": "5PM - 11PM",
                    "specialties": ["Biryani", "Tandoori", "Naan"],
                    "link": "https://www.yelp.com/search?find_desc=indian+restaurants"
                },
                {
                    "name": "Spice Route",
                    "cuisine": "Indian",
                    "rating": "4.6/5",
                    "reviews": 243,
                    "price": "$$",
                    "address": "753 Spruce Avenue",
                    "hours": "5PM - 10:30PM",
                    "specialties": ["Butter Chicken", "Samosa", "Gulab Jamun"],
                    "link": "https://www.yelp.com/search?find_desc=indian+restaurants"
                },
                {
                    "name": "Curry House",
                    "cuisine": "Indian",
                    "rating": "4.5/5",
                    "reviews": 189,
                    "price": "$",
                    "address": "456 Willow Way",
                    "hours": "11AM - 10PM",
                    "specialties": ["Chana Masala", "Dosa", "Lassi"],
                    "link": "https://www.yelp.com/search?find_desc=indian+restaurants"
                }
            ]
        elif cuisine == "vegan":
            return [
                {
                    "name": "Green Leaf Kitchen",
                    "cuisine": "Vegan",
                    "rating": "4.8/5",
                    "reviews": 198,
                    "price": "$$",
                    "address": "789 Ash Court",
                    "hours": "10AM - 9PM",
                    "specialties": ["Buddha Bowls", "Plant-Based Burgers", "Smoothies"],
                    "link": "https://www.yelp.com/search?find_desc=vegan+restaurants"
                },
                {
                    "name": "Roots & Greens",
                    "cuisine": "Vegan",
                    "rating": "4.7/5",
                    "reviews": 156,
                    "price": "$$",
                    "address": "321 Oak Street",
                    "hours": "11AM - 8:30PM",
                    "specialties": ["Grain Bowls", "Acai Bowls", "Salads"],
                    "link": "https://www.yelp.com/search?find_desc=vegan+restaurants"
                },
                {
                    "name": "Harvest Moon",
                    "cuisine": "Vegan",
                    "rating": "4.6/5",
                    "reviews": 124,
                    "price": "$",
                    "address": "654 Pine Avenue",
                    "hours": "8AM - 9PM",
                    "specialties": ["Smoothie Bowls", "Avocado Toast", "Wraps"],
                    "link": "https://www.yelp.com/search?find_desc=vegan+restaurants"
                }
            ]
        else:
            # Default: Best rated restaurants across all cuisines
            return [
                {
                    "name": "The Gourmet Kitchen",
                    "cuisine": "Contemporary",
                    "rating": "4.9/5",
                    "reviews": 421,
                    "price": "$$$",
                    "address": "123 Luxury Lane",
                    "hours": "6PM - 11PM",
                    "specialties": ["Fine Dining", "Tasting Menu", "Wine Pairing"],
                    "link": "https://www.yelp.com/search?find_desc=restaurants"
                },
                {
                    "name": "Local Farm Table",
                    "cuisine": "Farm-to-Table",
                    "rating": "4.8/5",
                    "reviews": 356,
                    "price": "$$$",
                    "address": "456 Garden Road",
                    "hours": "5PM - 10:30PM",
                    "specialties": ["Seasonal Menu", "Organic", "Craft Cocktails"],
                    "link": "https://www.yelp.com/search?find_desc=restaurants"
                },
                {
                    "name": "Street Eats",
                    "cuisine": "Street Food",
                    "rating": "4.7/5",
                    "reviews": 298,
                    "price": "$",
                    "address": "789 Market Street",
                    "hours": "11AM - 11PM",
                    "specialties": ["Tacos", "Dumplings", "Kebab"],
                    "link": "https://www.yelp.com/search?find_desc=restaurants"
                },
                {
                    "name": "Burger Haven",
                    "cuisine": "American",
                    "rating": "4.6/5",
                    "reviews": 287,
                    "price": "$",
                    "address": "321 Main Street",
                    "hours": "11AM - 10PM",
                    "specialties": ["Craft Burgers", "Hand-Cut Fries", "Milkshakes"],
                    "link": "https://www.yelp.com/search?find_desc=restaurants"
                },
                {
                    "name": "Steakhouse Prime",
                    "cuisine": "Steakhouse",
                    "rating": "4.8/5",
                    "reviews": 312,
                    "price": "$$$",
                    "address": "654 Premier Avenue",
                    "hours": "5PM - 11:30PM",
                    "specialties": ["Prime Rib", "Filet Mignon", "Seafood"],
                    "link": "https://www.yelp.com/search?find_desc=restaurants"
                },
                {
                    "name": "Café Brunch",
                    "cuisine": "Breakfast/Brunch",
                    "rating": "4.7/5",
                    "reviews": 234,
                    "price": "$$",
                    "address": "987 Grove Street",
                    "hours": "7AM - 2PM",
                    "specialties": ["Pancakes", "Eggs Benedict", "Smoothie Bowls"],
                    "link": "https://www.yelp.com/search?find_desc=restaurants"
                },
                {
                    "name": "Seafood Harbour",
                    "cuisine": "Seafood",
                    "rating": "4.8/5",
                    "reviews": 289,
                    "price": "$$$",
                    "address": "159 Beach Road",
                    "hours": "5PM - 10:30PM",
                    "specialties": ["Fresh Fish", "Lobster", "Oysters"],
                    "link": "https://www.yelp.com/search?find_desc=restaurants"
                },
                {
                    "name": "La Taqueria",
                    "cuisine": "Mexican",
                    "rating": "4.7/5",
                    "reviews": 267,
                    "price": "$",
                    "address": "753 Sunset Boulevard",
                    "hours": "11AM - 11PM",
                    "specialties": ["Tacos", "Enchiladas", "Guacamole"],
                    "link": "https://www.yelp.com/search?find_desc=restaurants"
                },
                {
                    "name": "Greek Taverna",
                    "cuisine": "Greek",
                    "rating": "4.6/5",
                    "reviews": 201,
                    "price": "$$",
                    "address": "456 Aegean Way",
                    "hours": "5PM - 10:30PM",
                    "specialties": ["Moussaka", "Souvlaki", "Feta Salade"],
                    "link": "https://www.yelp.com/search?find_desc=restaurants"
                },
                {
                    "name": "BBQ Smokehouse",
                    "cuisine": "BBQ",
                    "rating": "4.7/5",
                    "reviews": 345,
                    "price": "$",
                    "address": "321 Smoke Lane",
                    "hours": "11AM - 10PM",
                    "specialties": ["Brisket", "Ribs", "Pulled Pork"],
                    "link": "https://www.yelp.com/search?find_desc=restaurants"
                }
            ]
    except Exception as e:
        return []
