from __future__ import annotations

from typing import Dict, List, Optional

import streamlit as st
import time
import json
import os


def init_session_state() -> None:
    """Initialize all session state variables to prevent data loss."""
    # Messages for current conversation
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Streaming state
    if "is_streaming" not in st.session_state:
        st.session_state.is_streaming = False
    if "stop_generation" not in st.session_state:
        st.session_state.stop_generation = False
    
    # Current topic context
    if "current_topic" not in st.session_state:
        st.session_state.current_topic = None
    if "current_articles" not in st.session_state:
        st.session_state.current_articles = []
    
    # Conversation storage - dictionary format with chat_id keys
    if "conversations" not in st.session_state:
        st.session_state.conversations = {}
    
    # Ensure default conversation exists
    if "default" not in st.session_state.conversations:
        st.session_state.conversations["default"] = []
    
    # Current active chat
    if "current_chat" not in st.session_state:
        st.session_state.current_chat = "default"
    
    # Chat titles storage
    if "chat_titles" not in st.session_state:
        st.session_state.chat_titles = {}
    
    # Timestamp for conversation ordering
    if "timestamp" not in st.session_state:
        st.session_state.timestamp = time.time()
    
    # API configuration (persist user preferences)
    if "selected_model" not in st.session_state:
        st.session_state.selected_model = "gemini-2.0-flash"
    if "selected_temperature" not in st.session_state:
        st.session_state.selected_temperature = 0.7
    if "selected_max_tokens" not in st.session_state:
        st.session_state.selected_max_tokens = 1500
    if "selected_country" not in st.session_state:
        st.session_state.selected_country = "in"
    if "breaking_mode" not in st.session_state:
        st.session_state.breaking_mode = False


def add_message(role: str, content: str) -> None:
    """Add a message to the current conversation."""
    message = {"role": role, "content": content, "timestamp": time.time()}
    st.session_state.messages.append(message)
    
    # Also sync to conversations dict to ensure persistence
    current_chat = st.session_state.get("current_chat", "default")
    if current_chat not in st.session_state.conversations:
        st.session_state.conversations[current_chat] = []
    st.session_state.conversations[current_chat].append(message)


def get_messages() -> List[Dict[str, str]]:
    """Get messages for the current chat."""
    current_chat = st.session_state.get("current_chat", "default")
    return list(st.session_state.conversations.get(current_chat, []))


def clear_messages() -> None:
    """Clear messages for the current conversation."""
    st.session_state.messages = []
    current_chat = st.session_state.get("current_chat", "default")
    if current_chat in st.session_state.conversations:
        st.session_state.conversations[current_chat] = []


def save_current_conversation_to_history() -> None:
    """Persist the current chat to disk."""
    messages = get_messages()
    if not messages:
        return
    
    # Get title from first user message
    first_user = next((m for m in messages if m.get("role") == "user"), None)
    title = (first_user.get("content") if first_user else "Conversation") or "Conversation"
    title = (title[:60] + "...") if len(title) > 60 else title
    
    # Save to history file
    history_entry = {
        "id": int(time.time() * 1000),
        "title": title,
        "messages": messages,
        "timestamp": time.time(),
    }
    
    # Load existing history
    history = _load_history()
    history.append(history_entry)
    _persist_history(history)


def start_new_conversation() -> None:
    """Start a fresh conversation."""
    save_current_conversation_to_history()
    st.session_state.messages = []
    st.session_state.current_topic = None
    st.session_state.current_articles = []
    st.session_state.current_chat = "default"


def list_conversations() -> List[Dict[str, str]]:
    """Return saved conversations from disk."""
    return _load_history()


def load_conversation(conversation_id: int) -> None:
    """Load a saved conversation."""
    items = list_conversations()
    match = next((c for c in items if c.get("id") == conversation_id), None)
    if not match:
        return
    
    messages = list(match.get("messages", []))
    st.session_state.messages = messages
    
    # Also load into conversations dict
    current_chat = st.session_state.get("current_chat", "default")
    st.session_state.conversations[current_chat] = messages


def delete_conversation(conversation_id: int) -> None:
    """Remove a saved conversation."""
    history = _load_history()
    history = [c for c in history if c.get("id") != conversation_id]
    _persist_history(history)


def _history_path() -> str:
    """Get path to history file."""
    base = os.path.join(os.getcwd(), "logs")
    os.makedirs(base, exist_ok=True)
    return os.path.join(base, "chat_history.json")


def _load_history() -> List[Dict[str, str]]:
    """Read saved conversations from disk."""
    path = _history_path()
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except Exception:
        return []


def _persist_history(items: List[Dict[str, str]]) -> None:
    """Write conversations to disk."""
    path = _history_path()
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(items, f, ensure_ascii=False, indent=2)
    except Exception:
        pass
