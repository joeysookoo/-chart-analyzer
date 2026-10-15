import streamlit as st
from PIL import Image
import json
from google import genai
from google.genai import types

# Page Configurations
st.set_page_config(page_title="Pro AI Chart & News Analyzer", layout="wide", page_icon="📈")

# ==========================================
# 🎨 CUSTOM LAYOUT & THEME ENGINE
# ==========================================
with st.sidebar:
    st.header("🎨 Theme & Layout Customization")
    primary_color = st.color_picker("Primary Accent Color", "#00FF66")
    bg_color = st.color_picker("Background Style", "#0E1117")
    text_color = st.color_picker("Text Color", "#FFFFFF")
    
    st.markdown(f"""
        <style>
            .stApp {{ background-color: {bg_color}; color: {text_color}; }}
            h1, h2, h3, p, span, label {{ color: {text_color} !important; }}
            div[data-testid="stMetricValue"] {{ color: {primary_color} !important; font-family: 'JetBrains Mono', monospace; }}
            .stButton>button {{
                background-color: {primary_color} !important; color: #000000 !important;
                font-weight: bold; border-radius: 8px; border: none; width: 100%;
            }}
        </style>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.header("🔧 Risk Management Profile")
    api_key = st.text_input("Enter Gemini API Key", type="password")
    
    st.markdown("---")
    account_balance = st.number_input("💰 Account Balance ($)", min_value=10, value=10000, step=100)
    risk_percentage = st.slider("⚠️ Risk Per Trade (%)", min_value=0.25, max_value=5.0, value=1.0, step=0.25)
    risk_reward = st.slider("🎯 Target Risk-to-Reward Ratio", min_value=1.0, max_value=4.0, value=2.0, step=0.5)
    
    allowed_risk_usd = (account_balance * risk_percentage) / 100
    st.metric(label="Total Cash At Risk", value=f"${allowed_risk_usd:,.2f}")

# ==========================================
# 📊 MAIN INTERFACE & NEWS FILTERS
# ==========================================
st.markdown("# 📈 Pro AI Visual Chart & News Analyzer")
st.markdown("Combines chart structural analytics with high-impact economic news indicators.")

# 📰 Dynamic News Catalyst Selector
st.subheader("📰 Step 1: Select Today's Economic Calendar Filters")
news_catalyst = st.selectbox(
    "Select high-impact news events dropping today / this session:",
    [
        "None / Clear Market Environment",
        "US Core Retail Sales Data Release (High Volatility)",
        "US CPI / PPI Inflation Print (Extreme Volatility for XAUUSD)",
        "US Initial Jobless Claims / Employment Data",
        "FOMC Interest Rate Decision / Central Bank Speeches",
        "Geopolitical Tensions / Sudden Global Market Risk Shifts"
    ]
)

custom_news = st.text_input("Or type custom market news factors manually (Optional):", "")
active_news = custom_news if custom_news else news_catalyst

st.markdown("---")
st.subheader("🖼️ Step 2: Upload Chart Capture")
uploaded_file = st.file_uploader("Drop your chart screenshot here...", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🖼️ Uploaded Chart")
        st.image(image, use_container_width=True)
        
    with col2:
        st.subheader("🧠 Risk & News Assessment Analysis")
        run_analysis = st.button("🚀 Analyze Position Size & News Strategy")
        
        if run_analysis:
            if not api_key:
                st.warning("Please provide a valid Gemini API Key in the sidebar panel.")
            else:
                with st.spinner("⚡ Running data synthesis scan..."):
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
                            st.success("🎯 SIGNAL GENERATED: STRONG BUY")
                        elif action == "SELL":
                            st.error("🎯 SIGNAL GENERATED: STRONG SELL")
                        else:
                            st.warning("🎯 SIGNAL GENERATED: HOLD / NO SYSTEM SETUP")
                            
                        m1, m2, m3 = st.columns(3)
                        m1.metric(label="📍 Recommended Entry", value=f"${analysis.get('entry'):,}")
                        m2.metric(label="🛑 Invalidation (Stop Loss)", value=f"${analysis.get('stop_loss'):,}")
                        m3.metric(label="💰 Objective (Take Profit)", value=f"${analysis.get('take_profit'):,}")
                        
                        st.markdown("---")
                        
                        st.subheader("⚖️ Precision Order Execution")
                        st.info(f"👉 **EXECUTION SIZE:** Use **{analysis.get('lot_size')}** to ensure total risk stays fixed at exactly **${allowed_risk_usd:,.2f}**.")
                        
                        st.markdown(f"### 📰 Macro Assessment: **{analysis.get('news_impact_rating')}**")
                        st.markdown("### 🔍 Market Structure Reasoning")
                        st.write(analysis.get("reasoning"))
                        
                    except Exception as e:
                        st.error(f"System Parsing Error: {str(e)}")
