import streamlit as st
from PIL import Image
import json
from google import genai
from google.genai import types

# Page Configurations for a clean, modern workspace
st.set_page_config(page_title="QUANT AI - Core Terminal", layout="wide", page_icon="⚡")

# =========================================================================
# 🎨 PREMIUM DARK NEON THEME ENGINE (Direct CSS Injection)
# =========================================================================
st.markdown("""
    <style>
        /* Base Canvas Gradient */
        .stApp {
            background: linear-gradient(135deg, #090e17 0%, #04060a 100%) !important;
            color: #f0f4f8 !important;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        }
        
        /* Global Typography Corrections */
        h1, h2, h3, p, span, label, th, td {
            color: #f0f4f8 !important;
        }
        
        /* Glassmorphic Metrics Card Matrix */
        div[data-testid="metric-container"] {
            background: rgba(19, 27, 42, 0.45) !important;
            backdrop-filter: blur(12px) !important;
            -webkit-backdrop-filter: blur(12px) !important;
            border: 1px solid rgba(255, 255, 255, 0.06) !important;
            border-radius: 16px !important;
            padding: 24px !important;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.4) !important;
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
        }
        div[data-testid="metric-container"]:hover {
            transform: translateY(-4px);
            border-color: #00ff66 !important;
            box-shadow: 0 12px 40px 0 rgba(0, 255, 102, 0.15) !important;
        }
        
        /* Ultra-Glow Metric Typography */
        div[data-testid="stMetricValue"] {
            color: #00ff66 !important;
            font-family: ui-monospace, SFMono-Regular, SF Mono, Menlo, Monaco, Consolas, monospace !important;
            font-weight: 700 !important;
            font-size: 2.3rem !important;
            letter-spacing: -0.5px;
            text-shadow: 0 0 20px rgba(0, 255, 102, 0.4);
        }
        
        /* Institutional Action Execution Button Styling */
        .stButton>button {
            background: linear-gradient(135deg, #00ff66 0%, #00b347 100%) !important;
            color: #02060d !important;
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
            margin-top: 10px;
        }
        .stButton>button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 30px rgba(0, 255, 102, 0.5) !important;
        }
        
        /* Modernized Form Input Selectors & File Drag Drops */
        div[data-testid="stFileUploader"] {
            background-color: rgba(19, 27, 42, 0.3) !important;
            border: 2px dashed rgba(255, 255, 255, 0.1) !important;
            border-radius: 16px !important;
            padding: 20px !important;
            transition: border-color 0.2s ease;
        }
        div[data-testid="stFileUploader"]:hover {
            border-color: #00ff66 !important;
        }
        
        /* Order execution notifications */
        .stAlert {
            background-color: rgba(19, 27, 42, 0.6) !important;
            border-left: 5px solid #00ff66 !important;
            color: #f0f4f8 !important;
            border-radius: 12px !important;
            backdrop-filter: blur(12px) !important;
        }
        
        /* Structural Layout Containment Dividers */
        hr {
            border-color: rgba(255, 255, 255, 0.08) !important;
            margin: 30px 0 !important;
        }
    </style>
""", unsafe_allow_html=True)

# =========================================================================
# 🔧 SIDEBAR CONFIGURATION ARCHITECTURE
# =========================================================================
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #00ff66; font-weight: 800; tracking-wide: 1px;'>⚡ TERMINAL</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.header("🔑 Authentication")
    api_key = st.text_input("Gemini API Private Token", type="password", help="Input your verification credentials from Google AI Studio")
    
    st.markdown("---")
    st.header("⚖️ Risk Vector Space")
    account_balance = st.number_input("Capital Pool Balance ($)", min_value=10, value=10000, step=100)
    risk_percentage = st.slider("Session Equity Risk (%)", min_value=0.25, max_value=5.0, value=1.0, step=0.25)
    risk_reward = st.slider("Target Yield Ratio (R:R)", min_value=1.0, max_value=4.0, value=2.0, step=0.5)
    
    allowed_risk_usd = (account_balance * risk_percentage) / 100
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.metric(label="Absolute Dollar Exposure Limit", value=f"${allowed_risk_usd:,.2f}")

# =========================================================================
# 📊 MAIN INTERFACE CORE PLATFORM
# =========================================================================
st.markdown("<h1 style='text-align: center; font-weight: 900; letter-spacing: -1.5px; margin-bottom: 0px;'>⚡ QUANT AI CORE TERMINAL</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #8a99ad; font-size: 1.1rem; margin-bottom: 40px;'>Institutional Grade High-Speed Vision Scan Engine for Gold & Crypto</p>", unsafe_allow_html=True)

# Macro Fundamental Calendars Selector Matrix
st.markdown("### 📰 Session Fundamental Filters")
news_catalyst = st.selectbox(
    "Active Macroeconomic Conditions:",
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

# Visual Data Input Drop Box Section
st.markdown("### 🖼️ Context Input Vector")
uploaded_file = st.file_uploader("Upload market structure chart screenshot capture...", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    col1, col2 = st.columns([1.1, 0.9], gap="large")
    
    with col1:
        st.markdown("<h4 style='margin-bottom: 20px; color: #8a99ad !important;'>🖼️ Input Capture Array</h4>", unsafe_allow_html=True)
        st.image(image, use_container_width=True)
        
    with col2:
        st.markdown("<h4 style='margin-bottom: 20px; color: #8a99ad !important;'>🧠 Computed Output Plan</h4>", unsafe_allow_html=True)
        run_analysis = st.button("🚀 Execute System Analysis Run")
        
        if run_analysis:
            if not api_key:
                st.warning("Execution Terminated: API Authentication Token is Missing.")
            else:
                with st.spinner("⚡ Running data synthesis scan..."):
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
                    
                    # Premium Output Formatting Badges
                    if action == "BUY":
                        st.markdown("<div style='background: rgba(0, 255, 102, 0.1); border: 1px solid #00ff66; padding: 16px; border-radius: 12px; font-weight: 800; font-size: 1.2rem; color: #00ff66 !important; text-align: center; letter-spacing: 0.5px;'>🎯 TRADING MATRIX STRATEGY: STRONG BUY SIGNAL</div>", unsafe_allow_html=True)
                    elif action == "SELL":
