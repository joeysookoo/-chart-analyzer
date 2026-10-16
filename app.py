import streamlit as st
from PIL import Image
import json
from google import genai
from google.genai import types

# Page Configurations for a professional modern look
st.set_page_config(page_title="QUANT AI - Core Terminal", layout="wide", page_icon="⚡")

# ==========================================
# 🎨 LUXURY NEXUS TRADING TERMINAL STYLE ENGINE
# ==========================================
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #00FF66; letter-spacing: 1px; font-family: sans-serif;'>⚡ CONFIG PANEL</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.header("🎨 Dashboard Visuals")
    primary_color = st.color_picker("Glow Highlights", "#00FF66")
    bg_color = st.color_picker("Core Canvas Blur", "#06090F")
    card_bg = st.color_picker("Glassmorphic Modules", "#0D131E")
    text_color = st.color_picker("Typography Fill", "#F0F4F8")
    
    # Advanced UI CSS Injection for a premium premium look
    st.markdown(f"""
        <style>
            @import url('https://googleapis.com');
            
            .stApp {{
                background: radial-gradient(circle at top right, #111e13 0%, {bg_color} 60%) !important;
                color: {text_color} !important;
                font-family: 'Plus Jakarta Sans', sans-serif;
            }}
            h1, h2, h3, p, span, label {{
                color: {text_color} !important;
            }}
            
            /* Premium Dashboard Metric Cards */
            div[data-testid="stMetricValue"] {{
                color: {primary_color} !important;
                font-family: 'JetBrains Mono', monospace;
                font-weight: 700;
                font-size: 2.3rem !important;
                text-shadow: 0 0 15px rgba(0, 255, 102, 0.3);
            }}
            div[data-testid="metric-container"] {{
                background: {card_bg} !important;
                padding: 24px;
                border-radius: 16px !important;
                border: 1px solid rgba(255,255,255,0.04) !important;
                box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37) !important;
                backdrop-filter: blur(4px) !important;
                transition: transform 0.2s ease;
            }}
            div[data-testid="metric-container"]:hover {{
                transform: translateY(-3px);
                border-color: {primary_color} !important;
            }}
            
            /* Institutional Button Execution States */
            .stButton>button {{
                background: linear-gradient(135deg, {primary_color} 0%, #00b347 100%) !important;
                color: #02060D !important;
                font-family: 'Plus Jakarta Sans', sans-serif !important;
                font-weight: 800 !important;
                font-size: 1.1rem !important;
                letter-spacing: 1px;
                text-transform: uppercase;
                border-radius: 12px !important;
                border: none !important;
                padding: 16px 24px !important;
                width: 100%;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
                box-shadow: 0 4px 20px rgba(0, 255, 102, 0.25) !important;
            }}
            .stButton>button:hover {{
                transform: translateY(-2px) !important;
                box-shadow: 0 8px 30px rgba(0, 255, 102, 0.45) !important;
            }}
            
            /* Modern File Uploader Area */
            div[data-testid="stFileUploader"] {{
                background-color: {card_bg} !important;
                border: 2px dashed rgba(255, 255, 255, 0.1) !important;
                border-radius: 16px !important;
                padding: 10px !important;
            }}
            
            /* Custom Status Banners */
            .buy-banner {{
                background: linear-gradient(90deg, rgba(0,255,102,0.15) 0%, rgba(0,0,0,0) 100%);
                border-left: 6px solid #00FF66; padding: 18px; border-radius: 8px;
                font-weight: 800; font-size: 1.3rem; color: #00FF66 !important; letter-spacing: 0.5px;
            }}
            .sell-banner {{
                background: linear-gradient(90deg, rgba(255,51,51,0.15) 0%, rgba(0,0,0,0) 100%);
                border-left: 6px solid #FF3333; padding: 18px; border-radius: 8px;
                font-weight: 800; font-size: 1.3rem; color: #FF3333 !important; letter-spacing: 0.5px;
            }}
            .hold-banner {{
                background: linear-gradient(90deg, rgba(241,196,15,0.15) 0%, rgba(0,0,0,0) 100%);
                border-left: 6px solid #F1C40F; padding: 18px; border-radius: 8px;
                font-weight: 800; font-size: 1.3rem; color: #F1C40F !important; letter-spacing: 0.5px;
            }}
            
            .stAlert {{
                background-color: {card_bg} !important;
                border-left: 5px solid {primary_color} !important;
                color: {text_color} !important;
                border-radius: 12px !important;
            }}
        </style>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.header("🔧 Risk Profile Constraints")
    api_key = st.text_input("Enter Gemini API Key", type="password")
    
    st.markdown("---")
    account_balance = st.number_input("💰 Capital Inventory ($)", min_value=10, value=10000, step=100)
    risk_percentage = st.slider("⚠️ Allocation Risk (%)", min_value=0.25, max_value=5.0, value=1.0, step=0.25)
    risk_reward = st.slider("🎯 Position Target Ratio", min_value=1.0, max_value=4.0, value=2.0, step=0.5)
    
    allowed_risk_usd = (account_balance * risk_percentage) / 100
    st.metric(label="Absolute Value Protection", value=f"${allowed_risk_usd:,.2f}")

# ==========================================
# 📊 APP MAIN INTERFACE LAYOUT
# ==========================================
st.markdown("<h1 style='text-align: center; font-weight: 800; font-family: sans-serif; letter-spacing: -1px; margin-bottom: 0px;'>⚡ QUANT AI CORE TERMINAL</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #7EE79D !important; font-size: 1.1rem; margin-bottom: 40px;'>High-Speed Visual Chart Analyzer & Dynamic Risk Calculator</p>", unsafe_allow_html=True)

# 📰 Macro Overlay Section Layout
st.markdown("### 📰 Macro Environmental Inputs")
news_catalyst = st.selectbox(
    "Active High-Impact Volatility Filters:",
    [
        "None / Clear Structural Trading Conditions",
        "US Core Retail Sales Data Release (High Volatility)",
        "US CPI / PPI Inflation Print (Extreme Volatility for XAUUSD)",
        "US Initial Jobless Claims / Employment Data",
        "FOMC Interest Rate Decision / Central Bank Speeches",
        "Geopolitical Tensions / Sudden Global Market Risk Shifts"
    ]
)
custom_news = st.text_input("Manual Event Overrides (Optional):", "")
active_news = custom_news if custom_news else news_catalyst

st.markdown("<br><hr>", unsafe_allow_html=True)

# Drag-Drop Upload Panel
uploaded_file = st.file_uploader("", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    col1, col2 = st.columns([1.1, 0.9], gap="large")
    
    with col1:
        st.markdown("<h3 style='margin-bottom: 20px;'>🖼️ Live Market Context Capture</h3>", unsafe_allow_html=True)
        st.image(image, use_container_width=True)
        
    with col2:
        st.markdown("<h3 style='margin-bottom: 20px;'>🧠 Automated Execution Breakdown</h3>", unsafe_allow_html=True)
        run_analysis = st.button("🚀 Run Structural Core Analysis")
        
        if run_analysis:
            if not api_key:
                st.warning("Execution Halted: API Key Missing from Sidebar Panel.")
            else:
                with st.spinner("⚡ Activating Deep Vision Scanners..."):
                    try:
                        client = genai.Client(api_key=api_key)
                        
                        prompt = f"""
                        Analyze this chart screenshot while incorporating these fundamental variables:
                        - Current Active News Catalyst: {active_news}
                        - Starting Balance: ${account_balance}
                        - Absolute Risk Allowed: ${allowed_risk_usd}
                        - Target Risk-to-Reward: {risk_reward}:1
                        """
                        
                        json_schema = {
                            "type": "OBJECT",
                            "properties": {
                                "pair": {"type": "STRING"},
                                "action": {"type": "STRING"},
                                "entry": {"type": "NUMBER"},
                                "stop_loss": {"type": "NUMBER"},
                                "take_profit": {"type": "NUMBER"},
                                "lot_size": {"type": "STRING"},
                                "news_impact_rating": {"type": "STRING"},
                                "reasoning": {"type": "STRING"}
                            },
                            "required": ["pair", "action", "entry", "stop_loss", "take_profit", "lot_size", "news_impact_rating", "reasoning"]
                        }
                        
                        response = client.models.generate_content(
                            model='gemini-2.0-flash',
                            contents=[image, prompt],
                            config=types.GenerateContentConfig(
                                response_mime_type="application/json",
                                response_schema=json_schema,
                                temperature=0.1
                            )
                        )
                        
                        analysis = json.loads(response.text)
