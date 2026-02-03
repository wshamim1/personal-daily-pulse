# API Integration Guide

## Overview
The application has been refactored to use real APIs instead of hard-coded data. This document explains which APIs are used, how to get keys, and how to configure them.

## Configuration Files
- **`backend/config.py`**: Centralized API configuration with all endpoints and keys
- **`.env.example`**: Template for environment variables (copy to `.env`)

## APIs Used

### 1. **Books** - Open Library API ✅ (No Key Required)
- **Endpoint**: https://openlibrary.org/api/search.json
- **What it does**: Fetches trending and searchable books
- **Cost**: Free
- **Setup**: No API key needed - works out of the box
- **Tool**: `get_trending_books()` in `tools/books_tools.py`

### 2. **Entertainment - Movies & TV** - TMDB (The Movie Database)
- **Endpoint**: https://api.themoviedb.org/3
- **What it does**: Trending movies, now playing, TV shows, search
- **Cost**: Free
- **Required Key**: Yes - `TMDB_API_KEY`
- **Setup**:
  1. Visit https://www.themoviedb.org/settings/api
  2. Sign up for a free account
  3. Generate an API key
  4. Add to `.env`: `TMDB_API_KEY=your_key_here`
- **Tools**: 
  - `get_trending_movies()`
  - `get_now_playing_movies()`
  - `get_trending_shows()`
  - `search_movies(query)`

### 3. **Weather** - OpenWeatherMap API
- **Endpoint**: https://api.openweathermap.org/data/2.5
- **Fallback**: wttr.in (free, no key required)
- **Cost**: Free tier available
- **Required Key**: `OPENWEATHER_API_KEY` (optional - wttr.in fallback)
- **Setup**:
  1. Visit https://openweathermap.org/api
  2. Create a free account
  3. Get your API key from dashboard
  4. Add to `.env`: `OPENWEATHER_API_KEY=your_key_here`
- **Tool**: `get_local_weather(units='C')` in `tools/utility_tools.py`

### 4. **Quotes** - Quotable API ✅ (No Key Required)
- **Endpoint**: https://api.quotable.io/random
- **What it does**: Random inspirational quotes
- **Cost**: Free
- **Setup**: No API key needed
- **Tool**: `get_quote_of_day()` in `tools/entertainment_tools.py`

### 5. **Restaurants & Food** - Yelp API
- **Endpoint**: https://api.yelp.com/v3
- **What it does**: Restaurant search, ratings, prices
- **Cost**: Free tier available
- **Required Key**: Yes - `YELP_API_KEY`
- **Setup**:
  1. Visit https://www.yelp.com/developers/v3/manage_app
  2. Create an app
  3. Get your API key
  4. Add to `.env`: `YELP_API_KEY=your_key_here`
- **Tool**: `get_best_food(cuisine)` in `tools/entertainment_tools.py`

### 6. **Fashion** - Vogue RSS Feed (Using feedparser)
- **Source**: https://www.vogue.com/feed/rss
- **What it does**: Latest fashion trends
- **Cost**: Free
- **Setup**: Install `feedparser` (optional): `pip install feedparser`
- **Note**: Currently returns mock data (RSS parsing in progress)

### 7. **Gas Prices** - GasBuddy Alternative
- **Status**: Mock data only currently
- **Note**: GasBuddy API requires special access
- **Alternative**: Implement with free alternatives or user input
- **Tool**: `get_cheapest_gas(zipcode)` in `tools/utility_tools.py`

### 8. **Shopping** - Store Product APIs
- **Status**: Mock curated data
- **Note**: Amazon, Walmart, Target require affiliate programs
- **Tool**: `get_store_products(store, category)` in `tools/utility_tools.py`

## Setup Instructions

### Step 1: Copy Environment Template
```bash
cp .env.example .env
```

### Step 2: Get API Keys
1. **TMDB** (Movies):
   - Visit: https://www.themoviedb.org/settings/api
   - Create account → Request API key → Copy v3 auth token

2. **OpenWeatherMap** (Weather):
   - Visit: https://openweathermap.org/api
   - Sign up → Get free API key → Copy it

3. **Yelp** (Restaurants):
   - Visit: https://www.yelp.com/developers/v3/manage_app
   - Create app → Get Client ID and API Key

4. **News** (Optional):
   - Visit: https://newsapi.org/
   - Register → Get API key

### Step 3: Update `.env` File
```env
GROQ_API_KEY=your_groq_key
TMDB_API_KEY=your_tmdb_key
OPENWEATHER_API_KEY=your_weather_key
YELP_API_KEY=your_yelp_key
DEFAULT_LOCATION=New York, NY
DEFAULT_COUNTRY=US
```

### Step 4: Restart Backend
```bash
# In backend directory
python app.py
```

## Default Fallbacks
All tools have built-in fallbacks to mock data when:
- API keys are not configured
- APIs are temporarily unavailable
- Network errors occur

This ensures the app always works, even without API keys.

## Adding New APIs

To integrate a new API:

1. **Update `config.py`**:
   ```python
   NEW_API_KEY = os.getenv("NEW_API_KEY", "")
   NEW_API_BASE_URL = "https://api.example.com/v1"
   ```

2. **Create/Update tool**:
   ```python
   @tool
   def get_new_data():
       try:
           if not APIConfig.NEW_API_KEY:
               return _get_default_data()
           
           url = f"{APIConfig.NEW_API_BASE_URL}/endpoint"
           response = requests.get(url, headers={...}, timeout=10)
           # Process response
       except Exception as e:
           return _get_default_data()
   
   def _get_default_data():
       return [...]  # Fallback data
   ```

3. **Add to `.env.example`**:
   ```
   NEW_API_KEY=your_new_api_key_here
   ```

## API Status

| API | Status | Key Required | Free Tier |
|-----|--------|--------------|-----------|
| Open Library (Books) | ✅ Active | No | Yes |
| TMDB (Movies/TV) | ✅ Active | Yes | Yes |
| OpenWeatherMap (Weather) | ✅ Active | Optional* | Yes |
| Quotable (Quotes) | ✅ Active | No | Yes |
| Yelp (Restaurants) | ✅ Integrated | Yes | Yes |
| wttr.in (Weather Fallback) | ✅ Active | No | Yes |
| Vogue RSS (Fashion) | ⚠️ Mock Data | No | Yes |
| GasBuddy (Gas) | ⚠️ Mock Data | N/A | Limited |
| Shopping (Products) | ⚠️ Mock Data | N/A | N/A |

*Weather has free fallback (wttr.in), but OpenWeatherMap key provides better accuracy

## Troubleshooting

### API Key Issues
```python
# Check if keys are loaded
python -c "from config import APIConfig; print(APIConfig.get_config())"
```

### Network Issues
- Check internet connection
- Verify API endpoint URLs in `config.py`
- Check firewall/proxy settings

### Rate Limiting
- Most free APIs have rate limits
- Implement caching for frequently-called endpoints
- Consider upgrading to paid tiers for production

## Production Recommendations

1. **Use environment variables** - Never commit API keys to git
2. **Implement caching** - Cache API responses to reduce requests
3. **Add error handling** - Already implemented with fallbacks
4. **Monitor usage** - Track API calls to avoid rate limits
5. **Rotate keys** - Periodically refresh API keys for security
