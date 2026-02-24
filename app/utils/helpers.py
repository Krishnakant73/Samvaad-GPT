from __future__ import annotations

from typing import Dict, Iterable, List


def guess_news_query(user_text: str) -> Dict[str, str]:
    return {"keyword": (user_text or "").strip()}


def format_articles_for_display(articles: Iterable[Dict[str, str]]) -> str:
    """Format articles as markdown with clickable source links."""
    lines: List[str] = []
    for idx, a in enumerate(articles, 1):
        title = (a.get("title") or "").strip()
        link = (a.get("link") or a.get("url") or "").strip()
        source = (a.get("source") or a.get("source_id") or "Unknown").strip()
        
        if not title:
            continue
            
        if link:
            # Create clickable markdown link
            lines.append(f"{idx}. **[{title}]({link})** — *{source}*")
        else:
            lines.append(f"{idx}. **{title}** — *{source}*")
            
    return "\n\n".join(lines) if lines else "No sources available."
