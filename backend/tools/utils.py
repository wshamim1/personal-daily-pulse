"""Utility functions for LangChain tools with caching and async support."""

import json
import time
import httpx
import xml.etree.ElementTree as ET
from typing import Dict, Any, List, Optional
from functools import lru_cache

# Simple in-memory cache with TTL
_cache = {}
_cache_ttl = {}
DEFAULT_CACHE_TTL = 300  # 5 minutes

def _get_cached(key: str, ttl: int = DEFAULT_CACHE_TTL) -> Optional[Any]:
    """Get cached value if not expired."""
    if key in _cache and key in _cache_ttl:
        if time.time() < _cache_ttl[key]:
            return _cache[key]
        else:
            # Expired, remove from cache
            del _cache[key]
            del _cache_ttl[key]
    return None

def _set_cached(key: str, value: Any, ttl: int = DEFAULT_CACHE_TTL):
    """Set cached value with TTL."""
    _cache[key] = value
    _cache_ttl[key] = time.time() + ttl

def fetch_json(url: str, headers: dict = None, timeout: int = 5) -> dict:
    """Fetch JSON from URL with caching."""
    cache_key = f"json:{url}"
    cached = _get_cached(cache_key)
    if cached is not None:
        return cached
    
    try:
        with httpx.Client(timeout=timeout) as client:
            headers = headers or {"User-Agent": "daily-log-api-langchain/2.0"}
            response = client.get(url, headers=headers, follow_redirects=True)
            response.raise_for_status()
            data = response.json()
            _set_cached(cache_key, data)
            return data
    except Exception as e:
        # Return cached data even if expired, better than nothing
        if cache_key in _cache:
            return _cache[cache_key]
        raise

def fetch_text(url: str, timeout: int = 5) -> str:
    """Fetch text from URL with caching."""
    cache_key = f"text:{url}"
    cached = _get_cached(cache_key)
    if cached is not None:
        return cached
    
    try:
        with httpx.Client(timeout=timeout) as client:
            headers = {"User-Agent": "daily-log-api-langchain/2.0"}
            response = client.get(url, headers=headers, follow_redirects=True)
            response.raise_for_status()
            text = response.text
            _set_cached(cache_key, text)
            return text
    except Exception as e:
        if cache_key in _cache:
            return _cache[cache_key]
        raise

def fetch_xml(url: str, timeout: int = 5) -> str:
    """Fetch XML from URL with caching."""
    cache_key = f"xml:{url}"
    cached = _get_cached(cache_key)
    if cached is not None:
        return cached
    
    try:
        with httpx.Client(timeout=timeout) as client:
            headers = {"User-Agent": "daily-log-api-langchain/2.0"}
            response = client.get(url, headers=headers, follow_redirects=True)
            response.raise_for_status()
            xml = response.text
            _set_cached(cache_key, xml)
            return xml
    except Exception as e:
        if cache_key in _cache:
            return _cache[cache_key]
        raise

def parse_rss(xml_text: str) -> List[Dict[str, Any]]:
    """Parse RSS feed to list of items."""
    try:
        root = ET.fromstring(xml_text)
        channel = root.find("channel")
        if not channel:
            for child in root:
                if "channel" in child.tag:
                    channel = child
                    break
        
        items = []
        if channel:
            for item in channel.findall("item") or []:
                title_el = item.find("title")
                link_el = item.find("link")
                pub_el = item.find("pubDate")
                
                items.append({
                    "title": title_el.text if title_el is not None else "",
                    "link": link_el.text if link_el is not None else "",
                    "pubDate": pub_el.text if pub_el is not None else "",
                })
        
        return items
    except Exception as e:
        raise ValueError(f"Failed to parse RSS: {str(e)}")
