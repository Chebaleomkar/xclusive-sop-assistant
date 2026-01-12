import streamlit as st
import requests
import json
import time
import os

# Set page configuration
st.set_page_config(
    page_title="SOP Assistant - Xclusive Interior",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Enhanced Custom CSS - Clean ChatGPT-inspired design
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main background - clean dark */
    .stApp {
        background: #212121;
        color: #ececec;
    }
    
    /* Hide default streamlit elements but keep sidebar toggle */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Main container - reduced spacing */
    .main-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding-top: 2rem;
        padding-bottom: 1rem;
    }
    
    /* Header styling - clean and elegant */
    .main-header {
        text-align: center;
        color: #ececec !important;
        font-size: 1.8rem;
        font-weight: 600;
        margin-bottom: 0.25rem;
        letter-spacing: -0.02em;
    }
    
    .sub-header {
        text-align: center;
        color: #8e8e8e;
        font-size: 0.85rem;
        margin-bottom: 1rem;
        max-width: 400px;
        line-height: 1.4;
    }
    
    /* Input container styling */
    .input-container {
        max-width: 800px;
        margin: 1rem auto;
        padding: 0 1rem;
    }
    
    /* Input field styling - ChatGPT style */
    .stTextInput > div > div {
        background-color: #2f2f2f !important;
        border-radius: 24px !important;
        border: 1px solid #424242 !important;
    }
    
    .stTextInput > div > div > input {
        background-color: transparent !important;
        color: #ececec !important;
        border: none !important;
        border-radius: 24px !important;
        padding: 0 1.5rem !important;
        font-size: 1rem !important;
        height: 48px !important;
        line-height: 48px !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #8e8e8e !important;
        line-height: 48px !important;
    }
    
    .stTextInput > div > div > input:focus {
        box-shadow: none !important;
        outline: none !important;
        border: none !important;
    }
    
    /* Form container alignment */
    .stForm > div {
        display: flex !important;
        align-items: center !important;
    }
    
    /* Columns alignment fix */
    [data-testid="column"] {
        display: flex !important;
        align-items: center !important;
    }
    
    /* Form submit button - green send style */
    .stFormSubmitButton {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        margin-top: 0 !important;
    }
    
    .stFormSubmitButton > button {
        background-color: #10a37f !important;
        border: none !important;
        border-radius: 50% !important;
        width: 48px !important;
        height: 48px !important;
        min-width: 48px !important;
        padding: 0 !important;
        color: #ffffff !important;
        font-size: 1.2rem !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        cursor: pointer !important;
        transition: background-color 0.2s ease !important;
        margin: 0 !important;
    }
    
    .stFormSubmitButton > button:hover {
        background-color: #1a7f64 !important;
    }
    
    /* User message bubble */
    .user-message {
        background: #2f2f2f;
        border-radius: 12px;
        padding: 0.75rem 1.25rem;
        margin: 0.5rem 0;
        margin-left: 25%;
        color: #ececec;
        border: 1px solid #424242;
    }
    
    .user-message .message-label {
        font-size: 0.7rem;
        color: #8e8e8e;
        margin-bottom: 0.25rem;
        font-weight: 500;
    }
    
    .user-message .message-content {
        font-size: 0.95rem;
        line-height: 1.4;
    }
    
    /* Assistant message bubble */
    .assistant-message {
        background: transparent;
        border-radius: 12px;
        padding: 0.5rem 0;
        margin: 0.25rem 0;
        color: #ececec;
        border: none;
    }
    
    .assistant-message .message-label {
        font-size: 0.7rem;
        color: #10a37f;
        margin-bottom: 0.25rem;
        font-weight: 500;
    }
    
    .assistant-message .message-content {
        font-size: 0.95rem;
        line-height: 1.5;
    }
    
    .assistant-message .message-content p {
        margin: 0.3rem 0 !important;
    }
    
    .assistant-message .message-content ul,
    .assistant-message .message-content ol {
        margin: 0.3rem 0 !important;
        padding-left: 1.5rem !important;
    }
    
    .assistant-message .message-content li {
        margin: 0.15rem 0 !important;
    }
    
    .assistant-message .message-content h1,
    .assistant-message .message-content h2,
    .assistant-message .message-content h3 {
        margin: 0.5rem 0 0.25rem 0 !important;
        font-size: 1rem !important;
    }
    
    /* Chat container scroll */
    .chat-container {
        max-height: 70vh;
        overflow-y: auto;
        padding-bottom: 1rem;
    }
    
    /* Source Card Styling */
    .source-card {
        padding: 1rem 1.5rem;
        border-radius: 8px;
        background: #2f2f2f;
        color: #b4b4b4;
        margin-top: 0.75rem;
        font-size: 0.9rem;
        border: 1px solid #424242;
    }
    
    /* Sidebar styling - keep dark theme */
    section[data-testid="stSidebar"] {
        background: #171717;
        border-right: 1px solid #2f2f2f;
    }
    
    section[data-testid="stSidebar"] > div {
        padding-top: 2rem;
    }
    
    /* Feature cards for sidebar */
    .feature-card {
        background: #2f2f2f;
        border-radius: 10px;
        padding: 1rem;
        border: 1px solid #424242;
        margin-bottom: 0.75rem;
        height: auto;
    }
    
    .feature-card:hover {
        border-color: #676767;
    }
    
    .feature-icon {
        font-size: 1.5rem;
        margin-bottom: 0.4rem;
    }
    
    .feature-title {
        color: #ececec;
        font-weight: 500;
        font-size: 0.9rem;
        margin-bottom: 0.3rem;
    }
    
    .feature-desc {
        color: #8e8e8e;
        font-size: 0.8rem;
        line-height: 1.4;
    }
    
    /* Slider styling */
    .stSlider > div > div > div {
        background-color: #424242;
    }
    
    .stSlider > div > div > div > div {
        background-color: #ececec;
    }
    
    /* Status indicators */
    .status-online {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.4rem 0.8rem;
        background: rgba(34, 197, 94, 0.15);
        border: 1px solid rgba(34, 197, 94, 0.3);
        border-radius: 6px;
        color: #4ade80;
        font-size: 0.85rem;
    }
    
    .status-offline {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.4rem 0.8rem;
        background: rgba(239, 68, 68, 0.15);
        border: 1px solid rgba(239, 68, 68, 0.3);
        border-radius: 6px;
        color: #f87171;
        font-size: 0.85rem;
    }
    
    .pulse-dot {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background-color: currentColor;
        animation: pulse 2s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: #2f2f2f !important;
        border-radius: 8px;
        border: 1px solid #424242;
        color: #ececec !important;
        font-size: 0.9rem;
    }
    
    /* Footer - fixed at bottom */
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        text-align: center;
        color: #9a9a9a;
        padding: 1rem 0;
        font-size: 0.75rem;
        background: #212121;
        z-index: 100;
    }
    
    /* Hide streamlit branding */
    .viewerBadge_container__1QSob {
        display: none !important;
    }
    
    /* Form styling */
    .stForm {
        border: none !important;
        padding: 0 !important;
    }
    
    /* Markdown text */
    h1, h2, h3 {
        color: #ececec !important;
    }
    
    p {
        color: #b4b4b4;
    }
    
    /* Columns gap fix */
    [data-testid="column"] {
        padding: 0 0.25rem !important;
    }
    
    /* Team badge */
    .team-badge {
        display: inline-block;
        padding: 0.2rem 0.5rem;
        background: rgba(16, 163, 127, 0.2);
        border: 1px solid rgba(16, 163, 127, 0.4);
        border-radius: 4px;
        color: #10a37f;
        font-size: 0.7rem;
        font-weight: 500;
        margin-right: 0.5rem;
    }
    
    /* Score badge */
    .score-badge {
        display: inline-block;
        padding: 0.2rem 0.5rem;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 4px;
        color: #8e8e8e;
        font-size: 0.65rem;
    }
    
    /* Source item */
    .source-item {
        background: #2a2a2a;
        border: 1px solid #3a3a3a;
        border-radius: 8px;
        padding: 0.75rem 1rem;
        margin: 0.5rem 0;
    }
    
    .source-item:hover {
        border-color: #10a37f;
    }
    
    .source-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 0.5rem;
    }
    
    .source-title {
        color: #10a37f;
        font-weight: 500;
        font-size: 0.85rem;
    }
    
    .source-text {
        color: #9a9a9a;
        font-size: 0.8rem;
        line-height: 1.4;
    }
    
    /* Stats display */
    .stats-box {
        background: #2a2a2a;
        border: 1px solid #3a3a3a;
        border-radius: 8px;
        padding: 0.75rem 1rem;
        text-align: center;
    }
    
    .stats-number {
        font-size: 1.5rem;
        font-weight: 600;
        color: #10a37f;
    }
    
    .stats-label {
        font-size: 0.75rem;
        color: #8e8e8e;
    }
    
    /* Select box styling */
    .stSelectbox > div > div {
        background-color: #2f2f2f !important;
        border-color: #424242 !important;
    }
    
    </style>
    """, unsafe_allow_html=True)

# API Configuration
API_URL = "https://sop-rag-system.onrender.com"

# Initialize session state
if 'query_history' not in st.session_state:
    st.session_state.query_history = []
if 'query_submitted' not in st.session_state:
    st.session_state.query_submitted = False
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'is_loading' not in st.session_state:
    st.session_state.is_loading = False


def query_api(query: str, top_k: int, team: str = None):
    """Query the backend API"""
    try:
        payload = {
            "query": query,
            "top_k": top_k
        }
        if team and team != "All Teams":
            payload["team"] = team
            
        response = requests.post(f"{API_URL}/query", json=payload, timeout=60)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        return {"error": "Could not connect to the Backend API. Make sure it's running on http://localhost:8000"}
    except requests.exceptions.Timeout:
        return {"error": "Request timed out. Please try again."}
    except Exception as e:
        return {"error": str(e)}


def get_api_stats():
    """Get stats from API"""
    try:
        response = requests.get(f"{API_URL}/stats", timeout=5)
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return None


def get_teams():
    """Get available teams"""
    try:
        response = requests.get(f"{API_URL}/teams", timeout=5)
        if response.status_code == 200:
            return response.json().get("teams", [])
    except:
        pass
    return []


# Sidebar
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    st.markdown("---")
    
    # Team filter
    teams = get_teams()
    team_options = ["All Teams"] + teams
    selected_team = st.selectbox(
        "Filter by Team",
        options=team_options,
        index=0,
        help="Filter search results to a specific team's documents"
    )
    
    # Top K slider with help
    top_k = st.slider(
        "Search Depth", 
        min_value=1, 
        max_value=10, 
        value=5, 
        help="Higher values search more documents but may take longer"
    )
    
    st.markdown("---")
    
    # Backend status and stats
    st.markdown("### 📊 System Status")
    
    stats = get_api_stats()
    if stats:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
                <div class="stats-box">
                    <div class="stats-number">{stats.get('total_vectors', 0)}</div>
                    <div class="stats-label">Vectors</div>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
                <div class="stats-box">
                    <div class="stats-number">{len(stats.get('teams', []))}</div>
                    <div class="stats-label">Teams</div>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
            <div class="status-online" style="margin-top: 0.5rem;">
                <div class="pulse-dot"></div>
                Backend Online
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div class="status-offline">
                <div class="pulse-dot"></div>
                Backend Offline
            </div>
        """, unsafe_allow_html=True)
        st.info("Start the backend: `python -m uvicorn app:app --reload`")
    
    st.markdown("---")
    
    # Info section with features
    st.markdown("### 💡 Features")
    st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🔍</div>
            <div class="feature-title">Multi-Modal Search</div>
            <div class="feature-desc">Searches PDFs with images and text documents</div>
        </div>
        
        <div class="feature-card">
            <div class="feature-icon">🏢</div>
            <div class="feature-title">Team Filtering</div>
            <div class="feature-desc">Filter results by department: HR, 3D, Operations</div>
        </div>
        
        <div class="feature-card">
            <div class="feature-icon">📄</div>
            <div class="feature-title">Source Verification</div>
            <div class="feature-desc">See exactly which documents answers come from</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Clear chat button
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.query_history = []
        st.rerun()


# Main UI - Clean ChatGPT-inspired layout
st.markdown('''
    <div class="main-container">
        <h1 class="main-header">SOP Assistant</h1>
        <p class="sub-header">Your intelligent guide to Xclusive Interior's Standard Operating Procedures</p>
    </div>
''', unsafe_allow_html=True)

# Chat container - scrollable area for messages
chat_container = st.container()

with chat_container:
    # Display all messages in the chat history
    for idx, message in enumerate(st.session_state.messages):
        if message["role"] == "user":
            # User message - right aligned style
            st.markdown(f'''
                <div class="user-message">
                    <div class="message-label">You</div>
                    <div class="message-content">{message["content"]}</div>
                </div>
            ''', unsafe_allow_html=True)
        else:
            # Assistant message - use streamlit markdown for proper rendering
            st.markdown('''
                <div class="assistant-message">
                    <div class="message-label">🤖 SOP Assistant</div>
                </div>
            ''', unsafe_allow_html=True)
            st.markdown(message["content"])
            
            # Show sources if available
            sources = message.get("sources", [])
            if sources:
                with st.expander(f"📄 View Sources ({len(sources)})", expanded=False):
                    for source in sources:
                        team = source.get("team", "Unknown")
                        doc_id = source.get("document_id", "Unknown")
                        page = source.get("page_number", 0)
                        score = source.get("score", 0)
                        text = source.get("text", "")
                        source_file = source.get("source_file", "")
                        
                        # Build title
                        title = f"{team}/{doc_id}"
                        if page > 0:
                            title += f" (Page {page})"
                        
                        st.markdown(f'''
                            <div class="source-item">
                                <div class="source-header">
                                    <span class="source-title">📄 {title}</span>
                                    <span class="score-badge">Score: {score:.2%}</span>
                                </div>
                                <div style="margin-bottom: 0.5rem;">
                                    <span class="team-badge">{team}</span>
                                    <span style="color: #676767; font-size: 0.7rem;">{source_file}</span>
                                </div>
                                <div class="source-text">{text[:300]}{'...' if len(text) > 300 else ''}</div>
                            </div>
                        ''', unsafe_allow_html=True)

# Add minimal spacing before input
st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)

# Centered input area at bottom
st.markdown('<div class="input-container">', unsafe_allow_html=True)

# Show loading indicator or input form
if st.session_state.is_loading:
    # Show loading state
    st.markdown('''
        <div style="text-align: center; padding: 1rem; color: #10a37f;">
            <div style="font-size: 1.5rem; animation: pulse-loading 1.5s ease-in-out infinite;">⏳</div>
            <div style="font-size: 0.9rem; margin-top: 0.5rem;">Searching SOPs and generating response...</div>
        </div>
    ''', unsafe_allow_html=True)
else:
    # Create the input with form for enter-key submission
    with st.form(key="query_form", clear_on_submit=True):
        col1, col2 = st.columns([12, 1])
        
        with col1:
            query = st.text_input(
                "Ask anything",
                placeholder="Ask anything about company policies, procedures, workflows...",
                label_visibility="collapsed",
                key="query_input"
            )
        
        with col2:
            submitted = st.form_submit_button("➤", use_container_width=True)
    
    # Handle submission
    if submitted and query:
        # Set loading state
        st.session_state.is_loading = True
        
        # Add user message to chat
        st.session_state.messages.append({
            "role": "user",
            "content": query
        })
        
        # Add to query history for sidebar
        if query not in st.session_state.query_history:
            st.session_state.query_history.append(query)
        
        # Store query and settings for processing
        st.session_state.pending_query = query
        st.session_state.pending_team = selected_team
        st.session_state.pending_top_k = top_k
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# Process pending query if loading
if st.session_state.is_loading and hasattr(st.session_state, 'pending_query'):
    query = st.session_state.pending_query
    team = st.session_state.pending_team
    top_k_val = st.session_state.pending_top_k
    
    # Get response from API
    result = query_api(query, top_k_val, team if team != "All Teams" else None)
    
    # Add assistant response to chat
    if "error" in result:
        st.session_state.messages.append({
            "role": "assistant",
            "content": f"❌ {result['error']}",
            "sources": []
        })
    else:
        st.session_state.messages.append({
            "role": "assistant",
            "content": result.get('answer', 'No answer received'),
            "sources": result.get('sources', [])
        })
    
    # Clear loading state
    st.session_state.is_loading = False
    del st.session_state.pending_query
    del st.session_state.pending_team
    del st.session_state.pending_top_k
    st.rerun()

# Footer
st.markdown('''
    <div class="footer">
        <p>SOP Assistant • Powered by RAG • Xclusive Interior Pvt Ltd</p>
    </div>
''', unsafe_allow_html=True)
