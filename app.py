import streamlit as st
from PIL import Image
import json
from google import genai
from google.genai import types

# Page Configuration
st.set_page_config(page_title="QUANT AI Terminal", layout="wide", page_icon="⚡")

# ==========================================
# 🎨 HIGH-END DARK TRADING INTERFACE SYSTEM
# ==========================================
with st.sidebar:
    st.markdown("### ⚡ CONFIG PANEL")
    primary_color = st.color_picker("Glow Highlights", "#00FF66")
    bg_color = st.color_picker("Terminal Background", "#06090F")
    card_bg = st.color_picker("Card Containers", "#131924")
    text_color = st.color_picker("Typography Fill", "#F0F4F8")
    
    st.markdown(f"""
        <style>
            .stApp {{ background-color: {bg_color} !important; color: {text_color} !important; font-family: sans-serif; }}
            h1, h2, h3, p, span, label {{ color: {text_color} !important; }}
            div[data-testid="stMetricValue"] {{ color: {primary_color} !important; font-weight: 700; font-size: 2.2rem !important; }}
            div[data-testid="metric-container"] {{ background-color: {card_bg} !important; padding: 20px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05); }}
            .stButton>button {{
                background: linear-gradient(135deg, {primary_color} 0%, #00b347 100%) !important;
                color: #02060D !important; font-weight: 800; border-radius: 8px; border: none; padding: 14px 20px; width: 100%;
            }}
            .stAlert {{ background-color: {card_bg} !important; border-left: 5px solid {primary_color} !important; color: {text_color} !important; border-radius: 12px; }}
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
st.markdown("<h1 style='text-align: center; font-weight: 800;'>⚡ QUANT AI CORE TERMINAL</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #7EE79D;'>High-Speed Visual Chart Analyzer & Dynamic Risk Calculator</p>", unsafe_allow_html=True)

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

st.markdown("---")
uploaded_file = st.file_uploader("Upload Chart Screenshot", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🖼️ Live Market Context Capture")
        st.image(image, use_container_width=True)
        
    with col2:
        st.subheader("🧠 Automated Execution Breakdown")
        run_analysis = st.button("🚀 Run Structural Core Analysis")
        
        if run_analysis and not api_key:
            st.warning("Execution Halted: API Key Missing from Sidebar Panel.")
            
        if run_analysis and api_key:
            with st.spinner("⚡ Activating Deep Vision Scanners..."):
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
                action = analysis.get("action", "HOLD").upper()
                
                if action == "BUY":
                    st.success("🎯 POSITION STRATEGY: STRONG BUY SIGNAL")
                elif action == "SELL":
                    st.error("🎯 POSITION STRATEGY: STRONG SELL SIGNAL")
                else:
                    st.warning("🎯 POSITION STRATEGY: NEUTRAL MARKET STANDBY / HOLD")
                
                m1, m2, m3 = st.columns(3)
                m1.metric(label="📍 Target Entry", value=f"${analysis.get('entry'):,}")
                m2.metric(label="🛑 Stop Loss (SL)", value=f"${analysis.get('stop_loss'):,}")
                m3.metric(label="💰 Take Profit (TP)", value=f"${analysis.get('take_profit'):,}")
                
                st.markdown("---")
                st.subheader("⚖️ Risk Allocation Order Matrix")
                st.info(f"👉 EXECUTION SIZE: Use {analysis.get('lot_size')} to protect your capital layout.")
                st.write(f"Asset: {analysis.get('pair')} | News Rating: {analysis.get('news_impact_rating')}")
                st.write(analysis.get("reasoning"))
