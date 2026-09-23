import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="Plus AI | Enterprise ROI & Deployment Simulator",
    page_icon="https://plusai.com/favicon.svg",
    layout="wide",
    initial_sidebar_state="collapsed",
)

GLOSSARY_DATA = [
    {
        "Term": "Active Slide Creators",
        "Context and Operational Meaning": "The total count of employees, consultants, sales representatives, or analysts within an organization who regularly build, format, and deliver presentations as part of their work.",
    },
    {
        "Term": "Annual Hours Reclaimed",
        "Context and Operational Meaning": "The aggregate working hours returned to an organization over twelve months by eliminating manual slide formatting, alignment tasks, and repetitive layout adjustments.",
    },
    {
        "Term": "Annual Value Delivered",
        "Context and Operational Meaning": "The bottom line financial capacity unlocked across the workforce, calculated as total annual hours reclaimed multiplied by the average fully loaded hourly rate.",
    },
    {
        "Term": "Brand Architecture Tier",
        "Context and Operational Meaning": "The organizational complexity of a client design system, ranging from a single corporate identity to complex enterprise architectures with multiple subsidiary sub brands.",
    },
    {
        "Term": "Currency Selection",
        "Context and Operational Meaning": "Standardizes financial capacity calculations across global client operations to model exact local currency savings.",
    },
    {
        "Term": "Deck Velocity",
        "Context and Operational Meaning": "The total volume of completed slide presentations produced, reviewed, and finalized by an organization over a monthly operational cycle.",
    },
    {
        "Term": "Deployment Complexity Tier",
        "Context and Operational Meaning": "The technical and operational effort required to integrate custom corporate branding, single sign on permissions, and template governance into enterprise workspaces.",
    },
    {
        "Term": "Design Tokens",
        "Context and Operational Meaning": "Standardized, centralized data variables for colors, typography scales, spacing margins, and corner radii that enforce visual consistency across presentations programmatically.",
    },
    {
        "Term": "Fully Loaded Hourly Rate",
        "Context and Operational Meaning": "The total real cost of a knowledge worker per hour, including gross salary, payroll taxes, health benefits, software licensing, and operational overhead.",
    },
    {
        "Term": "Layout Bounding Box",
        "Context and Operational Meaning": "The predefined mathematical limits on a slide that restrict text and image containers from spilling over margins or colliding with adjacent graphical components.",
    },
    {
        "Term": "Linter",
        "Context and Operational Meaning": "An automated programmatic scanner that evaluates text and slide layouts against strict design rules to catch overflow defects, awkward line wraps, and hierarchy violations before delivery.",
    },
    {
        "Term": "Manual Formatting Hours",
        "Context and Operational Meaning": "The non strategic time a professional loses manually resizing shapes, fixing table alignments, wrestling text wrapping, and adjusting font sizes on a single presentation.",
    },
    {
        "Term": "Runtime Compatibility",
        "Context and Operational Meaning": "The guarantee that an automated presentation renders with pixel-perfect visual fidelity across both Google Slides and Microsoft PowerPoint without layout drift.",
    },
    {
        "Term": "Slide Slop",
        "Context and Operational Meaning": "Unpolished, generic artificial intelligence presentation output characterized by broken layouts, awkward line wraps, clashing color pills, and inconsistent visual hierarchy.",
    },
    {
        "Term": "Template Ingestion",
        "Context and Operational Meaning": "The operational process of importing master corporate presentation files, extracting style variables, and codifying layout rules into automated generation schemas.",
    },
    {
        "Term": "30, 60, 90 Day Roadmap",
        "Context and Operational Meaning": "A phased enterprise deployment framework divided into thirty days of technical ingestion, sixty days of team activation, and ninety days of organization wide scale.",
    },
    {
        "Term": "Usage Telemetry",
        "Context and Operational Meaning": "Aggregated, privacy compliant operational data that tracks template adoption frequency, slide generation volume, and active user engagement across departments.",
    },
]

df_glossary_master = (
    pd.DataFrame(GLOSSARY_DATA).sort_values(by="Term").reset_index(drop=True)
)

CURRENCY_OPTIONS = [
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
    "₫ VND - Vietnamese Dong",
]

BRAND_TIER_OPTIONS = [
    "Standard (Single Corporate Identity)",
    "Multi Brand (Two to Four Sub Brands and Business Units)",
    "Global Enterprise (Complex Design System and Custom Tokens)",
]


def tooltip_span(term_name, definition_text):
    return (
        f'<span style="text-decoration: underline dotted; cursor: help; '
        f'font-weight: 600;" title="{definition_text}">{term_name}</span>'
    )


def get_deployment_details(brand_tier):
    if "Standard" in brand_tier:
        return {
            "tier": "Tier 1",
            "name": "Standard",
            "status": "Fast direct access",
            "description": "Single identity template system with a focused implementation path.",
            "overview": "Launch a governed pilot quickly with one core template system, a focused creator cohort, and clear ownership.",
            "phase_1": [
                "Provision the core workspace and pilot cohort",
                "Ingest the primary corporate template",
                "Define administrator ownership and guardrails",
            ],
            "phase_2": [
                "Activate priority creators through guided onboarding",
                "Review usage telemetry and template adoption",
                "Publish the first governed production templates",
            ],
            "phase_3": [
                "Validate capacity gains with the executive sponsor",
                "Expand the pilot across adjacent teams",
                "Establish a repeatable operating cadence",
            ],
        }
    if "Multi Brand" in brand_tier:
        return {
            "tier": "Tier 2",
            "name": "Multi-brand",
            "status": "Phased rollout",
            "description": "Multiple business units coordinated through governed templates.",
            "overview": "Coordinate distinct business-unit identities through phased template ingestion, shared governance, and structured rollout waves.",
            "phase_1": [
                "Map business units, templates, and brand owners",
                "Prioritize high-volume presentation workflows",
                "Create governance rules for shared token systems",
            ],
            "phase_2": [
                "Onboard champions by business unit",
                "Monitor adoption by template and user segment",
                "Resolve brand exceptions through a shared review loop",
            ],
            "phase_3": [
                "Scale approved templates to remaining teams",
                "Formalize multi-brand governance reporting",
                "Introduce value reviews by business unit",
            ],
        }
    return {
        "tier": "Tier 3",
        "name": "Enterprise",
        "status": "Custom dedicated",
        "description": "Complex architecture, custom tokens, and advanced governance.",
        "overview": "Establish a dedicated enterprise operating model for complex design systems, strict governance, and distributed global teams.",
        "phase_1": [
            "Complete architecture and security alignment",
            "Codify custom design tokens and approval flows",
            "Establish enterprise workspace and access governance",
        ],
        "phase_2": [
            "Run controlled adoption waves with executive sponsors",
            "Validate token compliance and linter exceptions",
            "Integrate telemetry into operational governance reviews",
        ],
        "phase_3": [
            "Scale governed generation across regions and units",
            "Operationalize enterprise value and risk reporting",
            "Expand the approved component and template ecosystem",
        ],
    }


def create_cumulative_chart(month_numbers, values, curr, chart_type):
    if chart_type == "value":
        line_color = "#3f9dbc"
        fill_color = "rgba(63, 157, 188, 0.18)"
        title = "Cumulative value delivered"
        hover_label = f"{curr}%{{y:,.0f}}"
        y_title = f"Value delivered ({curr})"
    else:
        line_color = "#4b9a88"
        fill_color = "rgba(75, 154, 136, 0.18)"
        title = "Cumulative capacity reclaimed"
        hover_label = "%{y:,.0f} hours"
        y_title = "Hours reclaimed"

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=month_numbers,
            y=values,
            mode="lines+markers",
            name=title,
            line={"color": line_color, "width": 3},
            marker={
                "size": 7,
                "color": "#f7fbfa",
                "line": {"color": line_color, "width": 2},
            },
            fill="tozeroy",
            fillcolor=fill_color,
            hovertemplate=f"<b>Month %{{x}}</b><br>{hover_label}<extra></extra>",
        )
    )

    fig.update_layout(
        height=330,
        margin={"l": 6, "r": 6, "t": 20, "b": 6},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.18)",
        font={
            "family": "Inter, ui-sans-serif, system-ui, sans-serif",
            "color": "#4d6570",
            "size": 12,
        },
        hoverlabel={
            "bgcolor": "#f5f9f8",
            "bordercolor": "rgba(75, 111, 122, 0.22)",
            "font": {"color": "#1f343e"},
        },
        showlegend=False,
        xaxis={
            "title": {"text": ""},
            "tickmode": "array",
            "tickvals": [1, 3, 6, 9, 12],
            "ticktext": ["M1", "M3", "M6", "M9", "M12"],
            "showgrid": False,
            "zeroline": False,
            "fixedrange": True,
            "tickfont": {"color": "#71848c"},
        },
        yaxis={
            "title": {
                "text": y_title,
                "font": {"color": "#71848c", "size": 11},
            },
            "showgrid": True,
            "gridcolor": "rgba(75, 111, 122, 0.12)",
            "zeroline": False,
            "fixedrange": True,
            "tickfont": {"color": "#71848c"},
        },
    )
    return fig


st.markdown(
    """
<style>
    :root {
        --plus-bg: #dce7e7;
        --plus-surface: rgba(247, 250, 249, 0.56);
        --plus-text: #182b34;
        --plus-muted: #5a6f77;
        --plus-faint: #819198;
        --plus-blue: #3f9dbc;
        --plus-violet: #7482bd;
        --plus-teal: #4b9a88;
        --plus-amber: #be9632;
        --plus-red: #c96068;
        --plus-radius: 22px;
    }

    * {
        box-sizing: border-box;
    }

    .stApp {
        background:
            radial-gradient(circle at 9% 2%, rgba(74, 150, 174, 0.25) 0%, rgba(74, 150, 174, 0) 31%),
            radial-gradient(circle at 91% 6%, rgba(120, 133, 185, 0.19) 0%, rgba(120, 133, 185, 0) 28%),
            radial-gradient(circle at 54% 100%, rgba(102, 152, 136, 0.15) 0%, rgba(102, 152, 136, 0) 38%),
            linear-gradient(145deg, #dfeaea 0%, #d4e0e1 47%, #c7d5d7 100%);
        color: var(--plus-text);
        min-height: 100vh;
    }

    .stApp::before {
        content: "";
        position: fixed;
        inset: 0;
        pointer-events: none;
        z-index: 0;
        opacity: 0.20;
        background-image:
            linear-gradient(rgba(70, 103, 114, 0.08) 1px, transparent 1px),
            linear-gradient(90deg, rgba(70, 103, 114, 0.08) 1px, transparent 1px);
        background-size: 48px 48px;
        mask-image: linear-gradient(to bottom, black, transparent 80%);
    }

    [data-testid="stAppViewContainer"] > .main {
        position: relative;
        z-index: 1;
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    [data-testid="stToolbar"] {
        right: 1rem;
    }

    [data-testid="stAppViewContainer"] .main .block-container {
        max-width: 1440px;
        padding: 0.65rem 2.6rem 3.2rem;
    }

    #MainMenu,
    footer,
    [data-testid="stDecoration"] {
        visibility: hidden;
    }

    h1, h2, h3, h4, p, label, div {
        font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont,
            "Segoe UI", sans-serif;
    }

    .plus-shell {
        position: relative;
        overflow: hidden;
        background:
            linear-gradient(135deg, rgba(252, 254, 253, 0.48), rgba(228, 238, 238, 0.52)),
            rgba(240, 246, 245, 0.52);
        border: 1px solid rgba(255, 255, 255, 0.68);
        border-radius: 30px;
        padding: 0.55rem 1.55rem 1.7rem;
        box-shadow:
            0 28px 70px rgba(53, 75, 81, 0.16),
            inset 0 1px 0 rgba(255, 255, 255, 0.84);
        backdrop-filter: blur(24px);
        -webkit-backdrop-filter: blur(24px);
    }

    .plus-shell::before {
        content: "";
        position: absolute;
        width: 520px;
        height: 520px;
        right: -260px;
        top: -350px;
        pointer-events: none;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(104, 181, 205, 0.17) 0%, rgba(104, 181, 205, 0) 68%);
    }

    .plus-shell::after {
        content: "";
        position: absolute;
        width: 380px;
        height: 380px;
        left: -250px;
        bottom: -280px;
        pointer-events: none;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(128, 137, 190, 0.12) 0%, rgba(128, 137, 190, 0) 70%);
    }

    .plus-shell > * {
        position: relative;
        z-index: 1;
    }

    .topbar {
        min-height: 58px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1rem;
        padding: 0.42rem 0.62rem 0.52rem;
        margin-bottom: 1.15rem;
        border: 1px solid rgba(255, 255, 255, 0.58);
        border-radius: 18px;
        background: rgba(250, 253, 252, 0.30);
        box-shadow:
            inset 0 1px 0 rgba(255, 255, 255, 0.62),
            0 8px 20px rgba(67, 88, 95, 0.06);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
    }

    .brand-lockup {
        display: flex;
        align-items: center;
        gap: 0.72rem;
    }

    .brand-mark {
        width: 34px;
        height: 34px;
        display: grid;
        place-items: center;
        overflow: hidden;
        border-radius: 10px;
        background: rgba(255, 255, 255, 0.58);
        border: 1px solid rgba(255, 255, 255, 0.78);
        box-shadow:
            0 6px 15px rgba(73, 131, 153, 0.15),
            inset 0 1px 0 rgba(255, 255, 255, 0.80);
    }

    .brand-mark img {
        width: 24px;
        height: 24px;
        object-fit: contain;
        display: block;
    }

    .brand-copy {
        line-height: 1.08;
        padding-top: 1px;
    }

    .brand-title {
        margin: 0;
        color: #1c3039;
        font-size: 0.98rem;
        font-weight: 780;
        letter-spacing: -0.025em;
    }

    .brand-subtitle {
        margin-top: 0.20rem;
        color: #7a8d94;
        font-size: 0.66rem;
        font-weight: 750;
        letter-spacing: 0.15em;
        text-transform: uppercase;
    }

    .topbar-right {
        display: flex;
        align-items: center;
        gap: 0.65rem;
        flex-wrap: wrap;
        justify-content: flex-end;
    }

    .status-pill,
    .meta-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.38rem;
        border-radius: 999px;
        padding: 0.43rem 0.68rem;
        font-size: 0.70rem;
        font-weight: 720;
        letter-spacing: 0.02em;
        border: 1px solid rgba(60, 127, 110, 0.18);
        color: #2f7163;
        background: rgba(91, 168, 145, 0.13);
    }

    .status-dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background: var(--plus-teal);
        box-shadow: 0 0 0 4px rgba(75, 154, 136, 0.12);
    }

    .meta-pill {
        color: #52666f;
        border-color: rgba(69, 104, 115, 0.15);
        background: rgba(255, 255, 255, 0.35);
    }

    .hero-card {
        min-height: 100%;
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.72);
        border-radius: var(--plus-radius);
        padding: 1.7rem 1.75rem;
        background:
            linear-gradient(145deg, rgba(236, 248, 250, 0.65), rgba(224, 229, 247, 0.62)),
            rgba(244, 248, 248, 0.64);
        box-shadow:
            inset 0 1px 0 rgba(255, 255, 255, 0.85),
            0 17px 35px rgba(64, 85, 94, 0.10);
    }

    .hero-card::after {
        content: "";
        position: absolute;
        height: 250px;
        width: 250px;
        border-radius: 50%;
        right: -110px;
        top: -115px;
        background: radial-gradient(circle, rgba(116, 198, 226, 0.24), rgba(116, 198, 226, 0) 69%);
    }

    .eyebrow,
    .metric-label,
    .timeline-label {
        color: #5d7984;
        font-size: 0.67rem;
        font-weight: 800;
        letter-spacing: 0.15em;
        text-transform: uppercase;
    }

    .eyebrow {
        color: #467f95;
        margin-bottom: 0.82rem;
    }

    .hero-heading {
        position: relative;
        z-index: 1;
        margin: 0;
        max-width: 620px;
        color: #182b34;
        font-size: clamp(2rem, 3.4vw, 3.45rem);
        line-height: 1.04;
        letter-spacing: -0.055em;
        font-weight: 760;
    }

    .hero-description {
        position: relative;
        z-index: 1;
        max-width: 680px;
        margin: 0.94rem 0 1.12rem;
        color: #50656e;
        font-size: 0.98rem;
        line-height: 1.65;
    }

    .hero-tags {
        position: relative;
        z-index: 1;
        display: flex;
        gap: 0.5rem;
        flex-wrap: wrap;
    }

    .tag,
    .telemetry-chip {
        padding: 0.39rem 0.62rem;
        color: #46606b;
        background: rgba(255, 255, 255, 0.43);
        border: 1px solid rgba(65, 105, 116, 0.13);
        border-radius: 999px;
        font-size: 0.70rem;
        font-weight: 650;
    }

    .value-card {
        height: 100%;
        min-height: 255px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        overflow: hidden;
        position: relative;
        border-radius: var(--plus-radius);
        padding: 1.6rem;
        background:
            linear-gradient(148deg, rgba(226, 232, 249, 0.84), rgba(214, 236, 241, 0.83)),
            rgba(241, 247, 248, 0.78);
        border: 1px solid rgba(255, 255, 255, 0.78);
        box-shadow:
            inset 0 1px 0 rgba(255, 255, 255, 0.88),
            0 17px 35px rgba(58, 82, 94, 0.12);
    }

    .value-card::before {
        content: "";
        position: absolute;
        width: 270px;
        height: 270px;
        border-radius: 50%;
        right: -110px;
        bottom: -160px;
        background: radial-gradient(circle, rgba(101, 188, 212, 0.25), rgba(101, 188, 212, 0) 68%);
    }

    .value-card > * {
        position: relative;
        z-index: 1;
    }

    .value-title {
        color: #5a6f8d;
        font-size: 0.68rem;
        font-weight: 800;
        letter-spacing: 0.14em;
        text-transform: uppercase;
    }

    .value-number {
        margin-top: 0.8rem;
        color: #1e3340;
        font-size: clamp(2.25rem, 4.1vw, 4rem);
        font-weight: 790;
        line-height: 0.98;
        letter-spacing: -0.065em;
        overflow-wrap: anywhere;
    }

    .value-copy {
        margin-top: 0.7rem;
        color: #526974;
        font-size: 0.84rem;
        line-height: 1.45;
    }

    .value-footer {
        display: flex;
        align-items: center;
        gap: 0.46rem;
        margin-top: 1.25rem;
        color: #327968;
        font-size: 0.73rem;
        font-weight: 700;
    }

    .value-footer .arrow {
        display: grid;
        width: 22px;
        height: 22px;
        place-items: center;
        border-radius: 50%;
        background: rgba(75, 154, 136, 0.13);
        color: #338570;
    }

    .section-heading {
        display: flex;
        align-items: flex-end;
        justify-content: space-between;
        gap: 1rem;
        margin: 1.45rem 0 0.78rem;
    }

    .section-heading h2 {
        margin: 0;
        color: var(--plus-text);
        font-size: 1.14rem;
        letter-spacing: -0.025em;
        font-weight: 720;
    }

    .section-heading p {
        margin: 0.22rem 0 0;
        color: var(--plus-muted);
        font-size: 0.80rem;
        line-height: 1.45;
    }

    .section-kicker {
        flex: none;
        padding: 0.38rem 0.62rem;
        color: #55727d;
        background: rgba(255, 255, 255, 0.42);
        border: 1px solid rgba(69, 111, 123, 0.13);
        border-radius: 999px;
        font-size: 0.67rem;
        font-weight: 720;
    }

    .glass-panel,
    .analytics-card,
    .phase-card,
    .knowledge-card,
    .linter-summary {
        height: 100%;
        border: 1px solid rgba(255, 255, 255, 0.69);
        border-radius: var(--plus-radius);
        padding: 1.1rem;
        background:
            linear-gradient(145deg, rgba(250, 253, 252, 0.54), rgba(228, 237, 238, 0.46)),
            var(--plus-surface);
        box-shadow:
            inset 0 1px 0 rgba(255, 255, 255, 0.88),
            0 11px 25px rgba(66, 86, 93, 0.08);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
    }

    .input-group-title {
        display: flex;
        align-items: center;
        gap: 0.55rem;
        margin-bottom: 0.85rem;
        color: #263c46;
        font-size: 0.88rem;
        font-weight: 730;
        letter-spacing: -0.01em;
    }

    .group-dot {
        width: 9px;
        height: 9px;
        border-radius: 50%;
        background: var(--plus-blue);
        box-shadow: 0 0 0 4px rgba(63, 157, 188, 0.12);
    }

    .group-dot.teal {
        background: var(--plus-teal);
        box-shadow: 0 0 0 4px rgba(75, 154, 136, 0.12);
    }

    .group-dot.violet {
        background: var(--plus-violet);
        box-shadow: 0 0 0 4px rgba(116, 130, 189, 0.12);
    }

    .input-group-copy {
        min-height: 35px;
        margin: -0.35rem 0 0.95rem;
        color: #607680;
        font-size: 0.74rem;
        line-height: 1.42;
    }

    div[data-testid="stSelectbox"] > label,
    div[data-testid="stNumberInput"] > label,
    div[data-testid="stTextInput"] > label,
    div[data-testid="stTextArea"] > label,
    div[data-testid="stRadio"] > label {
        color: #425a64 !important;
        font-size: 0.72rem !important;
        font-weight: 650 !important;
        line-height: 1.25 !important;
        margin-bottom: 0.35rem !important;
    }

    div[data-testid="stNumberInput"] input,
    div[data-testid="stTextInput"] input,
    div[data-baseweb="select"] > div,
    div[data-testid="stTextArea"] textarea {
        color: #213640 !important;
        background: rgba(255, 255, 255, 0.54) !important;
        border-color: rgba(75, 111, 122, 0.18) !important;
        border-radius: 11px !important;
        box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.60) !important;
    }

    div[data-testid="stNumberInput"] input,
    div[data-testid="stTextInput"] input {
        min-height: 2.58rem !important;
        font-size: 0.86rem !important;
    }

    div[data-baseweb="select"] > div {
        min-height: 2.58rem !important;
        font-size: 0.84rem !important;
    }

    div[data-baseweb="select"] * {
        color: #213640 !important;
    }

    div[data-testid="stNumberInput"] button {
        color: #54727d !important;
        background: rgba(255, 255, 255, 0.48) !important;
        border-color: rgba(75, 111, 122, 0.13) !important;
    }

    div[data-testid="stNumberInput"] input:focus,
    div[data-testid="stTextInput"] input:focus,
    div[data-testid="stTextArea"] textarea:focus,
    div[data-baseweb="select"] > div:focus-within {
        border-color: rgba(63, 157, 188, 0.72) !important;
        box-shadow: 0 0 0 3px rgba(63, 157, 188, 0.13) !important;
    }

    div[data-baseweb="popover"],
    div[data-baseweb="menu"] {
        background: #f5f9f8 !important;
    }

    div[data-baseweb="menu"] li {
        color: #233943 !important;
    }

    div[data-baseweb="menu"] li:hover {
        background: rgba(63, 157, 188, 0.12) !important;
    }

    .metric-card {
        height: 100%;
        min-height: 166px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        padding: 1.18rem;
        border: 1px solid rgba(255, 255, 255, 0.68);
        border-radius: 18px;
        background:
            linear-gradient(145deg, rgba(250, 253, 252, 0.57), rgba(225, 235, 236, 0.48)),
            var(--plus-surface);
        box-shadow:
            inset 0 1px 0 rgba(255, 255, 255, 0.88),
            0 11px 25px rgba(66, 86, 93, 0.08);
    }

    .metric-card.teal-card {
        border-color: rgba(75, 154, 136, 0.25);
    }

    .metric-card.blue-card {
        border-color: rgba(63, 157, 188, 0.24);
    }

    .metric-card.violet-card {
        border-color: rgba(116, 130, 189, 0.25);
    }

    .metric-value {
        margin-top: 0.54rem;
        color: #1d333d;
        font-size: clamp(1.55rem, 2.4vw, 2.15rem);
        font-weight: 760;
        letter-spacing: -0.048em;
        line-height: 1.05;
        overflow-wrap: anywhere;
    }

    .metric-value.tier-value {
        font-size: clamp(1.25rem, 1.95vw, 1.7rem);
    }

    .metric-helper {
        margin-top: 0.55rem;
        color: #60737c;
        font-size: 0.73rem;
        line-height: 1.43;
    }

    .metric-status,
    .phase-status {
        display: inline-flex;
        align-items: center;
        width: fit-content;
        gap: 0.35rem;
        margin-top: 0.95rem;
        padding: 0.35rem 0.54rem;
        border-radius: 999px;
        font-size: 0.68rem;
        font-weight: 720;
        background: rgba(75, 154, 136, 0.12);
        color: #347663;
    }

    .metric-status.blue {
        background: rgba(63, 157, 188, 0.12);
        color: #297794;
    }

    .metric-status.violet {
        background: rgba(116, 130, 189, 0.13);
        color: #5969a7;
    }

    .impact-narrative,
    .deployment-summary {
        margin-top: 1rem;
        padding: 1rem 1.05rem;
        border: 1px solid rgba(79, 112, 122, 0.13);
        border-radius: 16px;
        color: #536a73;
        background: rgba(255, 255, 255, 0.38);
        font-size: 0.85rem;
        line-height: 1.6;
    }

    .impact-narrative strong,
    .deployment-summary strong {
        color: #1f343e;
        font-weight: 700;
    }

    .impact-narrative .narrative-highlight {
        color: #2d7666;
        font-weight: 720;
    }

    div[data-testid="stTabs"] {
        margin-top: 1.85rem;
    }

    div[data-testid="stTabs"] [data-baseweb="tab-list"] {
        gap: 0.35rem;
        border-bottom: 1px solid rgba(74, 107, 117, 0.17);
        overflow-x: auto;
    }

    div[data-testid="stTabs"] [data-baseweb="tab"] {
        height: auto;
        padding: 0.68rem 0.78rem 0.74rem;
        color: #617781;
        font-size: 0.75rem;
        font-weight: 680;
        white-space: nowrap;
    }

    div[data-testid="stTabs"] [aria-selected="true"] {
        color: #1f414e !important;
    }

    div[data-testid="stTabs"] [data-baseweb="tab-highlight"] {
        height: 2px;
        background: linear-gradient(90deg, var(--plus-blue), var(--plus-violet)) !important;
    }

    .tab-section-title {
        margin: 1.45rem 0 0.28rem;
        color: #203640;
        font-size: 1.22rem;
        font-weight: 730;
        letter-spacing: -0.025em;
    }

    .tab-section-copy {
        margin: 0 0 1.1rem;
        color: #5b717a;
        font-size: 0.84rem;
    }

    .milestone-card {
        height: 100%;
        padding: 0.95rem 1rem;
        border: 1px solid rgba(255, 255, 255, 0.68);
        border-radius: 16px;
        background: rgba(255, 255, 255, 0.37);
        box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.77);
    }

    .milestone-label {
        color: #71848c;
        font-size: 0.64rem;
        font-weight: 800;
        letter-spacing: 0.13em;
        text-transform: uppercase;
    }

    .milestone-value {
        margin-top: 0.38rem;
        color: #203842;
        font-size: 1.45rem;
        font-weight: 760;
        letter-spacing: -0.04em;
    }

    .milestone-copy {
        margin-top: 0.30rem;
        color: #657981;
        font-size: 0.70rem;
        line-height: 1.35;
    }

    .analytics-card {
        padding: 1.15rem 1.15rem 0.75rem;
        margin-top: 0.85rem;
    }

    .analytics-card h3,
    .knowledge-card h3 {
        margin: 0;
        color: #243a44;
        font-size: 0.95rem;
        font-weight: 730;
        letter-spacing: -0.015em;
    }

    .analytics-card p,
    .knowledge-card p {
        margin: 0.30rem 0 0;
        color: #647780;
        font-size: 0.76rem;
        line-height: 1.45;
    }

    .phase-track {
        display: flex;
        align-items: center;
        gap: 0.55rem;
        margin: 1.05rem 0 0.9rem;
    }

    .phase-track-step {
        display: flex;
        align-items: center;
        gap: 0.48rem;
        color: #56727c;
        font-size: 0.70rem;
        font-weight: 720;
        white-space: nowrap;
    }

    .phase-track-dot {
        display: grid;
        width: 23px;
        height: 23px;
        place-items: center;
        border-radius: 50%;
        color: #ffffff;
        background: linear-gradient(135deg, #51aac7, #7883c5);
        box-shadow: 0 5px 12px rgba(79, 137, 157, 0.18);
        font-size: 0.66rem;
        font-weight: 800;
    }

    .phase-track-line {
        height: 1px;
        flex: 1;
        background: linear-gradient(90deg, rgba(63, 157, 188, 0.52), rgba(116, 130, 189, 0.35));
    }

    .phase-card {
        position: relative;
        overflow: hidden;
        min-height: 260px;
        padding: 1.15rem;
    }

    .phase-card::after {
        content: "";
        position: absolute;
        width: 150px;
        height: 150px;
        right: -80px;
        top: -88px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(104, 181, 205, 0.18), rgba(104, 181, 205, 0) 70%);
    }

    .phase-card > * {
        position: relative;
        z-index: 1;
    }

    .phase-number {
        color: #527989;
        font-size: 0.67rem;
        font-weight: 800;
        letter-spacing: 0.14em;
        text-transform: uppercase;
    }

    .phase-card h3 {
        margin: 0.45rem 0 0;
        color: #203741;
        font-size: 1.12rem;
        font-weight: 750;
        letter-spacing: -0.025em;
    }

    .phase-card p {
        min-height: 38px;
        margin: 0.48rem 0 0.72rem;
        color: #60737c;
        font-size: 0.75rem;
        line-height: 1.45;
    }

    .phase-list {
        display: grid;
        gap: 0.48rem;
        padding: 0;
        margin: 0;
        list-style: none;
    }

    .phase-list li {
        position: relative;
        padding-left: 1.08rem;
        color: #465e68;
        font-size: 0.73rem;
        line-height: 1.40;
    }

    .phase-list li::before {
        content: "✓";
        position: absolute;
        left: 0;
        color: #3d937f;
        font-weight: 800;
    }

    .phase-status {
        margin-top: 0.85rem;
    }

    .linter-summary {
        padding: 1rem 1.1rem;
        margin-bottom: 0.95rem;
    }

    .linter-summary-grid {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1rem;
        flex-wrap: wrap;
    }

    .telemetry-row {
        display: flex;
        gap: 0.48rem;
        flex-wrap: wrap;
    }

    .telemetry-chip {
        color: #48636d;
        background: rgba(255, 255, 255, 0.46);
    }

    .telemetry-chip strong {
        color: #203943;
    }

    .slide-card-title {
        margin: 0 0 0.25rem;
        color: #203741;
        font-size: 1rem;
        font-weight: 730;
        letter-spacing: -0.02em;
    }

    .slide-card-caption {
        margin-bottom: 0.70rem;
        color: #6a7d85;
        font-size: 0.74rem;
    }

    .slide-canvas-broken {
        background:
            linear-gradient(145deg, rgba(255, 246, 246, 0.74), rgba(247, 226, 228, 0.67)),
            rgba(255, 255, 255, 0.42);
        border: 1px dashed rgba(190, 76, 87, 0.72);
        border-radius: 18px;
        padding: 20px;
        min-height: 235px;
        position: relative;
        overflow: hidden;
        box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.75);
    }

    .slide-canvas-clean {
        background:
            linear-gradient(145deg, rgba(236, 249, 250, 0.80), rgba(227, 239, 250, 0.72)),
            rgba(255, 255, 255, 0.48);
        border: 1px solid rgba(63, 157, 188, 0.60);
        border-radius: 18px;
        padding: 20px;
        min-height: 235px;
        box-shadow:
            inset 0 1px 0 rgba(255, 255, 255, 0.82),
            0 9px 20px rgba(58, 107, 124, 0.08);
    }

    .knowledge-card {
        padding: 1.05rem 1.1rem;
        margin-bottom: 0.9rem;
    }

    .knowledge-stat {
        margin-top: 0.48rem;
        color: #1f3a44;
        font-size: 1.55rem;
        font-weight: 760;
        letter-spacing: -0.04em;
    }

    div[data-testid="stDataFrame"] {
        border: 1px solid rgba(78, 111, 121, 0.15);
        border-radius: 14px;
        overflow: hidden;
        background: rgba(255, 255, 255, 0.38);
    }

    div[data-testid="stDataFrame"] [role="grid"] {
        background: rgba(255, 255, 255, 0.47) !important;
    }

    .custom-footer {
        margin-top: 2.4rem;
        padding-top: 1.35rem;
        border-top: 1px solid rgba(74, 107, 117, 0.16);
        color: #71868e;
        text-align: center;
        font-size: 0.72rem;
    }

    @media (max-width: 900px) {
        [data-testid="stAppViewContainer"] .main .block-container {
            padding: 0.6rem 1rem 2.5rem;
        }

        .plus-shell {
            padding: 0.5rem 1rem 1.2rem;
            border-radius: 22px;
        }

        .topbar {
            align-items: flex-start;
            flex-direction: column;
        }

        .topbar-right {
            justify-content: flex-start;
        }

        .hero-card,
        .value-card {
            min-height: auto;
        }

        .phase-track-line {
            display: none;
        }

        .phase-track {
            flex-wrap: wrap;
        }
    }

    @media (max-width: 640px) {
        .hero-heading {
            font-size: 2rem;
        }

        .hero-description {
            font-size: 0.89rem;
        }

        .value-number {
            font-size: 2.45rem;
        }

        div[data-testid="stTabs"] [data-baseweb="tab"] {
            font-size: 0.67rem;
            padding-left: 0.46rem;
            padding-right: 0.46rem;
        }

        .section-heading {
            align-items: flex-start;
            flex-direction: column;
        }

        .phase-track {
            align-items: flex-start;
            flex-direction: column;
        }
    }
</style>
""",
    unsafe_allow_html=True,
)

st.markdown('<div class="plus-shell">', unsafe_allow_html=True)

st.markdown(
    """
<div class="topbar">
    <div class="brand-lockup">
        <div class="brand-mark">
            <img src="https://plusai.com/favicon.svg" alt="Plus AI" />
        </div>
        <div class="brand-copy">
            <div class="brand-title">Plus AI</div>
            <div class="brand-subtitle">Enterprise Decision Intelligence</div>
        </div>
    </div>
    <div class="topbar-right">
        <div class="meta-pill">ROI modeling workspace</div>
        <div class="status-pill"><span class="status-dot"></span>Scenario ready</div>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

hero_placeholder = st.empty()

st.markdown(
    """
<div class="section-heading">
    <div>
        <h2>Scenario configuration</h2>
        <p>Define the operating assumptions that shape the enterprise value model.</p>
    </div>
    <div class="section-kicker">Live calculation</div>
</div>
""",
    unsafe_allow_html=True,
)

config_col_1, config_col_2, config_col_3 = st.columns([1, 1, 1.08], gap="medium")

with config_col_1:
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.markdown(
        """
<div class="input-group-title"><span class="group-dot"></span>Organization profile</div>
<div class="input-group-copy">Size the presentation-producing workforce and its monthly output.</div>
""",
        unsafe_allow_html=True,
    )
    final_team_size = st.number_input(
        "Active slide creators",
        min_value=1,
        max_value=10000,
        value=50,
        step=1,
        help="Total knowledge workers, consultants, or sales reps actively creating or modifying presentations.",
    )
    final_decks_per_month = st.number_input(
        "Average decks per user / month",
        min_value=0.5,
        max_value=100.0,
        value=6.0,
        step=0.5,
        format="%.1f",
        help="Estimated volume of presentations created, edited, or updated per employee every month.",
    )
    st.markdown("</div>", unsafe_allow_html=True)

with config_col_2:
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.markdown(
        """
<div class="input-group-title"><span class="group-dot teal"></span>Economic assumptions</div>
<div class="input-group-copy">Translate reduced formatting work into productivity capacity and annual value.</div>
""",
        unsafe_allow_html=True,
    )
    selected_currency_full = st.selectbox(
        "Currency",
        options=CURRENCY_OPTIONS,
        index=0,
        help="Select the operational currency to standardize financial return modeling across global teams.",
    )
    curr = selected_currency_full.split(" ")[0]
    hourly_rate = st.number_input(
        f"Average worker hourly rate ({curr})",
        min_value=1.00,
        max_value=2500.00,
        value=45.00,
        step=0.25,
        format="%.2f",
        help="Fully loaded hourly cost including salary and overhead of professionals creating presentations.",
    )
    st.markdown("</div>", unsafe_allow_html=True)

with config_col_3:
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.markdown(
        """
<div class="input-group-title"><span class="group-dot violet"></span>Deployment architecture</div>
<div class="input-group-copy">Match rollout scope to the complexity of brand, templates, and governance.</div>
""",
        unsafe_allow_html=True,
    )
    final_hours_per_deck = st.number_input(
        "Manual formatting hours per deck",
        min_value=0.1,
        max_value=40.0,
        value=3.5,
        step=0.25,
        format="%.2f",
        help="Average time a professional spends aligning shapes, fixing margins, and manually styling slides.",
    )
    brand_tier = st.selectbox(
        "Brand and template architecture tier",
        options=BRAND_TIER_OPTIONS,
        help="Defines organizational design complexity from single template schemas to multi-unit corporate brands.",
    )
    st.markdown("</div>", unsafe_allow_html=True)

total_monthly_decks = final_team_size * final_decks_per_month
hours_saved_per_deck = final_hours_per_deck * 0.65
monthly_hours_saved = total_monthly_decks * hours_saved_per_deck
annual_hours_saved = monthly_hours_saved * 12
annual_cost_savings = annual_hours_saved * hourly_rate
deployment = get_deployment_details(brand_tier)

month_numbers = list(range(1, 13))
months = [f"Month {month}" for month in month_numbers]
cumulative_hours = [monthly_hours_saved * month for month in month_numbers]
cumulative_savings = [monthly_hours_saved * hourly_rate * month for month in month_numbers]

with hero_placeholder.container():
    hero_left, hero_right = st.columns([1.42, 0.78], gap="large")

    with hero_left:
        st.markdown(
            """
<div class="hero-card">
    <div class="eyebrow">PLUS AI / ENTERPRISE STRATEGY CONSOLE</div>
    <h1 class="hero-heading">Turn presentation work into measurable enterprise capacity.</h1>
    <p class="hero-description">
        Model the time, operational throughput, and financial value unlocked when
        teams replace manual slide formatting with governed AI workflows.
    </p>
    <div class="hero-tags">
        <span class="tag">ROI scenario modeling</span>
        <span class="tag">Deployment planning</span>
        <span class="tag">Brand governance</span>
    </div>
</div>
""",
            unsafe_allow_html=True,
        )

    with hero_right:
        st.markdown(
            f"""
<div class="value-card">
    <div>
        <div class="value-title">Annual value delivered</div>
        <div class="value-number">{curr}{annual_cost_savings:,.0f}</div>
        <div class="value-copy">Estimated productivity capacity unlocked from the current scenario.</div>
    </div>
    <div class="value-footer"><span class="arrow">↗</span><span>Calculated from live operating assumptions</span></div>
</div>
""",
            unsafe_allow_html=True,
        )

st.markdown(
    """
<div class="section-heading">
    <div>
        <h2>Executive performance impact</h2>
        <p>The immediate capacity, financial, and deployment implications of this scenario.</p>
    </div>
    <div class="section-kicker">12-month outlook</div>
</div>
""",
    unsafe_allow_html=True,
)

metric_col_1, metric_col_2, metric_col_3 = st.columns([1, 1, 1], gap="medium")

with metric_col_1:
    st.markdown(
        f"""
<div class="metric-card teal-card">
    <div>
        <div class="metric-label">Annual hours reclaimed</div>
        <div class="metric-value">{annual_hours_saved:,.1f}<span style="font-size:0.46em; color:#668b82; font-weight:650;"> hrs</span></div>
        <div class="metric-helper">Formatting capacity returned to the organization over twelve months.</div>
    </div>
    <div class="metric-status">✦ 65% modeled efficiency gain</div>
</div>
""",
        unsafe_allow_html=True,
    )

with metric_col_2:
    st.markdown(
        f"""
<div class="metric-card blue-card">
    <div>
        <div class="metric-label">Monthly deck velocity</div>
        <div class="metric-value">{total_monthly_decks:,.0f}<span style="font-size:0.46em; color:#678b98; font-weight:650;"> decks</span></div>
        <div class="metric-helper">Presentation output created across {final_team_size:,} active slide creators each month.</div>
    </div>
    <div class="metric-status blue">↗ {final_decks_per_month:,.1f} decks per creator</div>
</div>
""",
        unsafe_allow_html=True,
    )

with metric_col_3:
    st.markdown(
        f"""
<div class="metric-card violet-card">
    <div>
        <div class="metric-label">Deployment readiness</div>
        <div class="metric-value tier-value">{deployment["tier"]}: {deployment["name"]}</div>
        <div class="metric-helper">{deployment["description"]}</div>
    </div>
    <div class="metric-status violet">◉ {deployment["status"]}</div>
</div>
""",
        unsafe_allow_html=True,
    )

st.markdown(
    f"""
<div class="impact-narrative">
    At the current configuration, Plus AI can reclaim approximately
    <strong>{annual_hours_saved:,.0f} hours</strong> of annual presentation-production capacity across
    <strong>{final_team_size:,} active creators</strong>, representing an estimated
    <span class="narrative-highlight">{curr}{annual_cost_savings:,.0f} in annual productivity value</span>.
</div>
""",
    unsafe_allow_html=True,
)

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "ROI & capacity model",
        "30 / 60 / 90 deployment",
        "Slide slop linter",
        "Glossary",
    ]
)

with tab1:
    st.markdown(
        '<div class="tab-section-title">Financial and capacity impact analysis</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="tab-section-copy">Track how reclaimed presentation capacity becomes measurable enterprise value over the first twelve months.</div>',
        unsafe_allow_html=True,
    )

    milestone_1, milestone_2, milestone_3 = st.columns(3, gap="medium")

    with milestone_1:
        st.markdown(
            f"""
<div class="milestone-card">
    <div class="milestone-label">Month 1 value</div>
    <div class="milestone-value">{curr}{cumulative_savings[0]:,.0f}</div>
    <div class="milestone-copy">{cumulative_hours[0]:,.0f} hours of reclaimed capacity.</div>
</div>
""",
            unsafe_allow_html=True,
        )

    with milestone_2:
        st.markdown(
            f"""
<div class="milestone-card">
    <div class="milestone-label">Month 6 value</div>
    <div class="milestone-value">{curr}{cumulative_savings[5]:,.0f}</div>
    <div class="milestone-copy">{cumulative_hours[5]:,.0f} cumulative hours reclaimed.</div>
</div>
""",
            unsafe_allow_html=True,
        )

    with milestone_3:
        st.markdown(
            f"""
<div class="milestone-card">
    <div class="milestone-label">Month 12 value</div>
    <div class="milestone-value">{curr}{cumulative_savings[11]:,.0f}</div>
    <div class="milestone-copy">{cumulative_hours[11]:,.0f} hours returned to the organization.</div>
</div>
""",
            unsafe_allow_html=True,
        )

    roi_view = st.radio(
        "ROI analysis view",
        options=["Financial value", "Capacity reclaimed", "Detailed monthly table"],
        horizontal=True,
        label_visibility="collapsed",
    )

    if roi_view == "Financial value":
        st.markdown(
            """
<div class="analytics-card">
    <h3>Value ramp</h3>
    <p>Cumulative estimated productivity value from the modeled reduction in manual deck formatting.</p>
</div>
""",
            unsafe_allow_html=True,
        )
        st.plotly_chart(
            create_cumulative_chart(month_numbers, cumulative_savings, curr, "value"),
            use_container_width=True,
            config={"displayModeBar": False, "responsive": True},
        )

    elif roi_view == "Capacity reclaimed":
        st.markdown(
            """
<div class="analytics-card">
    <h3>Capacity ramp</h3>
    <p>Cumulative hours returned to creators for higher-value work, collaboration, and customer-facing preparation.</p>
</div>
""",
            unsafe_allow_html=True,
        )
        st.plotly_chart(
            create_cumulative_chart(month_numbers, cumulative_hours, curr, "hours"),
            use_container_width=True,
            config={"displayModeBar": False, "responsive": True},
        )

    else:
        st.markdown(
            """
<div class="analytics-card">
    <h3>Detailed monthly model</h3>
    <p>Review the month-by-month cumulative capacity and value model behind the executive outcomes.</p>
</div>
""",
            unsafe_allow_html=True,
        )
        df_roi = pd.DataFrame(
            {
                "Timeline": months,
                "Cumulative Hours Saved": [f"{hours:,.1f}" for hours in cumulative_hours],
                f"Cumulative Value ({curr})": [
                    f"{curr}{value:,.2f}" for value in cumulative_savings
                ],
            }
        )
        st.dataframe(df_roi, use_container_width=True, hide_index=True)

with tab2:
    st.markdown(
        f'<div class="tab-section-title">{deployment["tier"]} deployment journey: {deployment["name"]}</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="tab-section-copy">A practical operating sequence that adapts to the chosen brand and template architecture.</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
<div class="deployment-summary">
    <strong>{deployment["tier"]} / {deployment["name"]}</strong> — {deployment["overview"]}
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
<div class="phase-track">
    <div class="phase-track-step"><span class="phase-track-dot">1</span>Days 1–30</div>
    <div class="phase-track-line"></div>
    <div class="phase-track-step"><span class="phase-track-dot">2</span>Days 31–60</div>
    <div class="phase-track-line"></div>
    <div class="phase-track-step"><span class="phase-track-dot">3</span>Days 61–90</div>
</div>
""",
        unsafe_allow_html=True,
    )

    phase_1, phase_2, phase_3 = st.columns(3, gap="medium")

    with phase_1:
        phase_1_items = "".join(f"<li>{item}</li>" for item in deployment["phase_1"])
        st.markdown(
            f"""
<div class="phase-card">
    <div class="phase-number">Phase 01 / Foundation</div>
    <h3>Ingestion</h3>
    <p>Establish the operating environment, template foundation, and accountable launch scope.</p>
    <ul class="phase-list">{phase_1_items}</ul>
    <div class="phase-status">● Foundation established</div>
</div>
""",
            unsafe_allow_html=True,
        )

    with phase_2:
        phase_2_items = "".join(f"<li>{item}</li>" for item in deployment["phase_2"])
        st.markdown(
            f"""
<div class="phase-card">
    <div class="phase-number">Phase 02 / Adoption</div>
    <h3>Activation</h3>
    <p>Turn the approved system into a repeatable creator workflow with observable adoption.</p>
    <ul class="phase-list">{phase_2_items}</ul>
    <div class="phase-status">● Adoption in motion</div>
</div>
""",
            unsafe_allow_html=True,
        )

    with phase_3:
        phase_3_items = "".join(f"<li>{item}</li>" for item in deployment["phase_3"])
        st.markdown(
            f"""
<div class="phase-card">
    <div class="phase-number">Phase 03 / Expansion</div>
    <h3>Scale</h3>
    <p>Convert early gains into durable governance, expanded reach, and executive value reporting.</p>
    <ul class="phase-list">{phase_3_items}</ul>
    <div class="phase-status">● Enterprise ready</div>
</div>
""",
            unsafe_allow_html=True,
        )

with tab3:
    st.markdown(
        '<div class="tab-section-title">Interactive slide slop linter</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="tab-section-copy">Compare unstructured output with a governed Plus AI layout engine that protects hierarchy, margins, and readability.</div>',
        unsafe_allow_html=True,
    )

    linter_expl = "An automated programmatic scanner that evaluates text and slide layouts against strict design rules to catch overflow defects before delivery."
    tokens_expl = "Standardized variables for colors, typography scales, and margins that enforce visual consistency across presentations."
    runtime_expl = "The guarantee that an automated presentation renders with pixel-perfect visual fidelity across both Google Slides and Microsoft PowerPoint."

    st.markdown(
        f"See how an automated {tooltip_span('Linter', linter_expl)} enforcing strict "
        f"{tooltip_span('Design Tokens', tokens_expl)} prevents layout overflow and guarantees "
        f"{tooltip_span('Runtime Compatibility', runtime_expl)} across Google Slides and Microsoft PowerPoint:",
        unsafe_allow_html=True,
    )

    sample_text = st.text_area(
        "Presentation text to evaluate",
        value="Accelerating Enterprise Revenue Velocity Across Global Distributed Teams and Unifying Cross Functional Execution",
        help="Edit or add long text to see how the layout engine dynamically enforces slide margins and font hierarchy.",
        height=112,
    )

    char_count = len(sample_text)
    word_count = len(sample_text.split())

    if char_count > 100:
        dynamic_font_size = "18px"
        dynamic_badge = "Auto scaled to subhead schema (Tier 3)"
        governance_status = "Complex copy safely adapted"
    elif char_count > 50:
        dynamic_font_size = "22px"
        dynamic_badge = "Auto balanced 2-line hierarchy (Tier 2)"
        governance_status = "Two-line hierarchy protected"
    else:
        dynamic_font_size = "26px"
        dynamic_badge = "Standard headline schema (Tier 1)"
        governance_status = "Headline schema protected"

    overflow_warning = (
        "High layout risk: text exceeds the safe 60-character container threshold."
        if char_count > 60
        else "Moderate layout risk: static output has no responsive padding or hierarchy rules."
    )

    st.markdown(
        f"""
<div class="linter-summary">
    <div class="linter-summary-grid">
        <div>
            <div class="metric-label">Live layout telemetry</div>
            <div style="margin-top:0.35rem; color:#4f6771; font-size:0.80rem;">The linter evaluates hierarchy and bounding-box fit as copy changes.</div>
        </div>
        <div class="telemetry-row">
            <span class="telemetry-chip"><strong>{char_count}</strong> characters</span>
            <span class="telemetry-chip"><strong>{word_count}</strong> words</span>
            <span class="telemetry-chip"><strong>{governance_status}</strong></span>
        </div>
    </div>
</div>
""",
        unsafe_allow_html=True,
    )

    col_linter_1, col_linter_2 = st.columns(2, gap="large")

    with col_linter_1:
        st.markdown('<div class="slide-card-title">Unstructured generation</div>', unsafe_allow_html=True)
        st.markdown('<div class="slide-card-caption">Common AI slide slop anti-pattern: static layout, uncontrolled copy, and no design governance.</div>', unsafe_allow_html=True)
        st.markdown(
            f"""
<div class="slide-canvas-broken">
    <div style="font-size:11px; color:#bd4c57; font-weight:800; text-transform:uppercase; margin-bottom:10px; letter-spacing:0.08em;">
        Layout risk detected
    </div>
    <div style="font-family:Georgia, serif; font-style:italic; font-size:24px; color:#b54e59; line-height:1.10; margin-bottom:14px;">
        {sample_text}
    </div>
    <div style="position:absolute; bottom:14px; right:14px; background:rgba(201,96,104,0.16); color:#9d3d48; padding:5px 9px; border-radius:6px; font-size:11px; font-weight:700;">
        Bounding box broken
    </div>
</div>
""",
            unsafe_allow_html=True,
        )
        st.error(overflow_warning)

    with col_linter_2:
        st.markdown('<div class="slide-card-title">Plus governed layout engine</div>', unsafe_allow_html=True)
        st.markdown('<div class="slide-card-caption">Structured design tokens, responsive hierarchy, and safe-margin enforcement before delivery.</div>', unsafe_allow_html=True)
        st.markdown(
            f"""
<div class="slide-canvas-clean">
    <div style="font-size:11px; color:#327e9a; font-weight:800; text-transform:uppercase; margin-bottom:10px; letter-spacing:0.08em;">
        Plus AI design system
    </div>
    <div style="font-family:Inter, sans-serif; font-weight:740; font-size:{dynamic_font_size}; color:#203640; line-height:1.3; margin-bottom:14px;">
        {sample_text}
    </div>
    <div style="display:inline-block; background:rgba(63,157,188,0.13); color:#286d88; padding:5px 9px; border-radius:6px; font-size:11px; font-weight:700;">
        {dynamic_badge}
    </div>
</div>
""",
            unsafe_allow_html=True,
        )
        st.success(
            f"Clean execution: governed layout adapted typography to {dynamic_font_size} while preserving strict 16:9 safe margins."
        )

with tab4:
    st.markdown(
        '<div class="tab-section-title">Glossary and operational terminology index</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="tab-section-copy">A searchable reference of the financial, technical, and operational language used throughout this workspace.</div>',
        unsafe_allow_html=True,
    )

    glossary_info, glossary_controls = st.columns([1, 2], gap="medium")

    with glossary_info:
        st.markdown(
            f"""
<div class="knowledge-card">
    <div class="metric-label">Knowledge base</div>
    <div class="knowledge-stat">{len(df_glossary_master)}</div>
    <p>Operational definitions supporting ROI modeling, governed creation, deployment planning, and enterprise rollout.</p>
</div>
""",
            unsafe_allow_html=True,
        )

    with glossary_controls:
        st.markdown('<div class="knowledge-card">', unsafe_allow_html=True)
        col_search, col_filter = st.columns([2, 1])

        with col_search:
            search_query = st.text_input(
                "Search terms by keyword",
                value="",
                placeholder="Type a word such as linter, token, telemetry, or ROI...",
            )

        with col_filter:
            selected_term_dropdown = st.selectbox(
                "Filter by specific term",
                options=["All Terms"] + list(df_glossary_master["Term"].values),
            )

        st.markdown("</div>", unsafe_allow_html=True)

    df_filtered = df_glossary_master.copy()

    if selected_term_dropdown != "All Terms":
        df_filtered = df_filtered[df_filtered["Term"] == selected_term_dropdown]
    elif search_query.strip():
        q = search_query.strip().lower()
        df_filtered = df_filtered[
            df_filtered["Term"].str.lower().str.contains(q)
            | df_filtered["Context and Operational Meaning"].str.lower().str.contains(q)
        ]

    result_label = "term" if len(df_filtered) == 1 else "terms"
    st.markdown(
        f'<div class="section-kicker" style="display:inline-block; margin:0.2rem 0 0.65rem;">{len(df_filtered)} {result_label} shown</div>',
        unsafe_allow_html=True,
    )

    st.dataframe(
        df_filtered,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Term": st.column_config.TextColumn("Term", width="small"),
            "Context and Operational Meaning": st.column_config.TextColumn(
                "Context and Operational Meaning",
                width="large",
            ),
        },
    )

st.markdown(
    '<div class="custom-footer">Built by Robin Sylvester · Plus AI enterprise strategy workspace</div>',
    unsafe_allow_html=True,
)

st.markdown("</div>", unsafe_allow_html=True)
