import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Plus AI | Enterprise ROI & Intake Simulator",
    page_icon="✨",
    layout="wide"
)

# Custom Styling for Plus AI Theme
st.markdown("""
<style>
    .main {
        background-color: #FFFFFF;
    }
    .stMetric {
        background-color: #F8FAFC;
        padding: 16px;
        border-radius: 8px;
        border: 1px solid #E2E8F0;
    }
    h1, h2, h3 {
        color: #18186D;
        font-family: 'Inter', sans-serif;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("Plus AI: Enterprise ROI & Deployment Simulator")
st.caption("A strategic decision tool for Enterprise GTM, ROI calculation, and 30-60-90 day deployment planning.")
st.divider()

# Sidebar: Inputs
st.sidebar.header("1. Client Organization Parameters")

# Comprehensive 25+ Global Currencies
currency_options = [
    "$ USD - US Dollar",
    "$ CAD - Canadian Dollar",
    "$ AUD - Australian Dollar",
    "€ EUR - Euro",
    "£ GBP - British Pound",
    "¥ JPY - Japanese Yen",
    "₹ INR - Indian Rupee",
    "$ SGD - Singapore Dollar",
    "$ HKD - Hong Kong Dollar",
    "CHF - Swiss Franc",
    "$ NZD - New Zealand Dollar",
    "kr SEK - Swedish Krona",
    "kr NOK - Norwegian Krone",
    "kr DKK - Danish Krone",
    "₩ KRW - South Korean Won",
    "R$ BRL - Brazilian Real",
    "$ MXN - Mexican Peso",
    "AED - UAE Dirham",
    "SAR - Saudi Riyal",
    "zł PLN - Polish Zloty",
    "TL TRY - Turkish Lira",
    "R ZAR - South African Rand",
    "$ TWD - New Taiwan Dollar",
    "฿ THB - Thai Baht",
    "Rp IDR - Indonesian Rupiah",
    "RM MYR - Malaysian Ringgit",
    "₱ PHP - Philippine Peso",
    "₫ VND - Vietnamese Dong"
]

selected_currency_full = st.sidebar.selectbox("Currency Selection", options=currency_options, index=0)
curr = selected_currency_full.split(" ")[0]

# Slider + Exact Number Input for Team Size
st.sidebar.markdown("**Active Slide Creators / Team Seats**")
c_team1, c_team2 = st.sidebar.columns([2, 1])
with c_team2:
    team_size_input = st.number_input("Seats Input", min_value=1, max_value=10000, value=50, step=1, label_visibility="collapsed")
with c_team1:
    team_size = st.slider("Seats Slider", min_value=1, max_value=2500, value=min(int(team_size_input), 2500), step=1, label_visibility="collapsed")
final_team_size = team_size_input if team_size_input != 50 and team_size == 50 else team_size

# Slider + Exact Number Input for Decks per Month
st.sidebar.markdown("**Average Decks Created per User / Month**")
c_deck1, c_deck2 = st.sidebar.columns([2, 1])
with c_deck2:
    decks_input = st.number_input("Decks Input", min_value=0.5, max_value=100.0, value=6.0, step=0.5, format="%.1f", label_visibility="collapsed")
with c_deck1:
    decks_slider = st.slider("Decks Slider", min_value=1.0, max_value=30.0, value=min(float(decks_input), 30.0), step=0.5, label_visibility="collapsed")
final_decks_per_month = decks_input if decks_input != 6.0 and decks_slider == 6.0 else decks_slider

# Slider + Exact Number Input for Hours Spent per Deck
st.sidebar.markdown("**Current Manual Hours Spent Formatting per Deck**")
c_hrs1, c_hrs2 = st.sidebar.columns([2, 1])
with c_hrs2:
    hours_input = st.number_input("Hours Input", min_value=0.1, max_value=40.0, value=3.5, step=0.25, format="%.2f", label_visibility="collapsed")
with c_hrs1:
    hours_slider = st.slider("Hours Slider", min_value=0.5, max_value=10.0, value=min(float(hours_input), 10.0), step=0.25, label_visibility="collapsed")
final_hours_per_deck = hours_input if hours_input != 3.5 and hours_slider == 3.5 else hours_slider

# Hourly Rate with Two Decimals
st.sidebar.markdown(f"**Average Hourly Rate of Knowledge Worker ({curr})**")
hourly_rate = st.sidebar.number_input(
    "Hourly Rate",
    min_value=1.00,
    max_value=2500.00,
    value=75.00,
    step=0.25,
    format="%.2f",
    label_visibility="collapsed"
)

st.sidebar.divider()
st.sidebar.header("2. Brand Architecture Complexity")
brand_tier = st.sidebar.selectbox(
    "Brand & Template Architecture Tier",
    options=[
        "Standard (Single Corporate Identity)",
        "Multi-Brand (2-4 Sub-Brands & Business Units)",
        "Global Enterprise (Complex Design System & Custom Tokens)"
    ]
)

# Core Business Logic Calculations
total_monthly_decks = final_team_size * final_decks_per_month
hours_saved_per_deck = final_hours_per_deck * 0.65  # 65% efficiency gain using Plus AI
monthly_hours_saved = total_monthly_decks * hours_saved_per_deck
annual_hours_saved = monthly_hours_saved * 12
annual_cost_savings = annual_hours_saved * hourly_rate

# Display Key Metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Annual Hours Reclaimed", f"{annual_hours_saved:,.1f} hrs")
with col2:
    st.metric("Annual Value Delivered", f"{curr}{annual_cost_savings:,.2f}")
with col3:
    st.metric("Monthly Deck Velocity", f"{total_monthly_decks:,.0f} decks")
with col4:
    if "Standard" in brand_tier:
        st.metric("Deployment Complexity", "Standard (Tier 1)", delta="Immediate Access")
    elif "Multi-Brand" in brand_tier:
        st.metric("Deployment Complexity", "Moderate (Tier 2)", delta="Phased Rollout")
    else:
        st.metric("Deployment Complexity", "Advanced (Tier 3)", delta="Enterprise Dedicated")

st.divider()

# Interactive Tabs
tab1, tab2, tab3 = st.tabs(["📊 ROI & Capacity Modeling", "🚀 30-60-90 Deployment Playbook", "🛡️ Slide Slop Linter Demo"])

with tab1:
    st.subheader("Financial & Capacity Impact Analysis")
    st.write("Modeling the cumulative capacity and time value across the organization:")
    
    # Monthly Breakdown Table
    months = [f"Month {i}" for i in range(1, 13)]
    cumulative_hours = [monthly_hours_saved * i for i in range(1, 13)]
    cumulative_savings = [monthly_hours_saved * hourly_rate * i for i in range(1, 13)]
    
    df_roi = pd.DataFrame({
        "Timeline": months,
        "Cumulative Hours Saved": [f"{hrs:,.1f}" for hrs in cumulative_hours],
        f"Cumulative Value ({curr})": [f"{curr}{val:,.2f}" for val in cumulative_savings]
    })
    
    st.dataframe(df_roi, use_container_width=True)

with tab2:
    st.subheader(f"Tailored 30-60-90 Day Deployment Roadmap: {brand_tier.split(' ')[0]}")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("### Days 1–30: Ingestion")
        st.markdown("""
        - Security, workspace provisioning & single sign-on configuration
        - Brand asset & template token extraction
        - Admin permissioning & initial pilot cohort activation
        """)
    with c2:
        st.markdown("### Days 31–60: Activation")
        st.markdown("""
        - Team onboarding sessions & workflow champion workshops
        - Bi-weekly template usage telemetry & engagement tracking
        - First 100 enterprise presentations generated in production
        """)
    with c3:
        st.markdown("### Days 61–90: Scale")
        st.markdown("""
        - Executive value review & operational time-savings audit
        - Custom theme expansion across remaining business units
        - Transition from pilot cohort to full organization-wide standard
        """)

with tab3:
    st.subheader("Interactive 'Slide Slop' Linter Demonstration")
    st.write("See how strict design token schemas prevent layout overflow and maintain formatting fidelity across Google Slides and PowerPoint:")
    
    sample_text = st.text_area(
        "Enter sample executive headline or body text to test layout container responsiveness:",
        value="Accelerating Enterprise Revenue Velocity Across Global Distributed Teams"
    )
    
    char_count = len(sample_text)
    
    col_linter1, col_linter2 = st.columns(2)
    with col_linter1:
        st.markdown("**Without Plus Token Linting (AI Slop Anti-Pattern):**")
        st.error(f"❌ Overflow Risk: Multi-line text ({char_count} chars) may wrap awkwardly over background graphics or force text scaling distortions.")
    with col_linter2:
        st.markdown("**With Plus Structured Layout Engine:**")
        st.success(f"✅ Safe Layout Schema: Content dynamically conforms to strict 16:9 bounding boxes, auto-padding, and hierarchy guardrails.")

st.caption("Built by Robin Sylvester")
