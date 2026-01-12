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

# Check if we have messages (determines sticky behavior)
has_messages = len(st.session_state.get('messages', [])) > 0

# Enhanced Custom CSS - Mobile-First Responsive Design with Sticky Input
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* ===== CSS RESET & BASE STYLES ===== */
    * {{
        font-family: 'Inter', sans-serif;
        box-sizing: border-box;
        -webkit-tap-highlight-color: transparent;
    }}
    
    /* Main background - clean dark */
    .stApp {{
        background: #212121;
        color: #ececec;
    }}
    
    /* Hide default streamlit elements */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    .viewerBadge_container__1QSob {{display: none !important;}}
    
    /* ===== STREAMLIT OVERRIDES FOR MOBILE ===== */
    .main .block-container {{
        padding: 0.5rem 0.75rem 0 0.75rem !important;
        max-width: 100% !important;
        padding-bottom: {'120px' if has_messages else '0'} !important;
    }}
    
    /* Fix column gaps */
    [data-testid="column"] {{
        padding: 0 0.15rem !important;
    }}
    
    .stHorizontalBlock {{
        gap: 0.5rem !important;
    }}
    
    /* ===== WELCOME SCREEN (No messages) ===== */
    .welcome-container {{
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 60vh;
        padding: 1rem;
        text-align: center;
    }}
    
    .welcome-header {{
        font-size: 2rem;
        font-weight: 700;
        color: #ececec;
        margin-bottom: 0.5rem;
        background: linear-gradient(135deg, #10a37f 0%, #1ec99f 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }}
    
    .welcome-subheader {{
        font-size: 0.9rem;
        color: #8e8e8e;
        max-width: 400px;
        line-height: 1.5;
        margin-bottom: 2rem;
    }}
    
    /* ===== COMPACT HEADER (With messages) ===== */
    .compact-header {{
        text-align: center;
        padding: 1rem 0 0.75rem 0;
        margin-bottom: 0.5rem;
    }}
    
    .compact-header h1 {{
        font-size: 2rem;
        font-weight: 700;
        color: #ececec;
        margin: 0 0 0.25rem 0;
    }}
    
    .compact-header p {{
        font-size: 0.85rem;
        color: #8e8e8e;
        margin: 0 auto;
        max-width: 400px;
        line-height: 1.4;
    }}
    
    /* ===== STICKY INPUT CONTAINER ===== */
    .sticky-input-wrapper {{
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: linear-gradient(transparent, #212121 15%);
        padding: 0.75rem 1rem 1rem 1rem;
        z-index: 999;
    }}
    
    .sticky-input-inner {{
        max-width: 800px;
        margin: 0 auto;
    }}
    
    /* ===== NON-STICKY INPUT (Welcome screen) ===== */
    .centered-input-wrapper {{
        width: 100%;
        max-width: 600px;
        margin: 0 auto;
        padding: 0 1rem;
    }}
    
    /* ===== TEXT AREA STYLING ===== */
    .stTextArea > div > div {{
        background-color: #2f2f2f !important;
        border-radius: 16px !important;
        border: 1px solid #424242 !important;
    }}
    
    .stTextArea > div > div > textarea {{
        background-color: transparent !important;
        color: #ececec !important;
        border: none !important;
        border-radius: 16px !important;
        padding: 0.75rem 1rem !important;
        font-size: 0.9rem !important;
        line-height: 1.5 !important;
        resize: none !important;
        min-height: 50px !important;
        max-height: 150px !important;
    }}
    
    .stTextArea > div > div > textarea::placeholder {{
        color: #8e8e8e !important;
    }}
    
    .stTextArea > div > div > textarea:focus {{
        box-shadow: none !important;
        outline: none !important;
    }}
    
    /* Hide textarea label */
    .stTextArea > label {{
        display: none !important;
    }}
    
    /* ===== INPUT ROW LAYOUT ===== */
    .input-row {{
        display: flex;
        align-items: flex-end;
        gap: 0.5rem;
        width: 100%;
    }}
    
    .input-field {{
        flex: 1;
        min-width: 0;
    }}
    
    .send-btn-wrapper {{
        flex-shrink: 0;
    }}
    
    /* ===== SEND BUTTON ===== */
    .stButton > button {{
        background: linear-gradient(135deg, #10a37f 0%, #0d8a6a 100%) !important;
        border: none !important;
        border-radius: 12px !important;
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
        transition: all 0.2s ease !important;
        box-shadow: 0 2px 8px rgba(16, 163, 127, 0.3) !important;
    }}
    
    .stButton > button:hover {{
        background: linear-gradient(135deg, #0d8a6a 0%, #0a7559 100%) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(16, 163, 127, 0.4) !important;
    }}
    
    .stButton > button:active {{
        transform: scale(0.95) !important;
    }}
    
    /* ===== CHAT CONTAINER ===== */
    .chat-messages {{
        display: flex;
        flex-direction: column;
        gap: 0.75rem;
        padding-bottom: 1rem;
    }}

    
    /* ===== USER MESSAGE ===== */
    .user-message {{
        background: linear-gradient(135deg, #2f2f2f 0%, #353535 100%);
        border-radius: 12px 12px 4px 12px;
        padding: 0.75rem 1rem;
        margin-left: 15%;
        color: #ececec;
        border: 1px solid #424242;
        position: relative;
    }}
    
    .user-message::before {{
        content: '';
        position: absolute;
        bottom: 0;
        right: -8px;
        width: 0;
        height: 0;
        border: 8px solid transparent;
        border-left-color: #353535;
        border-bottom-color: #353535;
    }}
    
    .user-label {{
        font-size: 0.65rem;
        color: #8e8e8e;
        margin-bottom: 0.25rem;
        font-weight: 500;
        display: flex;
        align-items: center;
        gap: 0.3rem;
    }}
    
    .user-content {{
        font-size: 0.9rem;
        line-height: 1.5;
    }}
    
    /* ===== ASSISTANT MESSAGE ===== */
    .assistant-message {{
        padding: 0.75rem 0;
        color: #ececec;
    }}
    
    .assistant-label {{
        font-size: 0.65rem;
        color: #10a37f;
        margin-bottom: 0.35rem;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 0.3rem;
    }}
    
    .assistant-content {{
        font-size: 0.9rem;
        line-height: 1.6;
    }}
    
    .assistant-content p {{
        margin: 0.4rem 0 !important;
    }}
    
    .assistant-content ul, .assistant-content ol {{
        margin: 0.4rem 0 !important;
        padding-left: 1.5rem !important;
    }}
    
    .assistant-content li {{
        margin: 0.2rem 0 !important;
    }}
    
    /* ===== DIVIDER ===== */
    .message-divider {{
        height: 1px;
        background: linear-gradient(90deg, transparent, #333, transparent);
        margin: 0.75rem 0;
    }}
    
    /* ===== SOURCE STYLING ===== */
    .source-item {{
        background: #252525;
        border: 1px solid #333;
        border-radius: 8px;
        padding: 0.6rem 0.75rem;
        margin: 0.35rem 0;
        transition: border-color 0.2s ease;
    }}
    
    .source-item:hover {{
        border-color: #10a37f;
    }}
    
    .source-header {{
        display: flex;
        align-items: flex-start;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 0.25rem;
        margin-bottom: 0.35rem;
    }}
    
    .source-title {{
        color: #10a37f;
        font-weight: 500;
        font-size: 0.78rem;
    }}
    
    .source-text {{
        color: #9a9a9a;
        font-size: 0.75rem;
        line-height: 1.4;
    }}
    
    .team-badge {{
        display: inline-block;
        padding: 0.15rem 0.4rem;
        background: rgba(16, 163, 127, 0.2);
        border: 1px solid rgba(16, 163, 127, 0.4);
        border-radius: 4px;
        color: #10a37f;
        font-size: 0.6rem;
        font-weight: 500;
    }}
    
    .score-badge {{
        display: inline-block;
        padding: 0.15rem 0.4rem;
        background: rgba(255, 255, 255, 0.08);
        border-radius: 4px;
        color: #8e8e8e;
        font-size: 0.58rem;
    }}
    
    /* ===== EXPANDER STYLING ===== */
    .streamlit-expanderHeader {{
        background-color: #252525 !important;
        border-radius: 8px !important;
        border: 1px solid #333 !important;
        color: #ececec !important;
        font-size: 0.8rem !important;
        padding: 0.5rem 0.75rem !important;
    }}
    
    /* ===== LOADING STATE ===== */
    .loading-container {{
        text-align: center;
        padding: 1rem;
        color: #10a37f;
    }}
    
    .loading-dots {{
        display: flex;
        justify-content: center;
        gap: 0.3rem;
        margin-bottom: 0.5rem;
    }}
    
    .loading-dot {{
        width: 8px;
        height: 8px;
        background: #10a37f;
        border-radius: 50%;
        animation: bounce 1.4s infinite ease-in-out both;
    }}
    
    .loading-dot:nth-child(1) {{ animation-delay: -0.32s; }}
    .loading-dot:nth-child(2) {{ animation-delay: -0.16s; }}
    .loading-dot:nth-child(3) {{ animation-delay: 0s; }}
    
    @keyframes bounce {{
        0%, 80%, 100% {{ transform: scale(0); }}
        40% {{ transform: scale(1); }}
    }}
    
    /* ===== SIDEBAR STYLING ===== */
    section[data-testid="stSidebar"] {{
        background: #171717;
        border-right: 1px solid #2f2f2f;
    }}
    
    section[data-testid="stSidebar"] > div {{
        padding: 1rem 0.75rem;
    }}
    
    .feature-card {{
        background: #2f2f2f;
        border-radius: 8px;
        padding: 0.75rem;
        border: 1px solid #424242;
        margin-bottom: 0.5rem;
    }}
    
    .feature-icon {{
        font-size: 1.25rem;
        margin-bottom: 0.25rem;
    }}
    
    .feature-title {{
        color: #ececec;
        font-weight: 500;
        font-size: 0.8rem;
        margin-bottom: 0.2rem;
    }}
    
    .feature-desc {{
        color: #8e8e8e;
        font-size: 0.7rem;
        line-height: 1.3;
    }}
    
    .stats-box {{
        background: #2a2a2a;
        border: 1px solid #3a3a3a;
        border-radius: 8px;
        padding: 0.5rem 0.6rem;
        text-align: center;
    }}
    
    .stats-number {{
        font-size: 1.2rem;
        font-weight: 600;
        color: #10a37f;
    }}
    
    .stats-label {{
        font-size: 0.65rem;
        color: #8e8e8e;
    }}
    
    .status-online {{
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        padding: 0.3rem 0.6rem;
        background: rgba(34, 197, 94, 0.15);
        border: 1px solid rgba(34, 197, 94, 0.3);
        border-radius: 6px;
        color: #4ade80;
        font-size: 0.75rem;
    }}
    
    .status-offline {{
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        padding: 0.3rem 0.6rem;
        background: rgba(239, 68, 68, 0.15);
        border: 1px solid rgba(239, 68, 68, 0.3);
        border-radius: 6px;
        color: #f87171;
        font-size: 0.75rem;
    }}
    
    .pulse-dot {{
        width: 5px;
        height: 5px;
        border-radius: 50%;
        background-color: currentColor;
        animation: pulse 2s ease-in-out infinite;
    }}
    
    @keyframes pulse {{
        0%, 100% {{ opacity: 1; }}
        50% {{ opacity: 0.5; }}
    }}
    
    /* Slider styling */
    .stSlider > div > div > div {{
        background-color: #424242;
    }}
    
    .stSlider > div > div > div > div {{
        background-color: #ececec;
    }}
    
    /* Select box styling */
    .stSelectbox > div > div {{
        background-color: #2f2f2f !important;
        border-color: #424242 !important;
    }}
    
    /* Markdown text */
    h1, h2, h3 {{
        color: #ececec !important;
    }}
    
    p {{
        color: #b4b4b4;
    }}
    
    /* ===== FOOTER ===== */
    .footer {{
        text-align: center;
        color: #666;
        padding: 0.5rem 0;
        font-size: 0.65rem;
        margin-top: 1rem;
    }}
    
    /* ===== MOBILE RESPONSIVE ===== */
    @media only screen and (max-width: 480px) {{
        .main .block-container {{
            padding: 0.25rem 0.5rem 0 0.5rem !important;
            padding-bottom: {'100px' if has_messages else '0'} !important;
        }}
        
        .welcome-header {{
            font-size: 1.5rem;
        }}
        
        .welcome-subheader {{
            font-size: 0.8rem;
        }}
        
        .user-message {{
            margin-left: 5%;
            padding: 0.6rem 0.8rem;
        }}
        
        .sticky-input-wrapper {{
            padding: 0.5rem 0.75rem 0.75rem 0.75rem;
        }}
        
        .stTextArea > div > div > textarea {{
            font-size: 16px !important; /* Prevents zoom on iOS */
            min-height: 44px !important;
        }}
        
        .stButton > button {{
            width: 44px !important;
            height: 44px !important;
            min-width: 44px !important;
            border-radius: 10px !important;
        }}
        
        .message-pair {{
            padding: 0.75rem;
        }}
        
        .source-item {{
            padding: 0.5rem 0.6rem;
        }}
    }}
    
    @media only screen and (min-width: 481px) and (max-width: 768px) {{
        .user-message {{
            margin-left: 10%;
        }}
        
        .welcome-header {{
            font-size: 1.75rem;
        }}
    }}
    
    @media only screen and (min-width: 769px) {{
        .main .block-container {{
            padding: 1rem 2rem 0 2rem !important;
            max-width: 900px !important;
            margin: 0 auto !important;
            padding-bottom: {'140px' if has_messages else '0'} !important;
        }}
        
        .user-message {{
            margin-left: 20%;
        }}
        
        .sticky-input-wrapper {{
            padding: 1rem 2rem 1.5rem 2rem;
        }}
        
        .sticky-input-inner {{
            max-width: 850px;
        }}
        
        .stButton > button {{
            width: 52px !important;
            height: 52px !important;
            min-width: 52px !important;
        }}
    }}
    
    /* Touch device optimizations */
    @media (hover: none) and (pointer: coarse) {{
        .stButton > button:active {{
            transform: scale(0.92) !important;
        }}
        
        .source-item:active {{
            background: #2a2a2a;
        }}
    }}
    
    /* Safe area for mobile browsers */
    @supports (padding-bottom: env(safe-area-inset-bottom)) {{
        .sticky-input-wrapper {{
            padding-bottom: calc(1rem + env(safe-area-inset-bottom));
        }}
    }}
    
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
        return {"error": "Could not connect to the Backend API."}
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
    
    st.markdown("---")
    
    # Info section with features
    st.markdown("### 💡 Features")
    st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🔍</div>
            <div class="feature-title">Multi-Modal Search</div>
            <div class="feature-desc">Searches PDFs with images and text</div>
        </div>
        
        <div class="feature-card">
            <div class="feature-icon">🏢</div>
            <div class="feature-title">Team Filtering</div>
            <div class="feature-desc">Filter by department</div>
        </div>
        
        <div class="feature-card">
            <div class="feature-icon">📄</div>
            <div class="feature-title">Source Verification</div>
            <div class="feature-desc">See source documents</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Clear chat button
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.query_history = []
        st.rerun()


# ========== MAIN CONTENT ==========

# Check if we have messages
has_messages = len(st.session_state.messages) > 0

if not has_messages:
    # ===== WELCOME SCREEN (First message - input NOT sticky) =====
    st.markdown('''
        <div class="welcome-container">
            <h1>SOP Assistant</h1>
            <p>
                Your intelligent guide to Xclusive Interior's Standard Operating Procedures. 
                Ask anything about company policies, workflows, and procedures.
            </p>
        </div>
    ''', unsafe_allow_html=True)
    
    # Centered input for welcome screen
    st.markdown('<div class="centered-input-wrapper">', unsafe_allow_html=True)
    
    # Input row with text area and send button
    col1, col2 = st.columns([9, 1])
    
    with col1:
        query = st.text_area(
            "Ask a question",
            placeholder="Ask anything about company policies, procedures, workflows...",
            height=80,
            max_chars=1000,
            key="welcome_input",
            label_visibility="collapsed"
        )
    
    with col2:
        st.write("")  # Spacer for alignment
        send_clicked = st.button("➤", key="welcome_send", use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Handle submission
    if send_clicked and query and query.strip():
        st.session_state.is_loading = True
        st.session_state.messages.append({
            "role": "user",
            "content": query.strip()
        })
        st.session_state.pending_query = query.strip()
        st.session_state.pending_team = selected_team
        st.session_state.pending_top_k = top_k
        st.rerun()
    
    # Footer for welcome screen
    st.markdown('''
        <div class="footer">
            SOP Assistant • Xclusive Interior Pvt Ltd
        </div>
    ''', unsafe_allow_html=True)

else:
    # ===== CHAT INTERFACE (Has messages - input IS sticky) =====
    
    # Header - same style as welcome screen
    st.markdown('''
        <div class="compact-header">
            <h1>SOP Assistant</h1>
            <p>Your intelligent guide to Xclusive Interior's Standard Operating Procedures</p>
        </div>
    ''', unsafe_allow_html=True)
    
    # Chat messages container
    chat_container = st.container()
    
    with chat_container:
        # Group messages into pairs (user + assistant)
        messages = st.session_state.messages
        i = 0
        while i < len(messages):
            # Start a message pair container
            st.markdown('<div class="message-pair">', unsafe_allow_html=True)
            
            # User message
            if i < len(messages) and messages[i]["role"] == "user":
                user_msg = messages[i]
                st.markdown(f'''
                    <div class="user-message">
                        <div class="user-label">👤 You</div>
                        <div class="user-content">{user_msg["content"]}</div>
                    </div>
                ''', unsafe_allow_html=True)
                i += 1
            
            # Divider
            st.markdown('<div class="message-divider"></div>', unsafe_allow_html=True)
            
            # Assistant message
            if i < len(messages) and messages[i]["role"] == "assistant":
                assistant_msg = messages[i]
                st.markdown('''
                    <div class="assistant-message">
                        <div class="assistant-label">🤖 SOP Assistant</div>
                    </div>
                ''', unsafe_allow_html=True)
                
                # Use streamlit markdown for proper rendering
                st.markdown(assistant_msg["content"])
                
                # Show sources if available
                sources = assistant_msg.get("sources", [])
                if sources:
                    with st.expander(f"📄 View Sources ({len(sources)})", expanded=False):
                        for source in sources:
                            team = source.get("team", "Unknown")
                            doc_id = source.get("document_id", "Unknown")
                            page = source.get("page_number", 0)
                            score = source.get("score", 0)
                            text = source.get("text", "")
                            source_file = source.get("source_file", "")
                            
                            title = f"{team}/{doc_id}"
                            if page > 0:
                                title += f" (Page {page})"
                            
                            st.markdown(f'''
                                <div class="source-item">
                                    <div class="source-header">
                                        <span class="source-title">📄 {title}</span>
                                        <span class="score-badge">Score: {score:.2%}</span>
                                    </div>
                                    <div style="margin-bottom: 0.3rem;">
                                        <span class="team-badge">{team}</span>
                                        <span style="color: #666; font-size: 0.65rem;">{source_file}</span>
                                    </div>
                                    <div class="source-text">{text[:250]}{'...' if len(text) > 250 else ''}</div>
                                </div>
                            ''', unsafe_allow_html=True)
                i += 1
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Show loading indicator
    if st.session_state.is_loading:
        st.markdown('''
            <div class="loading-container">
                <div class="loading-dots">
                    <div class="loading-dot"></div>
                    <div class="loading-dot"></div>
                    <div class="loading-dot"></div>
                </div>
                <div style="font-size: 0.8rem;">Searching SOPs...</div>
            </div>
        ''', unsafe_allow_html=True)
    
    # ===== STICKY INPUT BAR =====
    # We need to use a placeholder and JavaScript to make it truly sticky
    st.markdown('<div class="sticky-input-wrapper"><div class="sticky-input-inner">', unsafe_allow_html=True)
    
    # Input row
    col1, col2 = st.columns([9, 1])
    
    with col1:
        query = st.text_area(
            "Ask a question",
            placeholder="Ask anything about company policies, procedures, workflows...",
            height=60,
            max_chars=1000,
            key="chat_input",
            label_visibility="collapsed"
        )
    
    with col2:
        st.write("")  # Spacer
        send_clicked = st.button("➤", key="chat_send", use_container_width=True)
    
    st.markdown('</div></div>', unsafe_allow_html=True)
    
    # Handle submission
    if send_clicked and query and query.strip() and not st.session_state.is_loading:
        st.session_state.is_loading = True
        st.session_state.messages.append({
            "role": "user",
            "content": query.strip()
        })
        st.session_state.pending_query = query.strip()
        st.session_state.pending_team = selected_team
        st.session_state.pending_top_k = top_k
        st.rerun()


# ===== PROCESS PENDING QUERY =====
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
