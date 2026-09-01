import streamlit as st
import pandas as pd

# 1. Page Configuration (Using Official Plus AI Favicon URL)
st.set_page_config(
    page_title="Plus AI | Enterprise ROI and Deployment Simulator",
    page_icon="https://plusai.com/favicon.svg",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Comprehensive Operational Glossary Definition
GLOSSARY_DATA = [
    {
        "Term": "Active Slide Creators",
        "Context and Operational Meaning": "The total count of employees, consultants, sales representatives, or analysts within an organization who regularly build, format, and deliver presentations as part of their work."
    },
    {
        "Term": "Annual Hours Reclaimed",
        "Context and Operational Meaning": "The aggregate working hours returned to an organization over twelve months by eliminating manual slide formatting, alignment tasks, and repetitive layout adjustments."
    },
    {
        "Term": "Annual Value Delivered",
        "Context and Operational Meaning": "The bottom line financial capacity unlocked across the workforce, calculated as total annual hours reclaimed multiplied by the average fully loaded hourly rate."
    },
    {
        "Term": "Brand Architecture Tier",
        "Context and Operational Meaning": "The organizational complexity of a client design system, ranging from a single corporate identity to complex enterprise architectures with multiple subsidiary sub brands."
    },
    {
        "Term": "Currency Selection",
        "Context and Operational Meaning": "Standardizes financial capacity calculations across global client operations to model exact local currency savings."
    },
    {
        "Term": "Deck Velocity",
        "Context and Operational Meaning": "The total volume of completed slide presentations produced, reviewed, and finalized by an organization over a monthly operational cycle."
    },
    {
        "Term": "Deployment Complexity Tier",
        "Context and Operational Meaning": "The technical and operational effort required to integrate custom corporate branding, single sign on permissions, and template governance into enterprise workspaces."
    },
    {
        "Term": "Design Tokens",
        "Context and Operational Meaning": "Standardized, centralized data variables for colors, typography scales, spacing margins, and corner radii that enforce visual consistency across presentations programmatically."
    },
    {
        "Term": "Fully Loaded Hourly Rate",
        "Context and Operational Meaning": "The total real cost of a knowledge worker per hour, including gross salary, payroll taxes, health benefits, software licensing, and operational overhead."
    },
    {
        "Term": "Layout Bounding Box",
        "Context and Operational Meaning": "The predefined mathematical limits on a slide that restrict text and image containers from spilling over margins or colliding with adjacent graphical components."
    },
    {
        "Term": "Linter",
        "Context and Operational Meaning": "An automated programmatic scanner that evaluates text and slide layouts against strict design rules to catch overflow defects, awkward line wraps, and hierarchy violations before delivery."
    },
    {
        "Term": "Manual Formatting Hours",
        "Context and Operational Meaning": "The non strategic time a professional loses manually resizing shapes, fixing table alignments, wrestling text wrapping, and adjusting font sizes on a single presentation."
    },
    {
        "Term": "Runtime Compatibility",
        "Context and Operational Meaning": "The guarantee that an automated presentation renders with pixel perfect visual fidelity across both Google Slides and Microsoft PowerPoint without layout drift."
    },
    {
        "Term": "Slide Slop",
        "Context and Operational Meaning": "Unpolished, generic artificial intelligence presentation output characterized by broken layouts, awkward line wraps, clashing color pills, and inconsistent visual hierarchy."
    },
    {
        "Term": "Template Ingestion",
        "Context and Operational Meaning": "The operational process of importing master corporate presentation files, extracting style variables, and codifying layout rules into automated generation schemas."
    },
    {
        "Term": "30, 60,90 Day Roadmap",
        "Context and Operational Meaning": "A phased enterprise deployment framework divided into thirty days of technical ingestion, sixty days of team activation, and ninety days of organization wide scale."
    },
    {
        "Term": "Usage Telemetry",
        "Context and Operational Meaning": "Aggregated, privacy compliant operational data that tracks template adoption frequency, slide generation volume, and active user engagement across departments."
    }
]

df_glossary_master = pd.DataFrame(GLOSSARY_DATA).sort_values(by="Term").reset_index(drop=True)

# Helper function to generate term with explanation tooltip
def tooltip_span(term_name, definition_text):
    return f'<span style="text-decoration: underline dotted; cursor: help; font-weight: 500;" title="{definition_text}">{term_name}</span>'

# Custom CSS
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
    .custom-footer {
        margin-top: 60px;
        padding-top: 20px;
        border-top: 1px solid #E2E8F0;
        text-align: center;
        color: #64748B;
        font-size: 14px;
        font-family: 'Inter', sans-serif;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("Plus AI: Enterprise Return on Investment and Deployment Simulator")
st.caption("A strategic decision tool for Enterprise Go to Market strategy, financial modeling, and deployment planning.")
st.divider()

# Top Section: Control Center & Inputs
with st.expander("Configuration and Organization Parameters (Click to Expand or Collapse)", expanded=True):
    st.markdown("### Client Organization Parameters")
    
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
            help="Total knowledge workers, consultants, or sales reps actively creating or modifying presentations."
        )
        
    with col_top3:
        final_decks_per_month = st.number_input(
            "Average Decks Created per User per Month",
            min_value=0.5,
            max_value=100.0,
            value=6.0,
            step=0.5,
            format="%.1f",
            help="Estimated volume of presentations created, edited, or updated per employee every month."
        )
        
    with col_top4:
        final_hours_per_deck = st.number_input(
            "Manual Hours Spent Formatting per Deck",
            min_value=0.1,
            max_value=40.0,
            value=3.5,
            step=0.25,
            format="%.2f",
            help="Average time a professional spends aligning shapes, fixing margins, and manually styling slides."
        )

    st.markdown("---")
    
    col_sub1, col_sub2 = st.columns([1, 2])
    
    with col_sub1:
        hourly_rate = st.number_input(
            f"Average Knowledge Worker Hourly Rate ({curr})",
            min_value=1.00,
            max_value=2500.00,
            value=75.00,
            step=0.25,
            format="%.2f",
            help="Fully loaded hourly cost including salary and overhead of professionals creating presentations."
        )
        
    with col_sub2:
        brand_tier = st.selectbox(
            "Brand and Template Architecture Tier",
            options=[
                "Standard (Single Corporate Identity)",
                "Multi Brand (Two to Four Sub Brands and Business Units)",
                "Global Enterprise (Complex Design System and Custom Tokens)"
            ],
            help="Defines organizational design complexity from single template schemas to multi unit corporate brands."
        )

# Core Business Logic Calculations
total_monthly_decks = final_team_size * final_decks_per_month
hours_saved_per_deck = final_hours_per_deck * 0.65  # 65% efficiency gain
monthly_hours_saved = total_monthly_decks * hours_saved_per_deck
annual_hours_saved = monthly_hours_saved * 12
annual_cost_savings = annual_hours_saved * hourly_rate

st.markdown("### Executive Performance Impact Summary")

# Display Key Metrics
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
    elif "Multi Brand" in brand_tier:
        st.metric(
            "Deployment Tier",
            "Tier 2: Multi Brand",
            delta="Phased Rollout",
            help="Multi unit architecture supporting distinct corporate sub brands and token sets."
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
tab1, tab2, tab3, tab4 = st.tabs([
    "Return on Investment and Capacity Modeling",
    "30, 60, 90 Day Deployment Playbook",
    "Slide Slop Linter Demonstration",
    "Glossary and Terminology Index"
])

with tab1:
    st.subheader("Financial and Capacity Impact Analysis")
    st.write("Modeling the cumulative capacity and time value across the organization over twelve months:")
    
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
    st.subheader(f"Tailored 30, 60, 90 Day Deployment Roadmap: {brand_tier.split(' ')[0]}")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("### Days 1 to 30: Ingestion")
        st.markdown("""
        * Security, workspace provisioning and single sign on configuration
        * Brand asset and template token extraction
        * Admin permissioning and initial pilot cohort activation
        """)
    with c2:
        st.markdown("### Days 31 to 60: Activation")
        st.markdown("""
        * Team onboarding sessions and workflow champion workshops
        * Biweekly template usage telemetry and engagement tracking
        * First one hundred enterprise presentations generated in production
        """)
    with c3:
        st.markdown("### Days 61 to 90: Scale")
        st.markdown("""
        * Executive value review and operational time savings audit
        * Custom theme expansion across remaining business units
        * Transition from pilot cohort to full organization wide standard
        """)

with tab3:
    st.subheader("Interactive Slide Slop Linter Demonstration")
    
    linter_expl = "An automated programmatic scanner that evaluates text and slide layouts against strict design rules to catch overflow defects before delivery."
    tokens_expl = "Standardized variables for colors, typography scales, and margins that enforce visual consistency across presentations."
    runtime_expl = "The guarantee that an automated presentation renders with pixel perfect visual fidelity across both Google Slides and Microsoft PowerPoint."
    
    st.markdown(
        f"See how an automated {tooltip_span('Linter', linter_expl)} enforcing strict {tooltip_span('Design Tokens', tokens_expl)} prevents layout overflow and guarantees {tooltip_span('Runtime Compatibility', runtime_expl)} across Google Slides and Microsoft PowerPoint:",
        unsafe_allow_html=True
    )
    
    sample_text = st.text_area(
        "Enter sample executive headline or body text to test layout container responsiveness:",
        value="Accelerating Enterprise Revenue Velocity Across Global Distributed Teams",
        help="Type or paste sample slide text to test container responsiveness against layout rules."
    )
    
    char_count = len(sample_text)
    
    col_linter1, col_linter2 = st.columns(2)
    with col_linter1:
        st.markdown("**Without Plus Token Linting (Artificial Intelligence Slop Anti Pattern):**")
        st.error(f"Overflow Risk: Multi line text ({char_count} characters) may wrap awkwardly over background graphics or force text scaling distortions.")
    with col_linter2:
        st.markdown("**With Plus Structured Layout Engine:**")
        st.success("Safe Layout Schema: Content dynamically conforms to strict sixteen by nine bounding boxes, auto padding, and hierarchy guardrails.")

with tab4:
    st.subheader("Glossary and Operational Terminology Index")
    st.write("Alphabetical reference directory of all technical, operational, and financial terms used across this application:")
    
    col_search, col_filter = st.columns([2, 1])
    with col_search:
        search_query = st.text_input("Search terms by keyword:", value="", placeholder="Type any word such as linter, token, telemetry, roi...")
    with col_filter:
        selected_term_dropdown = st.selectbox(
            "Filter by specific term:",
            options=["All Terms"] + list(df_glossary_master["Term"].values)
        )
    
    # Filter Logic
    df_filtered = df_glossary_master.copy()
    if selected_term_dropdown != "All Terms":
        df_filtered = df_filtered[df_filtered["Term"] == selected_term_dropdown]
    elif search_query.strip():
        q = search_query.strip().lower()
        df_filtered = df_filtered[
            df_filtered["Term"].str.lower().str.contains(q) | 
            df_filtered["Context and Operational Meaning"].str.lower().str.contains(q)
        ]
    
    st.dataframe(df_filtered, use_container_width=True, hide_index=True)

# 3. Clean Dedicated Footer
st.markdown('<div class="custom-footer">Built by Robin Sylvester</div>', unsafe_allow_html=True)
