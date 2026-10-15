import streamlit as st
from PIL import Image
import json
from google import genai
from google.genai import types

# Page Configurations
st.set_page_config(page_title="Pro AI Trading Terminal", layout="wide", page_icon="⚡")

# ==========================================
# 🎨 HIGH-END TRADING TERMINAL STYLE ENGINE
# ==========================================
with st.sidebar:
    st.header("🎨 Interface Theme Customizer")
    primary_color = st.color_picker("Accent Highlights", "#00FF66", help="Changes metrics and active button glow")
    bg_color = st.color_picker("Terminal Background", "#090D14", help="Deep dashboard tone")
    card_bg = st.color_picker("Card Containers", "#131924", help="Layered panel tone")
    text_color = st.color_picker("Typography Fill", "#F0F4F8")
    
    # Advanced CSS Injection matching premium developer frameworks
    st.markdown(f"""
        <style>
            .stApp {{
                background-color: {bg_color};
                color: {text_color};
                font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
            }}
            h1, h2, h3, p, span, label, th, td {{
                color: {text_color} !important;
            }}
            /* Premium Dashboard Metric Cards */
            div[data-testid="stMetricValue"] {{
                color: {primary_color} !important;
                font-family: 'JetBrains Mono', monospace;
                font-weight: 700;
                font-size: 2.2rem !important;
            }}
            div[data-testid="metric-container"] {{
                background-color: {card_bg};
                padding: 20px;
                border-radius: 12px;
                border: 1px solid rgba(255,255,255,0.05);
                box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            }}
            /* Institutional Button Execution States */
            .stButton>button {{
                background: linear-gradient(135deg, {primary_color} 0%, #00CC52 100%) !important;
                color: #02060D !important;
                font-weight: 800;
                font-size: 1.05rem;
                letter-spacing: 0.5px;
                text-transform: uppercase;
                border-radius: 8px;
                border: none;
                padding: 14px 20px;
                width: 100%;
                transition: all 0.3s ease;
                box-shadow: 0 4px 15px rgba(0, 255, 102, 0.2);
            }}
            .stButton>button:hover {{
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(0, 255, 102, 0.3);
            }}
            /* Info Box & Strategic Insights Restyling */
            .stAlert {{
                background-color: {card_bg} !important;
                border-left: 5px solid {primary_color} !important;
                color: {text_color} !important;
                border-radius: 8px;
            }}
            /* Clean Section Dividers */
            hr {{
                border-color: rgba(255,255,255,0.08) !important;
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
# 📊 APP INTERFACE STRUCTURE
# ==========================================
st.markdown("<h1 style='text-align: center; font-weight: 800; margin-bottom: 5px;'>⚡ PRO AI CHART CORE TERMINAL</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #8A99AD !important; margin-bottom: 30px;'>Advanced Technical Scan Engine for XAUUSD, Crypto and Major Forex Pairs</p>", unsafe_allow_html=True)

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

st.markdown("---")

# Chart Drag-Drop Upload Panel
uploaded_file = st.file_uploader("", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    col1, col2 = st.columns([1.1, 0.9], gap="large")
    
    with col1:
        st.markdown("<h3 style='margin-bottom: 15px;'>🖼️ Live Market Context Capture</h3>", unsafe_allow_html=True)
        st.image(image, use_container_width=True)
        
    with col2:
        st.markdown("<h3 style='margin-bottom: 15px;'>🧠 Automated Execution Breakdown</h3>", unsafe_allow_html=True)
        run_analysis = st.button("🚀 Run Structural Core Analysis")
        
        if run_analysis:
            if not api_key:
                st.warning("Execution Halted: API Validation Token Missing from Sidebar Panel.")
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
                        
                        If a high-impact news catalyst like 'CPI', 'Retail Sales', or 'FOMC' is active, adjust the risk assessment: recommend wider Stop Losses to avoid spread wicks or suggest 'HOLD' if market risk is too high.
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
                            st.markdown("<div style='background-color: rgba(0, 255, 102, 0.1); border: 1px solid #00FF66; padding: 15px; border-radius: 8px; text-align: center; font-weight: bold; font-size: 1.2rem; color: #00FF66 !important; margin-bottom: 20px;'>🎯 POSITION STRATEGY: STRONG BUY SIGNAL</div>", unsafe_allow_html=True)
                        elif action == "SELL":
                            st.markdown("<div style='background-color: rgba(255, 51, 51, 0.1); border: 1px solid #FF3333; padding: 15px; border-radius: 8px; text-align: center; font-weight: bold; font-size: 1.2rem; color: #FF3333 !important; margin-bottom: 20px;'>🎯 POSITION STRATEGY: STRONG SELL SIGNAL</div>", unsafe_allow_html=True)
                        else:
                            st.markdown("<div style='background-color: rgba(241, 196, 15, 0.1); border: 1px solid #F1C40F; padding: 15px; border-radius: 8px; text-align: center; font-weight: bold; font-size: 1.2rem; color: #F1C40F !important; margin-bottom: 20px;'>🎯 POSITION STRATEGY: NEUTRAL MARKET STANDBY / HOLD</div>", unsafe_allow_html=True)
                            
                        # Layout Key Metrics Dashboard
                        m1, m2, m3 = st.columns(3)
                        m1.metric(label="📍 Target Entry", value=f"${analysis.get('entry'):,}")
                        m2.metric(label="🛑 Stop Loss (SL)", value=f"${analysis.get('stop_loss'):,}")
                        m3.metric(label="💰 Take Profit (TP)", value=f"${analysis.get('take_profit'):,}")
                        
                        st.markdown("<br>", unsafe_allow_html=True)
                        
                        # Position sizing display framework
                        st.subheader("⚖️ Risk Allocation Engine Order")
