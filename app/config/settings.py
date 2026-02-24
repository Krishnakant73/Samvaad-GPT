from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Literal

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:
    gemini_api_key: str
    gnews_api_key: str
    newsapi_key: str
    newsdata_api_key: str
    gemini_model: str
    max_output_tokens: int
    stream_delay_seconds: float
    context_message_limit: int
    news_fetch_limit: int
    use_advanced_pipeline: bool
    use_sqlite: bool


def get_settings() -> Settings:
    # Reload .env each call to pick up key changes without restarting
    load_dotenv(override=True)
    return Settings(
        gemini_api_key=os.getenv("GEMINI_API_KEY", "").strip(),
        gnews_api_key=os.getenv("GNEWS_API_KEY", "").strip(),
        newsapi_key=os.getenv("NEWSAPI_KEY", "").strip(),
        newsdata_api_key=os.getenv("NEWSDATA_API_KEY", "").strip(),
        gemini_model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash").strip(),
        max_output_tokens=int(os.getenv("MAX_OUTPUT_TOKENS", "1500")),
        stream_delay_seconds=float(os.getenv("STREAM_DELAY_SECONDS", "0.02")),
        context_message_limit=int(os.getenv("CONTEXT_MESSAGE_LIMIT", "5")),
        news_fetch_limit=int(os.getenv("NEWS_FETCH_LIMIT", "5")),
        use_advanced_pipeline=os.getenv("USE_ADVANCED_PIPELINE", "false").strip().lower() == "true",
        use_sqlite=os.getenv("USE_SQLITE", "false").strip().lower() == "true",
    )
