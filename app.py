import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Plus AI | Enterprise ROI & Intake Simulator",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom Styling for Plus AI Theme & Metric Wrap
st.markdown("""
<style>
    .main {
        background-color: #FFFFFF;
    }
    div[data-testid="stMetricValue"] > div {
        font-size: 24px !important;
        white-space: normal !important;
        word-break: break-word !important;
        overflow-wrap: break-word !important;
    }
    .stMetric {
        background-color: #F8FAFC;
        padding: 16px;
        border-radius: 8px;
        border: 1px solid #E2E8F0;
        min-height: 125px;
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

# Top Section: Control Center & Inputs (No Sidebar)
with st.expander("⚙️ Configuration & Organization Parameters (Click to Expand / Collapse)", expanded=True):
    st.markdown("### 1. Client Organization Parameters")
    
    col_top1, col_top2, col_top3, col_top4 = st.columns(4)
    
    with col_top1:
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
        selected_currency_full = st.selectbox(
            "Currency",
            options=currency_options,
            index=0,
            help="Select the operational currency to standardize financial return modeling across global teams."
        )
        curr = selected_currency_full.split(" ")[0]
        
    with col_top2:
        final_team_size = st.number_input(
            "Active Slide Creators (Seats)",
            min_value=1,
            max_value=10000,
            value=50,
            step=1,
            help="Total knowledge workers, consultants, or sales reps actively creating or modifying slides."
        )
        
    with col_top3:
        final_decks_per_month = st.number_input(
            "Avg Decks Created / User / Month",
            min_value=0.5,
            max_value=100.0,
            value=6.0,
            step=0.5,
            format="%.1f",
            help="Estimated volume of presentations created, edited, or updated per employee every month."
        )
        
    with col_top4:
        final_hours_per_deck = st.number_input(
            "Manual Hours Formatting / Deck",
            min_value=0.1,
            max_value=40.0,
            value=3.5,
            step=0.25,
            format="%.2f",
            help="Average time a professional spends aligning text boxes, fixing margins, and manually styling slides."
        )

    st.markdown("---")
    
    col_sub1, col_sub2 = st.columns([1, 2])
    
    with col_sub1:
        hourly_rate = st.number_input(
            f"Avg Knowledge Worker Hourly Rate ({curr})",
            min_value=1.00,
            max_value=2500.00,
            value=75.00,
            step=0.25,
            format="%.2f",
            help="Fully-loaded hourly cost (salary + benefits) of professionals creating presentations."
        )
        
    with col_sub2:
        brand_tier = st.selectbox(
            "Brand & Template Architecture Tier",
            options=[
                "Standard (Single Corporate Identity)",
                "Multi-Brand (2-4 Sub-Brands & Business Units)",
                "Global Enterprise (Complex Design System & Custom Tokens)"
            ],
            help="Defines the complexity of your design system: single template vs. multi-subsidiary tokenized schemas."
        )

# Core Business Logic Calculations
total_monthly_decks = final_team_size * final_decks_per_month
hours_saved_per_deck = final_hours_per_deck * 0.65  # 65% efficiency gain using Plus AI
monthly_hours_saved = total_monthly_decks * hours_saved_per_deck
annual_hours_saved = monthly_hours_saved * 12
annual_cost_savings = annual_hours_saved * hourly_rate

st.markdown("### Executive Performance Impact Summary")

# Display Key Metrics (Full Width Grid)
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Annual Hours Reclaimed",
        f"{annual_hours_saved:,.1f} hrs",
        help="Total hours saved across the team by eliminating manual slide formatting friction."
    )
with col2:
    st.metric(
        "Annual Value Delivered",
        f"{curr}{annual_cost_savings:,.2f}",
        help="Net financial capacity unlocked, calculated as total hours reclaimed multiplied by hourly rate."
    )
with col3:
    st.metric(
        "Monthly Deck Velocity",
        f"{total_monthly_decks:,.0f} decks",
        help="Aggregate presentation output generated monthly across all active user seats."
    )
with col4:
    if "Standard" in brand_tier:
        st.metric(
            "Deployment Tier",
            "Tier 1: Standard",
            delta="Fast Direct Access",
            help="Single brand template ingestion with standard workspace provisioning."
        )
    elif "Multi-Brand" in brand_tier:
        st.metric(
            "Deployment Tier",
            "Tier 2: Multi-Brand",
            delta="Phased Rollout",
            help="Multi-unit architecture supporting 2-4 distinct corporate sub-brands and token sets."
        )
    else:
        st.metric(
            "Deployment Tier",
            "Tier 3: Enterprise",
            delta="Custom Dedicated",
            help="Complex enterprise design system integration with custom token linting and custom governance."
        )

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
        value="Accelerating Enterprise Revenue Velocity Across Global Distributed Teams",
        help="Type or paste sample slide text to test container responsiveness against layout rules."
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
