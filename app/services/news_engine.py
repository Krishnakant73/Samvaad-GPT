from __future__ import annotations

import requests
import time
from typing import List, Dict
from datetime import datetime, timedelta
from cachetools import TTLCache

from app.config.settings import get_settings
from app.utils.logger import get_logger

logger = get_logger(__name__)

class AdvancedNewsEngine:

    def __init__(self):
        settings = get_settings()
        
        self.gnews_url = "https://gnews.io/api/v4/search"
        self.newsapi_url = "https://newsapi.org/v2/everything"

        # Cache: 100 queries, expires in 15 minutes
        self.cache = TTLCache(maxsize=100, ttl=900)

        self.rate_tracker = {
            "gnews_calls": 0,
            "newsapi_calls": 0
        }

    # =========================================
    # MAIN PUBLIC METHOD
    # =========================================

    def fetch_news(
        self,
        query: str,
        country: str = "in",
        breaking: bool = False,
        limit: int = 5
    ) -> List[Dict]:
        """Fetch news with intelligent API switching for real-time coverage."""
        
        # Smart Query Enhancement
        query = self._enhance_query(query, breaking)
        
        # Dynamic Date Filter based on query type
        from_date = self._get_date_filter(breaking)
        
        # Cache Check
        cache_key = f"{query}_{country}_{breaking}"
        if cache_key in self.cache:
            logger.info(f"Cache hit for query: {query}")
            return self.cache[cache_key]

        articles = []
        
        # For recent/breaking news: Try NewsAPI first (better real-time coverage)
        if breaking:
            articles = self._retry_fetch(
                lambda: self._fetch_newsapi(query, country, from_date, limit)
            )
            if articles:
                logger.info(f"NewsAPI success for breaking news: {query}")
                self.cache[cache_key] = articles
                return articles
        
        # For regular news: Try GNews first (better quality)
        articles = self._retry_fetch(
            lambda: self._fetch_gnews(query, country, from_date, limit)
        )
        
        if articles:
            self.cache[cache_key] = articles
            logger.info(f"GNews success for query: {query}")
            return articles

        # Fallback to NewsAPI
        if not breaking:  # Already tried NewsAPI if breaking
            articles = self._retry_fetch(
                lambda: self._fetch_newsapi(query, country, from_date, limit)
            )
            
            if articles:
                self.cache[cache_key] = articles
                logger.info(f"NewsAPI fallback success for query: {query}")
                return articles

        logger.warning(f"No articles found for query: {query}")
        return []

    # =========================================
    # SMART QUERY ENHANCER
    # =========================================

    def _enhance_query(self, query: str, breaking: bool) -> str:
        if breaking:
            return f"{query} breaking news latest updates"
        return f"{query} latest news"

    # =========================================
    # DATE FILTER
    # =========================================

    def _get_date_filter(self, breaking: bool) -> str:
        """Get date filter optimized for news freshness."""
        if breaking:
            # For breaking news: last 6 hours for better coverage
            return (datetime.utcnow() - timedelta(hours=6)).strftime("%Y-%m-%dT%H:%M:%SZ")
        # For regular news: last 24 hours
        return (datetime.utcnow() - timedelta(days=1)).strftime("%Y-%m-%d")

    # =========================================
    # RETRY LOGIC
    # =========================================

    def _retry_fetch(self, func, retries=2):
        for attempt in range(retries):
            try:
                result = func()
                if result:
                    return result
                if attempt < retries - 1:
                    time.sleep(1)
            except Exception as e:
                logger.warning(f"Retry {attempt + 1} failed: {e}")
                if attempt < retries - 1:
                    time.sleep(1)
        return []

    # =========================================
    # GNEWS FETCH
    # =========================================

    def _fetch_gnews(self, query, country, from_date, limit):
        settings = get_settings()
        
        if not settings.gnews_api_key:
            logger.warning("GNews API key not configured")
            return []

        params = {
            "q": query,
            "lang": "en",
            "country": country,
            "max": limit,
            "from": from_date,
            "token": settings.gnews_api_key
        }

        try:
            response = requests.get(self.gnews_url, params=params, timeout=10)

            if response.status_code != 200:
                logger.warning(f"GNews API error: {response.status_code}")
                return []

            self.rate_tracker["gnews_calls"] += 1

            data = response.json()
            return self._format_articles(data.get("articles", []))

        except Exception as e:
            logger.error(f"GNews fetch error: {e}")
            return []

    # =========================================
    # NEWSAPI FETCH
    # =========================================

    def _fetch_newsapi(self, query, country, from_date, limit):
        settings = get_settings()
        
        if not settings.newsapi_key:
            logger.warning("NewsAPI key not configured")
            return []

        params = {
            "q": query,
            "apiKey": settings.newsapi_key,
            "pageSize": limit,
            "from": from_date,
            "language": "en",
            "sortBy": "publishedAt"
        }

        try:
            response = requests.get(self.newsapi_url, params=params, timeout=10)

            if response.status_code != 200:
                logger.warning(f"NewsAPI error: {response.status_code}")
                return []

            self.rate_tracker["newsapi_calls"] += 1

            data = response.json()
            return self._format_articles(data.get("articles", []))

        except Exception as e:
            logger.error(f"NewsAPI fetch error: {e}")
            return []

    # =========================================
    # FORMATTER
    # =========================================

    def _format_articles(self, articles):
        """Format articles with complete source information for display."""
        formatted = []

        for a in articles:
            article_data = {
                "title": a.get("title", ""),
                "description": a.get("description", ""),
                "content": a.get("content", a.get("description", "")),  # Fallback to description
                "source": a.get("source", {}).get("name", "Unknown") if isinstance(a.get("source"), dict) else a.get("source", "Unknown"),
                "source_id": a.get("source", {}).get("id", ""),
                "published_at": a.get("publishedAt", ""),
                "pubDate": a.get("publishedAt", a.get("pubDate", "")),
                "url": a.get("url", ""),
                "link": a.get("url", a.get("link", ""))  # Support both url and link
            }
            formatted.append(article_data)

        return formatted
