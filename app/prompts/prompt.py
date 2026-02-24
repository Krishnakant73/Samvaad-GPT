from __future__ import annotations

from typing import List, Dict, Any
import json
import re


class PromptBuilder:

    def __init__(
        self,
        max_history_messages: int = 6,
        max_article_chars: int = 800,
        max_articles: int = 5,
        summarize_after: int = 10,
    ):
        self.max_history_messages = max_history_messages
        self.max_article_chars = max_article_chars
        self.max_articles = max_articles
        self.summarize_after = summarize_after

   
    def build(
        self,
        history: List[Dict[str, str]],
        news_articles: List[Dict[str, Any]],
        user_query: str,
    ) -> str:

        compressed_history = self._compress_history_if_needed(history)
        formatted_history = self._format_history(compressed_history)
        ranked_articles = self._rank_articles(news_articles, user_query)
        formatted_news = self._format_news(ranked_articles)

        return f"""
You are NewsGPT — a professional real-time news intelligence assistant.


CORE RULES (STRICT)

1. Use ONLY the provided articles as factual evidence.
2. Never use prior knowledge.
3. Never speculate or infer beyond text.
4. If something is missing, explicitly say:
   "This information is not specified in the provided articles."
5. Maintain neutral, journalistic tone.
6. Return a single valid JSON object only. No code blocks or extra text.


ADVANCED ANALYSIS TASKS

Step 1: Intent Detection
- Determine whether this is:
  • Follow-up on same event
  • Clarification
  • New topic
  • Comparative query

Step 2: Event Anchoring
- Identify core event/topic.
- Restrict analysis strictly to that event.

Step 3: Evidence Mapping
- Extract ONLY directly stated facts.
- Cite supporting details clearly in narrative form.

Step 4: Information Gaps
- Clearly state when details are absent.

Step 5: Risk Check
- Avoid assumptions.
- Avoid predictive claims unless explicitly mentioned.


OUTPUT STRUCTURE


Return exactly one JSON object with the following fields:
- intent: one of "follow_up", "clarification", "new_topic", "comparative"
- core_topic: a short phrase naming the event/topic
- used_articles: array of integers referencing the Article numbers used
- summary: a cohesive answer that covers headline summary, key developments,
  detailed explanation, why it matters, and what is not specified. Keep a
  neutral tone and ground statements in the provided articles.
- confidence: "High" | "Medium" | "Low" based on article completeness


CONTEXT


Conversation History:
{formatted_history}

Articles:
{formatted_news}

User Question:
{user_query}
""".strip()

   
    # HISTORY FORMATTER
   

    def _compress_history_if_needed(self, history: List[Dict[str, str]]) -> List[Dict[str, str]]:
        if not history:
            return []
        if len(history) <= self.summarize_after:
            return history[-self.max_history_messages:]
        old_messages = history[:-self.max_history_messages]
        recent_messages = history[-self.max_history_messages:]
        summary = self._generate_summary_text(old_messages)
        return [{"role": "system", "content": f"Conversation Summary Memory:\n{summary}"}] + recent_messages

    def build_summary_prompt(self, messages: List[Dict[str, str]]) -> str:
        conversation_text = "\n".join(
            f"{m.get('role', '').upper()}: {m.get('content', '')}".strip()
            for m in messages
        ).strip()
        return f"""
You compress conversations into concise memory blocks.

Rules:
- Preserve key facts, entities, and user intent.
- Remove repetition and filler.
- Neutral, factual style under 200 words.

Conversation:
{conversation_text}

Return only the summary text.
""".strip()

    def _generate_summary_text(self, old_messages: List[Dict[str, str]]) -> str:
        if not old_messages:
            return ""
        try:
            from app.config.settings import get_settings
            from app.services.gemini_client import GeminiClient, GeminiGenerationConfig
            settings = get_settings()
            if not settings.gemini_api_key:
                raise RuntimeError("missing_key")
            prompt = self.build_summary_prompt(old_messages)
            client = GeminiClient(
                api_key=settings.gemini_api_key,
                config=GeminiGenerationConfig(
                    model_name=settings.gemini_model,
                    max_output_tokens=200,
                    temperature=0.3,
                ),
            )
            text = client.generate(prompt=prompt).strip()
            if not text:
                raise RuntimeError("empty_summary")
            if len(text) > 900:
                text = text[:900].rstrip() + "..."
            return text
        except Exception:
            first_user = next((m.get("content", "") for m in old_messages if m.get("role") == "user"), "")
            last_assistant = next((m.get("content", "") for m in reversed(old_messages) if m.get("role") == "assistant"), "")
            parts = []
            if first_user:
                parts.append(f"User intent: {first_user}")
            if last_assistant:
                parts.append(f"Assistant provided: {last_assistant}")
            summary = "\n".join(parts).strip()
            if len(summary) > 900:
                summary = summary[:900].rstrip() + "..."
            return summary or "Earlier discussion summarized."

    def _format_history(self, history: List[Dict[str, str]]) -> str:
        if not history:
            return "No prior conversation."

        trimmed = history[-self.max_history_messages:]

        formatted = []
        for msg in trimmed:
            role = msg.get("role", "").upper()
            content = msg.get("content", "").strip()
            formatted.append(f"{role}: {content}")

        return "\n".join(formatted)

    
# ARTICLE RANKING (Relevance Boost)
    def _rank_articles(
        self,
        articles: List[Dict[str, Any]],
        query: str
    ) -> List[Dict[str, Any]]:

        if not articles:
            return []

        query_keywords = set(re.findall(r"\w+", query.lower()))

        def score(article):
            text = (
                (article.get("title") or "") +
                (article.get("description") or "") +
                (article.get("content") or "")
            ).lower()

            matches = sum(1 for word in query_keywords if word in text)
            return matches

        ranked = sorted(articles, key=score, reverse=True)

        return ranked[:self.max_articles]

    
    # ARTICLE FORMATTERs
    

    def _format_news(self, articles: List[Dict[str, Any]]) -> str:
        if not articles:
            return "No relevant news articles retrieved."

        formatted_blocks = []

        for idx, article in enumerate(articles, 1):
            content = (article.get("content") or "")[:self.max_article_chars]

            formatted_blocks.append(f"""
Article {idx}:
Title: {article.get("title")}
Description: {article.get("description")}
Content: {content}
Source: {article.get("source_id") or article.get("source")}
Published At: {article.get("pubDate") or article.get("published_at")}
Link: {article.get("link")}
----------------------------------------
""")

        return "\n".join(formatted_blocks).strip()

    
    # SAFE RESPONSE PARSE
    

    def parse_response(self, llm_response: str) -> Dict[str, Any]:

        if not llm_response.strip():
            return self._fallback_response("Empty response.")

        try:
            response_dict = json.loads(llm_response)

            required_fields = [
                "intent",
                "core_topic",
                "used_articles",
                "summary",
                "confidence"
            ]

            for field in required_fields:
                response_dict.setdefault(field, "")

            return response_dict

        except json.JSONDecodeError:
            return {
                "intent": "analysis",
                "core_topic": "",
                "used_articles": [],
                "summary": llm_response.strip(),
                "confidence": "Medium"
            }

    def _fallback_response(self, message: str) -> Dict[str, Any]:
        return {
            "intent": "error",
            "core_topic": "",
            "used_articles": [],
            "summary": message,
            "confidence": "Low"
        }


class SimplePromptBuilder:
    """A simplified prompt builder for normal conversational text output (like ChatGPT)."""

    def __init__(
        self,
        max_history_messages: int = 6,
        max_article_chars: int = 800,
        max_articles: int = 5,
    ):
        self.max_history_messages = max_history_messages
        self.max_article_chars = max_article_chars
        self.max_articles = max_articles

    def build(
        self,
        history: List[Dict[str, str]],
        news_articles: List[Dict[str, Any]],
        user_query: str,
    ) -> str:

        formatted_history = self._format_history(history)
        formatted_news = self._format_news(news_articles)

        return f"""You are Samvaad GPT — a helpful, conversational news assistant.

Your job is to provide clear, natural-sounding responses about current events.

RULES:
1. Answer based ONLY on the provided news articles
2. Be conversational and friendly (like ChatGPT)
3. If information is missing, say so honestly
4. Keep a neutral, factual tone
5. Don't use JSON or structured formats — just plain text

CONVERSATION HISTORY:
{formatted_history}

NEWS ARTICLES:
{formatted_news}

USER QUESTION: {user_query}

Provide a helpful, natural response:""".strip()

    def _format_history(self, history: List[Dict[str, str]]) -> str:
        if not history:
            return "No prior conversation."

        trimmed = history[-self.max_history_messages:]
        formatted = []
        for msg in trimmed:
            role = msg.get("role", "").upper()
            content = msg.get("content", "").strip()
            formatted.append(f"{role}: {content}")

        return "\n".join(formatted)

    def _format_news(self, articles: List[Dict[str, Any]]) -> str:
        if not articles:
            return "No relevant news articles retrieved."

        formatted_blocks = []
        for idx, article in enumerate(articles, 1):
            content = (article.get("content") or "")[:self.max_article_chars]

            formatted_blocks.append(f"""
Article {idx}:
Title: {article.get("title")}
Description: {article.get("description")}
Content: {content}
Source: {article.get("source_id") or article.get("source")}
Published: {article.get("pubDate") or article.get("published_at")}
""")

        return "\n".join(formatted_blocks).strip()

    def parse_response(self, llm_response: str) -> Dict[str, Any]:
        """Return the response directly as plain text without JSON parsing."""
        return {
            "intent": "conversation",
            "core_topic": "",
            "used_articles": [],
            "summary": llm_response.strip(),
            "confidence": "High"
        }


# System prompt for news assistant
SYSTEM_PROMPT = """You are NewsGPT, a professional real-time news intelligence assistant.

ROLE:
You provide accurate, neutral, and structured news analysis strictly based on the provided news context.

CONSTRAINTS:
- Only use the supplied news articles as your knowledge source.
- Do NOT use prior knowledge.
- Do NOT hallucinate facts.
- If the answer is not present in the context, clearly say:
  "The provided news data does not contain information about this."
- Maintain a neutral and journalistic tone.
- Avoid personal opinions.
- Avoid speculation.

CONVERSATION MEMORY:
You will be provided previous conversation history.
Use it to understand follow-up questions and references.
However, always ground your response in the latest provided news context.

RESPONSE FORMAT:

If the user asks for:
1) Summary -> Provide:
   - Headline Overview
   - Key Developments
   - Important Entities (Companies, Countries, People)
   - Potential Impact

2) Specific Question -> Provide:
   - Direct Answer
   - Supporting Details from Articles
   - Source Mentions (Article titles)

3) Comparative Question -> Provide:
   - Structured comparison
   - Bullet points
   - Clear distinctions

STYLE:
- Clear
- Structured
- Professional
- Concise but informative
- Use bullet points where helpful

SAFETY:
- If asked for harmful or political persuasion content, respond neutrally.
- If news context is empty, politely inform the user that no relevant real-time news was found.

Always prioritize factual accuracy over completeness."""
