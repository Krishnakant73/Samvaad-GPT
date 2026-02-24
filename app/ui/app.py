from __future__ import annotations

import streamlit as st
import time
from datetime import datetime
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from app.config.settings import get_settings
from app.memory.context_window import last_n_messages
from app.memory.session_manager import (
    get_messages,
    init_session_state,
)
from app.memory.sqlite_store import (
    init_db as init_db_sqlite,
    get_messages as sqlite_get_messages,
)
from app.prompts.prompt import SimplePromptBuilder
from app.services.gemini_client import GeminiClient, GeminiGenerationConfig
from app.services.response_streamer import stream_words
from app.ui.styles import apply_global_styles, chatgpt_header, chatgpt_input_placeholder
from app.utils.helpers import format_articles_for_display
from app.services.news_engine import AdvancedNewsEngine


def is_follow_up(user_input: str) -> bool:
    """Check if the user input is a follow-up question to existing context."""
    follow_up_keywords = [
        "tell me more", "what about", "how about", "and", "also",
        "more", "else", "further", "continue", "details", "explain",
        "why", "how", "when", "where", "who", "what else", "anything else"
    ]
    
    input_lower = user_input.lower().strip()
    
    # Check for follow-up keywords at start
    for keyword in follow_up_keywords:
        if input_lower.startswith(keyword):
            return True
    
    # Check for short inputs (likely follow-ups)
    if len(input_lower.split()) <= 3:
        return True
    
    # Check for pronouns indicating continuation
    pronouns = ["it", "they", "them", "this", "that", "these", "those", "he", "she"]
    first_words = input_lower.split()[:2]
    if any(p in first_words for p in pronouns):
        return True
    
    return False


def generate_chat_title(user_input: str) -> str:
    """Generate a short chat title from user input like ChatGPT does."""
    # Clean up the input
    cleaned = user_input.strip()
    
    # Remove common question words at the start
    prefixes_to_remove = [
        "what is ", "what are ", "what's ", "whats ",
        "how to ", "how do ", "how does ", "how can ", "how is ",
        "why is ", "why do ", "why does ",
        "who is ", "who are ", "who was ",
        "when is ", "when was ", "when did ",
        "where is ", "where are ", "where was ",
        "tell me about ", "explain ", "describe ",
        "can you ", "could you ", "would you ",
        "give me ", "show me ", "list ", "find ",
        "latest ", "recent ", "breaking ", "news about ",
    ]
    
    input_lower = cleaned.lower()
    for prefix in prefixes_to_remove:
        if input_lower.startswith(prefix):
            cleaned = cleaned[len(prefix):]
            break
    
    # Capitalize first letter
    cleaned = cleaned.strip()
    if cleaned:
        cleaned = cleaned[0].upper() + cleaned[1:]
    
    # Truncate to reasonable length for sidebar
    max_length = 30
    if len(cleaned) > max_length:
        # Try to break at a word boundary
        truncated = cleaned[:max_length]
        last_space = truncated.rfind(' ')
        if last_space > 10:  # Only break if we have enough content
            cleaned = truncated[:last_space]
        else:
            cleaned = truncated
        cleaned += "..."
    
    # If still empty, provide a default
    if not cleaned or len(cleaned) < 3:
        cleaned = "New Chat"
    
    return cleaned


def get_chat_display_name(chat_id: str, conversations: dict, chat_titles: dict) -> str:
    """Get the display name for a chat - either the title or a default."""
    # If we have a custom title, use it
    if chat_id in chat_titles and chat_titles[chat_id]:
        return chat_titles[chat_id]
    
    # Otherwise, check if there's a first message to derive title from
    if chat_id in conversations and conversations[chat_id]:
        for msg in conversations[chat_id]:
            if msg.get("role") == "user":
                # Generate title from first user message
                title = generate_chat_title(msg.get("content", ""))
                return title
    
    # Default fallback
    return f"Chat {chat_id}" if chat_id != "default" else "Default Chat"


def main() -> None:
    settings = get_settings()

    st.set_page_config(
        page_title="Samvaad GPT", 
        page_icon="�", 
        layout="centered",
        initial_sidebar_state="expanded"
    )
    
    apply_global_styles()
    init_session_state()
    if settings.use_sqlite:
        init_db_sqlite()
    
    # Initialize conversation memory
    if "conversations" not in st.session_state or not isinstance(st.session_state.conversations, dict):
        st.session_state.conversations = {}
    if "current_chat" not in st.session_state:
        st.session_state.current_chat = "default"
    if st.session_state.current_chat not in st.session_state.conversations:
        st.session_state.conversations[st.session_state.current_chat] = []
    
    # Initialize chat titles storage
    if "chat_titles" not in st.session_state:
        st.session_state.chat_titles = {}
    
    # Add timestamp for new conversations
    if "timestamp" not in st.session_state:
        st.session_state.timestamp = time.time()

    # ChatGPT-style header
    chatgpt_header()
    
    with st.sidebar:
        st.markdown("### 💬 Chats")
        
        # New chat button
        if st.button("New Chat", use_container_width=True, type="primary"):
            new_id = str(len(st.session_state.conversations) + 1)
            st.session_state.conversations[new_id] = []
            st.session_state.current_chat = new_id
            st.rerun()
        
        st.markdown("---")
        
        # Chat history
        st.markdown("### 📜 Chat History")
        
        # Create a scrollable container for chat history
        chat_container = st.container()
        with chat_container:
            for chat_id in st.session_state.conversations.keys():
                # Get display name for the chat
                display_name = get_chat_display_name(
                    chat_id, 
                    st.session_state.conversations, 
                    st.session_state.get("chat_titles", {})
                )
                # Full-width button for each chat
                if st.button(f"{display_name}", use_container_width=True, type="primary", key=f"chat_btn_{chat_id}"):
                    st.session_state.current_chat = chat_id
                    st.rerun()
        
        st.markdown("---")
        
        # Settings
        st.markdown("### ⚙️ Settings")
        
        model_options = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-2.0-flash-lite"]
        selected_model = st.selectbox("Model", model_options, index=0)
        st.session_state.selected_model = selected_model
        
        temperature = st.slider("Temperature", 0.0, 1.0, 0.7, 0.1)
        st.session_state.selected_temperature = temperature
        
        max_tokens = st.selectbox("Max Tokens", [800, 1200, 1500, 2000], index=1)
        st.session_state.selected_max_tokens = max_tokens
        
        # Breaking news mode
        breaking = st.toggle("Breaking News Mode")
        st.session_state.breaking_mode = breaking
        
        if st.session_state.get("is_streaming"):
            if st.button("⛔ Stop", use_container_width=True):
                st.session_state.stop_generation = True

    

    # Display messages with timestamps and sources
    messages = st.session_state.conversations[st.session_state.current_chat]
    for i, message in enumerate(messages):
        current_time = datetime.now().strftime("%H:%M")
        with st.chat_message(message["role"]):
            if message["role"] == "user":
                st.markdown(f'<div class="message-container"><div style="color: #ffffff;">{message["content"]}</div></div>', unsafe_allow_html=True)
                st.markdown(f"<div class='timestamp'>{current_time}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f'''
                <div class="message-container">
                    <div style="color: #ffffff; line-height: 1.6;">{message["content"]}</div>
                </div>
                ''', unsafe_allow_html=True)
                st.markdown(f"<div class='timestamp'>{current_time}</div>", unsafe_allow_html=True)
                
                # Show sources if they exist for this message
                if message.get("has_sources") and message.get("sources"):
                    with st.expander("📚 Sources", expanded=False):
                        st.markdown(format_articles_for_display(message["sources"]))

    # Handle pending input from suggestions
    user_input = st.chat_input("Ask about current events...", key="main_input")
    
    # Check for pending input from suggestion buttons
    if "pending_input" in st.session_state:
        user_input = st.session_state.pending_input
        del st.session_state.pending_input

    if not user_input:
        chatgpt_input_placeholder()
        return

    # Add user message
    st.session_state.conversations[st.session_state.current_chat].append({
        "role": "user",
        "content": user_input
    })
    
    # Generate chat title on first user message
    if len(st.session_state.conversations[st.session_state.current_chat]) == 1:
        chat_title = generate_chat_title(user_input)
        st.session_state.chat_titles[st.session_state.current_chat] = chat_title

    # Process message
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        # Show typing indicator
        with message_placeholder.container():
            st.markdown('<span class="typing">Thinking</span>', unsafe_allow_html=True)
        
        # Conversational Retrieval Logic
        if is_follow_up(user_input) and st.session_state.current_articles:
            # Reuse existing topic articles for follow-up
            news_articles = st.session_state.current_articles
        else:
            # New topic → fetch new articles
            st.markdown("""
<style>

/* BACKGROUND */
html, body, .stApp {
    background: linear-gradient(180deg, #0B1220 0%, #0E1117 100%) !important;
    color: #E5E7EB !important;
}

.stMarkdown, .stMarkdown p, .stMarkdown span, .stMarkdown li {
    color: #E5E7EB !important;
}

/* Remove any white background */
.main {
    background: transparent !important;
}

.block-container {
    padding-top: 2rem !important;
    padding-bottom: 120px !important;
    background: transparent !important;
}

/* Remove white content area */
section.main > div {
    background: transparent !important;
}

/* Expander content text */
[data-testid="stExpander"] * {
    color: #E5E7EB;
}

/* Sidebar Dark */
section[data-testid="stSidebar"] {
    background: #070D18 !important;
}

/* Remove weird borders */
section[data-testid="stSidebar"] > div {
    background: transparent !important;
}

/*CHAT BUBBLES*/
[data-testid="stChatMessage"] {
    border-radius: 18px;
    padding: 14px 18px;
    margin-bottom: 12px;
    backdrop-filter: blur(12px);
    animation: fadeUp 0.25s ease-out;
    transition: all 0.2s ease-in-out;
}

/* Assistant bubble */
[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-assistant"]) {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.08);
}

/* User bubble */
[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-user"]) {
    background: rgba(16,185,129,0.12);
    border: 1px solid rgba(16,185,129,0.35);
}

/* Hover elevation */
[data-testid="stChatMessage"]:hover {
    transform: translateY(-2px);
}

/* Smooth message animation */
@keyframes fadeUp {
    from {
        opacity: 0;
        transform: translateY(6px);
    }
    to {
        opacity: 1;
        transform: translateY(0px);
    }
}

/* INPUT BAR */
div[data-testid="stChatInput"] {
    position: fixed;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
    width: 65%;
    background: rgba(255,255,255,0.05);
    border-radius: 25px;
    padding: 10px 20px;
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0 0 30px rgba(16,185,129,0.15);
}

/* Remove input border */
div[data-testid="stChatInput"] input {
    border: none !important;
    background: transparent !important;
    color: white !important;
}

/* SEND BUTTON GLOW */
button[kind="secondary"] {
    border-radius: 50% !important;
    transition: all 0.2s ease-in-out !important;
}

button[kind="secondary"]:hover {
    box-shadow: 0 0 15px #10B981;
    transform: scale(1.05);
}

/* SIDEBAR MODERN */
section[data-testid="stSidebar"] button {
    border-radius: 12px !important;
    transition: all 0.2s ease-in-out;
}

/* Hover slide effect */
section[data-testid="stSidebar"] button:hover {
    background-color: rgba(255,255,255,0.08) !important;
    transform: translateX(4px);
}

/* Active focus glow */
section[data-testid="stSidebar"] button:focus {
    box-shadow: 0 0 10px #10B981;
}

/* STATUS DOT GLOW */
.status-dot {
    height: 10px;
    width: 10px;
    background-color: #10B981;
    border-radius: 50%;
    display: inline-block;
    box-shadow: 0 0 12px #10B981;
    margin-right: 8px;
}

/* TYPING INDICATOR */
.typing {
    display: inline-block;
    font-size: 14px;
    opacity: 0.6;
}

.typing::after {
    content: " .";
    animation: dots 1.5s infinite;
}

@keyframes dots {
    0% { content: " ."; }
    33% { content: " .."; }
    66% { content: " ..."; }
}

/* MINIMAL TIMESTAMP STYLE */
.timestamp {
    font-size: 11px;
    opacity: 0.35;
    margin-top: 4px;
}

</style>
""", unsafe_allow_html=True)

            # New topic → fetch new articles with advanced engine
            news_engine = AdvancedNewsEngine()
            
            # Get country and breaking mode from sidebar
            country = st.session_state.get("selected_country", "in")
            breaking = st.session_state.get("breaking_mode", False)
            
            news_articles = news_engine.fetch_news(
                query=user_input,
                country=country,
                breaking=breaking,
                limit=settings.news_fetch_limit
            )
            
            # Update topic and store articles
            st.session_state.current_topic = user_input
            st.session_state.current_articles = news_articles

        conversation = last_n_messages(get_messages(), n=settings.context_message_limit)

        # Use optimized prompt builder
        prompt_builder = SimplePromptBuilder(
            max_history_messages=settings.context_message_limit,
            max_article_chars=600
        )
        final_prompt = prompt_builder.build(
            history=conversation,
            news_articles=news_articles,
            user_query=user_input
        )

        gemini = GeminiClient(
            api_key=settings.gemini_api_key,
            config=GeminiGenerationConfig(
                model_name=settings.gemini_model, 
                max_output_tokens=settings.max_output_tokens
            ),
        )

        try:
            # Generate response
            start_time = time.time()
            full_text = gemini.generate(prompt=final_prompt)
            end_time = time.time()
            generation_time = round(end_time - start_time, 2)

            # Parse JSON response
            parsed_response = prompt_builder.parse_response(full_text)
            final_summary = parsed_response["summary"]

            # Clear typing and show streaming response
            message_placeholder.empty()
            
            # Stream the response
            streamed = ""
            for chunk in stream_words(final_summary, delay_seconds=settings.stream_delay_seconds):
                streamed = chunk
                with message_placeholder.container():
                    st.markdown(f'''
                    <div class="message-container">
                        <div style="color: #ffffff; line-height: 1.6;">{streamed}▌</div>
                    </div>
                    ''', unsafe_allow_html=True)

            # Final display without cursor
            with message_placeholder.container():
                st.markdown(f'''
                <div class="message-container">
                    <div style="color: #ffffff; line-height: 1.6;">{streamed}</div>
                    <div class="timestamp">Generated in {generation_time}s</div>
                </div>
                ''', unsafe_allow_html=True)

            # Show sources if available
            if news_articles:
                with st.expander("📚 Sources", expanded=False):
                    st.markdown(format_articles_for_display(news_articles))

            # Add assistant message to conversation with sources
            st.session_state.conversations[st.session_state.current_chat].append({
                "role": "assistant",
                "content": streamed,
                "sources": news_articles,
                "has_sources": bool(news_articles)
            })

        except Exception as e:
            with message_placeholder.container():
                st.error(f"⚠️ An error occurred: {str(e)}")
            
            # Add error message to conversation
            st.session_state.conversations[st.session_state.current_chat].append({
                "role": "assistant",
                "content": f"I encountered an error while processing your request: {str(e)}",
                "sources": [],
                "has_sources": False
            })

if __name__ == "__main__":
    main()
