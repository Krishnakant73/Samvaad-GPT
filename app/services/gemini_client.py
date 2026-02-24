from __future__ import annotations

import time
from dataclasses import dataclass

import google.generativeai as genai

from app.utils.logger import get_logger


logger = get_logger(__name__)


@dataclass(frozen=True)
class GeminiGenerationConfig:
    model_name: str
    max_output_tokens: int = 1500
    temperature: float = 0.7


class GeminiClient:
    def __init__(self, *, api_key: str, config: GeminiGenerationConfig):
        self._api_key = api_key
        self._config = config

        if self._api_key:
            genai.configure(api_key=self._api_key)

    def generate(self, *, prompt: str) -> str:
        if not self._api_key:
            logger.warning("GEMINI_API_KEY is missing; returning fallback response")
            return "Gemini API key is not configured. Please set GEMINI_API_KEY in your .env file."

        candidates_models = [self._config.model_name, "gemini-1.5-flash"]
        last_error_msg = ""
        for model_name in candidates_models:
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    model = genai.GenerativeModel(model_name)
                    response = model.generate_content(
                        prompt,
                        generation_config=genai.types.GenerationConfig(
                            max_output_tokens=self._config.max_output_tokens,
                            temperature=self._config.temperature,
                        ),
                    )
                    text = getattr(response, "text", None)
                    if isinstance(text, str) and text.strip():
                        return text.strip()
                    try:
                        candidates = getattr(response, "candidates", None)
                        if candidates:
                            return str(candidates[0]).strip()
                    except Exception:
                        logger.exception("Gemini response parsing failed")
                    return "I couldn't parse a response from Gemini. Please try again."
                except Exception as e:
                    logger.exception(f"Gemini generation failed for model {model_name} (attempt {attempt + 1}/{max_retries})")
                    error_msg = str(e)
                    last_error_msg = error_msg
                    lower = error_msg.lower()
                    if "timeout" in lower or "failed to connect" in lower or "503" in error_msg:
                        if attempt < max_retries - 1:
                            wait_time = 2 ** attempt
                            time.sleep(wait_time)
                            continue
                        break
                    if "429" in error_msg or "quota" in lower or "resource exhausted" in lower:
                        if attempt < max_retries - 1:
                            wait_time = 2 ** attempt
                            logger.info(f"Quota exceeded, retrying in {wait_time} seconds...")
                            time.sleep(wait_time)
                            continue
                        return "⚠️ Gemini API quota exceeded. Please try again later or upgrade your plan."
                    if "404" in error_msg or "not found" in lower:
                        break
                    if ("permission" in lower or "forbidden" in lower or "unauthorized" in lower or "invalid api key" in lower or "401" in error_msg):
                        return "⚠️ Gemini API permission denied. Please check your API key."
                    if attempt < max_retries - 1:
                        wait_time = 1
                        logger.info(f"API error, retrying in {wait_time} seconds...")
                        time.sleep(wait_time)
                        continue
                    break
        if "404" in last_error_msg or "not found" in last_error_msg.lower():
            return "⚠️ Gemini model not available. Falling back failed. Please set a supported model."
        if ("permission" in last_error_msg.lower() or "forbidden" in last_error_msg.lower() or "unauthorized" in last_error_msg.lower() or "invalid api key" in last_error_msg.lower() or "401" in last_error_msg):
            return "⚠️ Gemini API permission denied. Please check your API key."
        if "timeout" in last_error_msg.lower() or "failed to connect" in last_error_msg.lower() or "503" in last_error_msg:
            return "⚠️ Gemini is temporarily unreachable. Please try again in a moment."
        if "429" in last_error_msg or "quota" in last_error_msg.lower() or "resource exhausted" in last_error_msg.lower():
            return "⚠️ Gemini API quota exceeded. Please try again later or upgrade your plan."
        return "⚠️ Gemini service error. Please try again shortly."
