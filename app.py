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
st.caption("A strategic decision tool for Enterprise GTM, ROI calculation, and 30,60,90 day deployment planning.")
st.divider()

# Sidebar: Inputs
st.sidebar.header("1. Client Organization Parameters")

team_size = st.sidebar.slider("Enterprise Team Size (Seats)", min_value=10, max_value=2500, value=250, step=10)
decks_per_week = st.sidebar.slider("Average Decks Created per User / Month", min_value=1, max_value=20, value=6, step=1)
hours_per_deck = st.sidebar.slider("Current Manual Hours Spent per Deck", min_value=1.0, max_value=8.0, value=3.5, step=0.5)
hourly_rate = st.sidebar.number_input("Average Hourly Rate of Knowledge Worker ($ USD)", min_value=30, max_value=300, value=85, step=5)

st.sidebar.divider()
st.sidebar.header("2. Brand Architecture Complexity")
brand_tier = st.sidebar.selectbox(
    "Brand & Template Architecture Tier",
    options=["Standard (Single Corporate Identity)", "Multi-Brand (2-4 Sub-Brands & Business Units)", "Global Enterprise (Complex Design System & Custom Tokens)"]
)

# Core Business Logic Calculations
total_monthly_decks = team_size * decks_per_week
hours_saved_per_deck = hours_per_deck * 0.65  # 65% efficiency gain using Plus AI
monthly_hours_saved = total_monthly_decks * hours_saved_per_deck
annual_hours_saved = monthly_hours_saved * 12
annual_cost_savings = annual_hours_saved * hourly_rate

# Display Key Metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Annual Hours Reclaimed", f"{int(annual_hours_saved):,} hrs")
with col2:
    st.metric("Annual Cost Savings", f"${int(annual_cost_savings):,}")
with col3:
    st.metric("Monthly Deck Velocity", f"{int(total_monthly_decks):,} decks")
with col4:
    if "Standard" in brand_tier:
        st.metric("Deployment Complexity", "Low (Tier 1)", delta="Fast Rollout")
    elif "Multi-Brand" in brand_tier:
        st.metric("Deployment Complexity", "Moderate (Tier 2)", delta="Phased")
    else:
        st.metric("Deployment Complexity", "High (Tier 3)", delta="Enterprise Dedicated")

st.divider()

# Interactive Tabs
tab1, tab2, tab3 = st.tabs(["📊 ROI & Capacity Modeling", "🚀 30-60-90 Deployment Playbook", "🛡️ Slide Slop Linter Demo"])

with tab1:
    st.subheader("Financial & Capacity Impact Analysis")
    st.write("Modeling the bottom-line capacity expansion across the organization:")
    
    # Simple Monthly Breakdown Table
    months = [f"Month {i}" for i in range(1, 13)]
    cumulative_hours = [int(monthly_hours_saved * i) for i in range(1, 13)]
    cumulative_savings = [int(monthly_hours_saved * hourly_rate * i) for i in range(1, 13)]
    
    df_roi = pd.DataFrame({
        "Timeline": months,
        "Cumulative Hours Saved": cumulative_hours,
        "Cumulative Financial Return ($)": cumulative_savings
    })
    
    st.dataframe(df_roi, use_container_width=True)

with tab2:
    st.subheader(f"Tailored 30-60-90 Day Deployment Roadmap: {brand_tier.split(' ')[0]}")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("### Days 1–30: Ingestion")
        st.markdown("""
        - Security, SOC2 & Workspace provisioning
        - Master template token extraction from Figma
        - Admin permissioning & pilot cohort onboarding
        """)
    with c2:
        st.markdown("### Days 31–60: Activation")
        st.markdown("""
        - Departmental champion training workshops
        - Bi-weekly template usage telemetry tracking
        - First 100 enterprise decks generated in production
        """)
    with c3:
        st.markdown("### Days 61–90: Scale")
        st.markdown("""
        - Executive value review & ROI audit
        - Custom theme expansion across remaining business units
        - Transition from pilot to full enterprise multi-year agreement
        """)

with tab3:
    st.subheader("Interactive 'Slide Slop' Linter Demonstration")
    st.write("See how strict design token schemas prevent layout overflow and maintain layout fidelity across Google Slides and PowerPoint:")
    
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

st.caption("Built by Robin Sylvester | Candidate for Business Operations Lead at Plus AI")
