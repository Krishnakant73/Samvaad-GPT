from __future__ import annotations

import streamlit as st


def apply_global_styles() -> None:
    """Apply production-ready ChatGPT-style dark theme."""
    st.markdown(
        """
        <style>
        /*  BASE THEME  */
        .stApp { 
            background: linear-gradient(180deg, #0E1117 0%, #111827 100%); 
        }
        .stApp::before { 
            content: ""; 
            position: fixed; 
            inset: 0; 
            background-image: url("https://www.transparenttextures.com/patterns/noise.png"); 
            opacity: 0.03; 
            pointer-events: none; 
            z-index: 0; 
        }
        
        /*  LAYOUT  */
        .block-container { 
            padding-top: 2rem !important; 
            padding-bottom: 9rem !important; 
        }
        .main {
            padding-top: 2rem;
            max-width: 850px;
            margin: 0 auto;
        }
        
        /*  CHAT MESSAGES  */
        [data-testid="stChatMessage"] { 
            border-radius: 18px; 
            padding: 14px 18px; 
            margin-bottom: 12px; 
            backdrop-filter: blur(12px); 
            animation: fadeUp 0.25s ease-out; 
            transition: all 0.2s ease-in-out;
            max-width: 800px;
            margin-left: auto;
            margin-right: auto;
        }
        [data-testid="stChatMessage"]:hover { 
            transform: translateY(-2px); 
        }
        [data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-user"]) { 
            background: rgba(16, 185, 129, 0.12); 
            border: 1px solid rgba(16, 185, 129, 0.35); 
        }
        [data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-assistant"]) { 
            background: rgba(255, 255, 255, 0.05); 
            border: 1px solid rgba(255, 255, 255, 0.08); 
        }
        [data-testid="stChatMessage"] p, 
        [data-testid="stChatMessage"] div { 
            overflow-wrap: anywhere; 
            word-break: break-word; 
        }
        
        /*  TYPOGRAPHY  */
        html, body {
            background: #0E1117 !important;
            color: #E5E7EB !important;
        }
        .stMarkdown, .stMarkdown p, .stMarkdown span, .stMarkdown li {
            color: #E5E7EB !important;
        }
        
        /*  INPUT BAR  */
        div[data-testid="stChatInput"] { 
            position: fixed; 
            bottom: 20px; 
            left: 50%; 
            transform: translateX(-50%); 
            width: 65%; 
            max-width: 850px;
            background: rgba(255,255,255,0.05); 
            border-radius: 25px; 
            padding: 10px 20px; 
            backdrop-filter: blur(20px); 
            box-shadow: 0 0 30px rgba(16,185,129,0.15); 
            border: 1px solid rgba(255,255,255,0.08); 
        }
        div[data-testid="stChatInput"] input { 
            border: none !important; 
            background: transparent !important; 
            color: white !important; 
        }
        .stChatInput > div > div > textarea {
            background: transparent;
            border: 1px solid rgba(255,255,255,0.12);
            border-radius: 12px;
            padding: 12px 16px;
            font-size: 16px;
            resize: none;
            color: #E5E7EB;
        }
        .stChatInput > div > div > textarea:focus {
            border-color: rgba(16,185,129,0.75);
            box-shadow: 0 0 0 2px rgba(16,185,129,0.18);
        }
        
        /*  BUTTONS  */
        button { 
            border-radius: 8px !important; 
            transition: all 0.2s ease-in-out !important; 
        }
        button:hover { 
            box-shadow: 0 0 10px #10B981; 
        }
        button[kind="secondary"] { 
            border-radius: 50% !important; 
            height: 48px !important; 
            width: 48px !important; 
            transition: all 0.2s ease-in-out !important; 
        }
        button[kind="secondary"]:hover { 
            box-shadow: 0 0 15px #10B981; 
            transform: scale(1.05); 
        }
        
        /*  SIDEBAR  */
        section[data-testid="stSidebar"] { 
            background: #0B0F15; 
        }
        section[data-testid="stSidebar"] button { 
            border-radius: 12px !important; 
            transition: all 0.2s ease-in-out; 
        }
        section[data-testid="stSidebar"] button:hover { 
            background-color: rgba(255,255,255,0.08) !important; 
            transform: translateX(4px); 
        }
        section[data-testid="stSidebar"] button p { 
            white-space: nowrap; 
            overflow: hidden; 
            text-overflow: ellipsis; 
            max-width: 100%; 
        }
        
        /* ANIMATIONS  */
        @keyframes fadeUp { 
            from { opacity: 0; transform: translateY(6px); } 
            to { opacity: 1; transform: translateY(0px); } 
        }
        @keyframes dots { 
            0% { content: " ."; } 
            33% { content: " .."; } 
            66% { content: " ..."; } 
        }
        @keyframes shimmer { 
            0% { background-position: 100% 0; } 
            100% { background-position: -100% 0; } 
        }
        @keyframes blink { 
            0%, 50%, 100% { opacity: 1; } 
            25%, 75% { opacity: 0; } 
        }
        
        /* UI COMPONENTS  */
        .status-dot { 
            height: 10px; 
            width: 10px; 
            background-color: #10B981; 
            border-radius: 50%; 
            display: inline-block; 
            box-shadow: 0 0 12px #10B981; 
            margin-right: 8px; 
        }
        .typing { 
            display: inline-block; 
            font-size: 14px; 
            opacity: 0.6; 
        }
        .typing::after { 
            content: " ."; 
            animation: dots 1.5s infinite; 
        }
        .timestamp { 
            font-size: 11px; 
            opacity: 0.35; 
            margin-top: 4px; 
        }
        
        /*  MESSAGE CONTAINER  */
        .message-container { 
            position: relative; 
            padding-bottom: 24px; 
        }
        .message-actions { 
            position: absolute; 
            right: 10px; 
            bottom: 6px; 
            opacity: 0; 
            font-size: 14px; 
            transition: opacity 0.2s ease-in-out; 
        }
        .message-container:hover .message-actions { 
            opacity: 1; 
        }
        .message-actions span { 
            margin-left: 10px; 
            cursor: pointer; 
            opacity: 0.6; 
            transition: all 0.2s ease-in-out; 
        }
        .message-actions span:hover { 
            opacity: 1; 
            color: #10B981; 
        }
        
        /*  SKELETON LOADING  */
        .skeleton { 
            height: 14px; 
            border-radius: 6px; 
            margin-bottom: 8px;
            background: linear-gradient(90deg, rgba(255,255,255,0.05) 25%, rgba(255,255,255,0.15) 37%, rgba(255,255,255,0.05) 63%);
            background-size: 400% 100%; 
            animation: shimmer 1.4s ease infinite; 
        }
        .skeleton.short { width: 40%; } 
        .skeleton.medium { width: 70%; } 
        .skeleton.long { width: 90%; }
        
        /*  EXPANDER  */
        .streamlit-expanderHeader {
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.10);
            border-radius: 8px;
            padding: 8px 12px;
            font-weight: 500;
            color: #E5E7EB;
        }
        
        /*  SCROLLBAR  */
        ::-webkit-scrollbar {
            width: 8px;
        }
        ::-webkit-scrollbar-track {
            background: rgba(255,255,255,0.04);
        }
        ::-webkit-scrollbar-thumb {
            background: rgba(255,255,255,0.18);
            border-radius: 4px;
            padding: 6px 14px;
            font-size: 0.8rem;
            color: #10B981;
            font-weight: 500;
            animation: pulse 2s infinite;
        }
        .realtime-dot {
            width: 8px;
            height: 8px;
            background: #10B981;
            border-radius: 50%;
            animation: blink 1.5s infinite;
            box-shadow: 0 0 8px #10B981;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.8; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def chatgpt_header():
    """Render ChatGPT-style header with status indicator."""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        st.empty()
    
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 1rem 0;">
            <h1 style="margin: 0; font-size: 1.8rem; color: #E5E7EB;">Samvaad GPT</h1>
            <p style="margin: 0.5rem 0 0 0; opacity: .7; font-size: 0.9rem; color: #E5E7EB;">Real-time news intelligence powered by Gemini</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        model_status_text = "Online" if st.session_state.get("conversations") else "Ready"
        st.markdown(f"""
        <div style="text-align: right; padding: 1rem 0;">
            <span class="status-dot"></span><span style="opacity:.7; color: #E5E7EB;">{model_status_text}</span>
        </div>
        """, unsafe_allow_html=True)


def chatgpt_input_placeholder():
    """Display placeholder hints for the chat input."""
    st.markdown("""
    <div style="text-align: center; padding: 2rem; opacity: 0.6;">
        <p style="color: #E5E7EB;">💡 Try asking about recent news like:</p>
        <p style="color: #9CA3AF; font-size: 0.9rem;">
        "What's happening in India today?"<br>
        "Latest technology news"<br>
        "Breaking news in USA"
        </p>
        <p style="color: #6B7280; font-size: 0.75rem; margin-top: 1rem;">
        Powered by GNews API, NewsAPI, and Gemini API<br>
        Latest News (5 min - 6 Hours)
        </p>
    </div>
    """, unsafe_allow_html=True)


def realtime_news_indicator():
    """Display a real-time news fetching indicator."""
    st.markdown("""
    <div style="display: flex; justify-content: center; margin-bottom: 10px;">
        <div class="realtime-news-indicator">
            <span class="dot"></span>
            <span class="live-text">⚡ Live News • Fetched from Last 6 Hours</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def realtime_news_indicator():
    """Display a real-time news fetching indicator."""
    st.markdown("""
    <div style="display: flex; justify-content: center; margin: 10px 0;">
        <div class="realtime-indicator">
            <span class="realtime-dot"></span>
            <span>● Live News Fetched (Last 6 Hours)</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

