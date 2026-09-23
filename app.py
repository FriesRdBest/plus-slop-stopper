from datetime import datetime
from io import BytesIO
from xml.sax.saxutils import escape

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    HRFlowable,
    KeepTogether,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

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

PRESETS = {
    "Pilot": {
        "team_size": 15,
        "decks_per_month": 4.0,
        "hours_per_deck": 2.0,
        "hourly_rate": 45.0,
        "currency": "$ USD - US Dollar",
        "brand_tier": "Standard (Single Corporate Identity)",
        "description": "A focused launch cohort validating value, workflow fit, and template governance.",
    },
    "Department rollout": {
        "team_size": 75,
        "decks_per_month": 6.0,
        "hours_per_deck": 3.0,
        "hourly_rate": 55.0,
        "currency": "$ USD - US Dollar",
        "brand_tier": "Multi Brand (Two to Four Sub Brands and Business Units)",
        "description": "A department-level rollout across multiple teams, templates, and operating rhythms.",
    },
    "Enterprise rollout": {
        "team_size": 500,
        "decks_per_month": 8.0,
        "hours_per_deck": 3.5,
        "hourly_rate": 65.0,
        "currency": "$ USD - US Dollar",
        "brand_tier": "Global Enterprise (Complex Design System and Custom Tokens)",
        "description": "A governed enterprise program with complex architecture and broad creator adoption.",
    },
}

DEFAULT_SCENARIO = {
    "team_size": 50,
    "decks_per_month": 6.0,
    "hours_per_deck": 3.5,
    "hourly_rate": 45.0,
    "currency": "$ USD - US Dollar",
    "brand_tier": "Standard (Single Corporate Identity)",
}


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


def get_scenario_name(values):
    for preset_name, preset in PRESETS.items():
        if all(values[key] == preset[key] for key in DEFAULT_SCENARIO):
            return preset_name
    return "Custom scenario"


def apply_preset(preset_name):
    preset = PRESETS[preset_name]
    st.session_state.team_size = preset["team_size"]
    st.session_state.decks_per_month = preset["decks_per_month"]
    st.session_state.hours_per_deck = preset["hours_per_deck"]
    st.session_state.hourly_rate = preset["hourly_rate"]
    st.session_state.currency = preset["currency"]
    st.session_state.brand_tier = preset["brand_tier"]


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


def pdf_paragraph(text, style):
    return Paragraph(escape(str(text)).replace("\n", "<br/>"), style)


def build_executive_summary_pdf(
    client_name,
    scenario_name,
    curr,
    team_size,
    decks_per_month,
    hours_per_deck,
    hourly_rate,
    total_monthly_decks,
    annual_hours_saved,
    annual_cost_savings,
    cumulative_hours,
    cumulative_savings,
    deployment,
):
    output = BytesIO()
    document = SimpleDocTemplate(
        output,
        pagesize=letter,
        rightMargin=0.55 * inch,
        leftMargin=0.55 * inch,
        topMargin=0.45 * inch,
        bottomMargin=0.45 * inch,
        title="Plus AI Executive Value Summary",
        author="Plus AI",
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "ExecutiveTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=21,
        leading=24,
        textColor=HexColor("#1d333d"),
        spaceAfter=4,
    )
    subtitle_style = ParagraphStyle(
        "ExecutiveSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=12,
        textColor=HexColor("#607680"),
        spaceAfter=12,
    )
    eyebrow_style = ParagraphStyle(
        "Eyebrow",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=7.5,
        leading=10,
        textColor=HexColor("#3f7f95"),
        spaceAfter=4,
    )
    section_style = ParagraphStyle(
        "Section",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=12,
        textColor=HexColor("#203842"),
        spaceBefore=8,
        spaceAfter=6,
    )
    body_style = ParagraphStyle(
        "Body",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=8.3,
        leading=11,
        textColor=HexColor("#48616b"),
    )
    metric_label_style = ParagraphStyle(
        "MetricLabel",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=6.8,
        leading=9,
        textColor=HexColor("#607680"),
    )
    metric_value_style = ParagraphStyle(
        "MetricValue",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=15,
        leading=17,
        textColor=HexColor("#1e3340"),
    )
    small_style = ParagraphStyle(
        "Small",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=7.2,
        leading=9.5,
        textColor=HexColor("#607680"),
    )
    right_small_style = ParagraphStyle(
        "RightSmall",
        parent=small_style,
        alignment=TA_RIGHT,
    )

    display_client = client_name.strip() or "Current modeled scenario"
    export_timestamp = datetime.now().strftime("%B %-d, %Y") if hasattr(datetime.now(), "strftime") else ""

    story = [
        pdf_paragraph("PLUS AI / ENTERPRISE DECISION INTELLIGENCE", eyebrow_style),
        pdf_paragraph("Executive Value Summary", title_style),
        pdf_paragraph(
            f"{display_client} · {scenario_name} · Generated {export_timestamp}",
            subtitle_style,
        ),
        HRFlowable(
            width="100%",
            thickness=1,
            color=HexColor("#b7d7df"),
            spaceAfter=10,
        ),
    ]

    metric_data = [
        [
            pdf_paragraph("ANNUAL VALUE DELIVERED", metric_label_style),
            pdf_paragraph("ANNUAL HOURS RECLAIMED", metric_label_style),
            pdf_paragraph("MONTHLY DECK VELOCITY", metric_label_style),
        ],
        [
            pdf_paragraph(f"{curr}{annual_cost_savings:,.0f}", metric_value_style),
            pdf_paragraph(f"{annual_hours_saved:,.0f} hrs", metric_value_style),
            pdf_paragraph(f"{total_monthly_decks:,.0f} decks", metric_value_style),
        ],
        [
            pdf_paragraph("Estimated productivity capacity unlocked.", small_style),
            pdf_paragraph("Capacity returned from manual formatting work.", small_style),
            pdf_paragraph("Aggregate presentation output across active creators.", small_style),
        ],
    ]

    metric_table = Table(
        metric_data,
        colWidths=[2.45 * inch, 2.45 * inch, 2.45 * inch],
    )
    metric_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), HexColor("#edf5f5")),
                ("BOX", (0, 0), (-1, -1), 0.5, HexColor("#c4dce1")),
                ("INNERGRID", (0, 0), (-1, -1), 0.35, HexColor("#d6e7e9")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 11),
                ("RIGHTPADDING", (0, 0), (-1, -1), 11),
                ("TOPPADDING", (0, 0), (-1, 0), 9),
                ("TOPPADDING", (0, 1), (-1, 1), 3),
                ("BOTTOMPADDING", (0, 1), (-1, 1), 3),
                ("BOTTOMPADDING", (0, 2), (-1, 2), 9),
            ]
        )
    )
    story.append(metric_table)
    story.append(Spacer(1, 10))

    story.append(pdf_paragraph("Scenario assumptions", section_style))

    assumptions_data = [
        [
            pdf_paragraph("Active slide creators", metric_label_style),
            pdf_paragraph(f"{team_size:,}", body_style),
            pdf_paragraph("Avg. decks / creator / month", metric_label_style),
            pdf_paragraph(f"{decks_per_month:,.1f}", body_style),
        ],
        [
            pdf_paragraph("Manual formatting hours / deck", metric_label_style),
            pdf_paragraph(f"{hours_per_deck:,.2f} hrs", body_style),
            pdf_paragraph("Average worker hourly rate", metric_label_style),
            pdf_paragraph(f"{curr}{hourly_rate:,.2f}", body_style),
        ],
        [
            pdf_paragraph("Deployment readiness", metric_label_style),
            pdf_paragraph(f"{deployment['tier']}: {deployment['name']}", body_style),
            pdf_paragraph("Rollout posture", metric_label_style),
            pdf_paragraph(deployment["status"], body_style),
        ],
    ]

    assumptions_table = Table(
        assumptions_data,
        colWidths=[1.85 * inch, 1.8 * inch, 1.85 * inch, 1.9 * inch],
    )
    assumptions_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.white),
                ("BOX", (0, 0), (-1, -1), 0.5, HexColor("#d1e2e5")),
                ("INNERGRID", (0, 0), (-1, -1), 0.35, HexColor("#e0ebed")),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )
    story.append(assumptions_table)
    story.append(Spacer(1, 7))

    story.append(pdf_paragraph("Value ramp and deployment recommendation", section_style))

    ramp_data = [
        [
            pdf_paragraph("Month 1", metric_label_style),
            pdf_paragraph("Month 6", metric_label_style),
            pdf_paragraph("Month 12", metric_label_style),
        ],
        [
            pdf_paragraph(f"{curr}{cumulative_savings[0]:,.0f}", metric_value_style),
            pdf_paragraph(f"{curr}{cumulative_savings[5]:,.0f}", metric_value_style),
            pdf_paragraph(f"{curr}{cumulative_savings[11]:,.0f}", metric_value_style),
        ],
        [
            pdf_paragraph(f"{cumulative_hours[0]:,.0f} reclaimed hours", small_style),
            pdf_paragraph(f"{cumulative_hours[5]:,.0f} reclaimed hours", small_style),
            pdf_paragraph(f"{cumulative_hours[11]:,.0f} reclaimed hours", small_style),
        ],
    ]

    ramp_table = Table(
        ramp_data,
        colWidths=[2.45 * inch, 2.45 * inch, 2.45 * inch],
    )
    ramp_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), HexColor("#f2f7fb")),
                ("BOX", (0, 0), (-1, -1), 0.5, HexColor("#d2e2eb")),
                ("INNERGRID", (0, 0), (-1, -1), 0.35, HexColor("#dceaf0")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 11),
                ("RIGHTPADDING", (0, 0), (-1, -1), 11),
                ("TOPPADDING", (0, 0), (-1, 0), 8),
                ("TOPPADDING", (0, 1), (-1, 1), 3),
                ("BOTTOMPADDING", (0, 1), (-1, 1), 3),
                ("BOTTOMPADDING", (0, 2), (-1, 2), 8),
            ]
        )
    )
    story.append(ramp_table)
    story.append(Spacer(1, 8))

    recommendation = (
        f"<b>{escape(deployment['tier'])}: {escape(deployment['name'])}</b> — "
        f"{escape(deployment['overview'])}"
    )
    methodology = (
        "Model methodology: annual reclaimed hours = active creators × average decks per month × "
        "manual formatting hours per deck × 65% modeled efficiency gain × 12 months. "
        "Annual value = annual reclaimed hours × average worker hourly rate."
    )

    story.extend(
        [
            Paragraph(recommendation, body_style),
            Spacer(1, 6),
            Paragraph(methodology, small_style),
            Spacer(1, 7),
            HRFlowable(
                width="100%",
                thickness=0.6,
                color=HexColor("#d0e0e3"),
                spaceAfter=5,
            ),
            Table(
                [
                    [
                        pdf_paragraph(
                            "Plus AI Enterprise ROI & Deployment Simulator",
                            small_style,
                        ),
                        pdf_paragraph(
                            "Prepared from live scenario assumptions",
                            right_small_style,
                        ),
                    ]
                ],
                colWidths=[4.2 * inch, 3.15 * inch],
                style=TableStyle(
                    [
                        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                        ("LEFTPADDING", (0, 0), (-1, -1), 0),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                        ("TOPPADDING", (0, 0), (-1, -1), 0),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
                    ]
                ),
            ),
        ]
    )

    document.build(story)
    output.seek(0)
    return output.getvalue()


if "show_onboarding" not in st.session_state:
    st.session_state.show_onboarding = True

for key, value in DEFAULT_SCENARIO.items():
    if key not in st.session_state:
        st.session_state[key] = value

if "client_name" not in st.session_state:
    st.session_state.client_name = ""

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

    .topbar {
        min-height: 58px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1rem;
        padding: 0.42rem 0.62rem 0.52rem;
        margin-bottom: 1.0rem;
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

    .onboarding-card {
        margin: 0.2rem 0 1rem;
        padding: 1.05rem 1.15rem;
        border: 1px solid rgba(255, 255, 255, 0.74);
        border-radius: 19px;
        background:
            linear-gradient(135deg, rgba(231, 246, 249, 0.72), rgba(232, 233, 248, 0.64)),
            rgba(250, 253, 252, 0.50);
        box-shadow:
            inset 0 1px 0 rgba(255, 255, 255, 0.88),
            0 10px 22px rgba(66, 86, 93, 0.07);
    }

    .onboarding-eyebrow,
    .eyebrow,
    .metric-label,
    .timeline-label,
    .preset-label {
        color: #5d7984;
        font-size: 0.67rem;
        font-weight: 800;
        letter-spacing: 0.15em;
        text-transform: uppercase;
    }

    .onboarding-title {
        margin-top: 0.35rem;
        color: #1e3741;
        font-size: 1.02rem;
        font-weight: 760;
        letter-spacing: -0.022em;
    }

    .onboarding-copy {
        margin-top: 0.32rem;
        max-width: 850px;
        color: #58707a;
        font-size: 0.79rem;
        line-height: 1.5;
    }

    .onboarding-steps {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 0.7rem;
        margin-top: 0.85rem;
    }

    .onboarding-step {
        padding: 0.68rem 0.72rem;
        border: 1px solid rgba(91, 138, 153, 0.13);
        border-radius: 13px;
        background: rgba(255, 255, 255, 0.38);
        color: #536b75;
        font-size: 0.73rem;
        line-height: 1.42;
    }

    .onboarding-step strong {
        display: block;
        margin-bottom: 0.16rem;
        color: #294b58;
        font-size: 0.72rem;
    }

    .scenario-panel {
        margin: 0.35rem 0 0.25rem;
        padding: 1rem 1.05rem;
        border: 1px solid rgba(48, 126, 111, 0.28);
        border-radius: 19px;
        background: linear-gradient(135deg, #4a9b89, #3c8797);
        box-shadow:
            inset 0 1px 0 rgba(255, 255, 255, 0.22),
            0 10px 22px rgba(54, 126, 112, 0.16);
    }

    .scenario-panel .preset-label {
        color: rgba(255, 255, 255, 0.74);
    }

    .scenario-panel-title {
        margin: 0;
        color: #ffffff;
        font-size: 0.90rem;
        font-weight: 740;
        letter-spacing: -0.012em;
    }

    .scenario-panel-copy {
        margin: 0.28rem 0 0;
        color: rgba(255, 255, 255, 0.86);
        font-size: 0.74rem;
        line-height: 1.45;
    }

    .scenario-active {
        display: inline-flex;
        align-items: center;
        margin-top: 0.65rem;
        padding: 0.33rem 0.58rem;
        border: 1px solid rgba(48, 126, 111, 0.22);
        border-radius: 999px;
        background: rgba(75, 154, 136, 0.13);
        color: #327663;
        font-size: 0.69rem;
        font-weight: 720;
    }

    div[data-testid="stButton"] > button {
        min-height: 2.35rem;
        width: 100%;
        border-radius: 11px;
        border: 1px solid rgba(75, 111, 122, 0.18);
        color: #315866;
        background: rgba(255, 255, 255, 0.46);
        box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.72);
        font-size: 0.76rem;
        font-weight: 720;
    }

    div[data-testid="stButton"] > button:hover {
        border-color: rgba(63, 157, 188, 0.48);
        color: #226f8b;
        background: rgba(235, 248, 250, 0.72);
    }

    div[data-testid="stDownloadButton"] > button {
        min-height: 2.58rem;
        width: 100%;
        border: 1px solid rgba(48, 126, 111, 0.28);
        border-radius: 12px;
        color: #ffffff;
        background: linear-gradient(135deg, #4a9b89, #3c8797);
        box-shadow: 0 8px 18px rgba(54, 126, 112, 0.20);
        font-size: 0.78rem;
        font-weight: 740;
    }

    div[data-testid="stDownloadButton"] > button:hover {
        color: #ffffff;
        background: linear-gradient(135deg, #3d8979, #347a89);
        border-color: rgba(48, 126, 111, 0.36);
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
    .linter-summary,
    .export-card {
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

    .export-card {
        padding: 1.15rem;
    }

    .export-card-title {
        color: #263e48;
        font-size: 0.93rem;
        font-weight: 750;
        letter-spacing: -0.015em;
    }

    .export-card-copy {
        margin: 0.35rem 0 0.85rem;
        color: #617782;
        font-size: 0.75rem;
        line-height: 1.48;
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

        .onboarding-steps {
            grid-template-columns: 1fr;
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

if st.session_state.show_onboarding:
    guide_column, guide_action_column = st.columns([5, 1])
    with guide_column:
        st.markdown(
            """
<div class="onboarding-card">
    <div class="onboarding-eyebrow">START HERE</div>
    <div class="onboarding-title">Turn a presentation workflow into an executive value conversation.</div>
    <div class="onboarding-copy">Start from a rollout preset or enter your own assumptions. The model updates immediately, then the ROI, deployment, and linter workspaces explain the operational case behind the numbers.</div>
    <div class="onboarding-steps">
        <div class="onboarding-step"><strong>01 · Set the context</strong>Add a client name if relevant, then select a rollout starting point.</div>
        <div class="onboarding-step"><strong>02 · Tune the model</strong>Adjust creator volume, deck activity, formatting time, and labour rate.</div>
        <div class="onboarding-step"><strong>03 · Share the case</strong>Explore the ROI and deployment plan, then export a one-page PDF summary.</div>
    </div>
</div>
""",
            unsafe_allow_html=True,
        )
    with guide_action_column:
        st.write("")
        st.write("")
        if st.button("Hide guide", key="hide_onboarding"):
            st.session_state.show_onboarding = False
            st.rerun()
else:
    if st.button("Show quick guide", key="show_onboarding_button"):
        st.session_state.show_onboarding = True
        st.rerun()

st.markdown(
    """
<div class="scenario-panel">
    <div class="preset-label">SCENARIO SETUP</div>
    <div class="scenario-panel-title">Personalize the model, then start from the rollout posture that matches the conversation.</div>
    <div class="scenario-panel-copy">Client/company name is optional. Presets change only the assumptions; every value can still be adjusted manually.</div>
</div>
""",
    unsafe_allow_html=True,
)

scenario_name_col, scenario_context_col = st.columns([1.45, 2.55], gap="medium")

with scenario_name_col:
    client_name = st.text_input(
        "Client / company name (optional)",
        key="client_name",
        placeholder="e.g., Acme Corporation",
    )

current_values_before_preset = {
    "team_size": st.session_state.team_size,
    "decks_per_month": st.session_state.decks_per_month,
    "hours_per_deck": st.session_state.hours_per_deck,
    "hourly_rate": st.session_state.hourly_rate,
    "currency": st.session_state.currency,
    "brand_tier": st.session_state.brand_tier,
}
scenario_name_before_preset = get_scenario_name(current_values_before_preset)

with scenario_context_col:
    st.markdown(
        f'<div class="scenario-active">Active scenario · {scenario_name_before_preset}</div>',
        unsafe_allow_html=True,
    )

preset_col_1, preset_col_2, preset_col_3 = st.columns(3, gap="small")

with preset_col_1:
    if st.button("Pilot", key="preset_pilot"):
        apply_preset("Pilot")
        st.rerun()

with preset_col_2:
    if st.button("Department rollout", key="preset_department"):
        apply_preset("Department rollout")
        st.rerun()

with preset_col_3:
    if st.button("Enterprise rollout", key="preset_enterprise"):
        apply_preset("Enterprise rollout")
        st.rerun()

preset_description = (
    PRESETS[scenario_name_before_preset]["description"]
    if scenario_name_before_preset in PRESETS
    else "A custom model built from your current organization, economic, and architecture assumptions."
)

st.markdown(
    f'<div class="scenario-panel-copy" style="margin:0.45rem 0 0.95rem;">{preset_description}</div>',
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
        step=1,
        key="team_size",
        help="Total knowledge workers, consultants, or sales reps actively creating or modifying presentations.",
    )
    final_decks_per_month = st.number_input(
        "Average decks per user / month",
        min_value=0.5,
        max_value=100.0,
        step=0.5,
        format="%.1f",
        key="decks_per_month",
        help="Estimated volume of presentations created, edited, or updated per employee every month.",
    )

with config_col_2:
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
        key="currency",
        help="Select the operational currency to standardize financial return modeling across global teams.",
    )
    curr = selected_currency_full.split(" ")[0]
    hourly_rate = st.number_input(
        f"Average worker hourly rate ({curr})",
        min_value=1.00,
        max_value=2500.00,
        step=0.25,
        format="%.2f",
        key="hourly_rate",
        help="Fully loaded hourly cost including salary and overhead of professionals creating presentations.",
    )

with config_col_3:
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
        step=0.25,
        format="%.2f",
        key="hours_per_deck",
        help="Average time a professional spends aligning shapes, fixing margins, and manually styling slides.",
    )
    brand_tier = st.selectbox(
        "Brand and template architecture tier",
        options=BRAND_TIER_OPTIONS,
        key="brand_tier",
        help="Defines organizational design complexity from single template schemas to multi-unit corporate brands.",
    )

current_values = {
    "team_size": final_team_size,
    "decks_per_month": final_decks_per_month,
    "hours_per_deck": final_hours_per_deck,
    "hourly_rate": hourly_rate,
    "currency": selected_currency_full,
    "brand_tier": brand_tier,
}
scenario_name = get_scenario_name(current_values)

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
            f"""
<div class="hero-card">
    <div class="eyebrow">PLUS AI / ENTERPRISE STRATEGY CONSOLE</div>
    <h1 class="hero-heading">Turn presentation work into measurable enterprise capacity.</h1>
    <p class="hero-description">
        Model the time, operational throughput, and financial value unlocked when
        teams replace manual slide formatting with governed AI workflows.
    </p>
    <div class="hero-tags">
        <span class="tag">{scenario_name}</span>
        <span class="tag">ROI scenario modeling</span>
        <span class="tag">Deployment planning</span>
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

st.markdown(
    """
<div class="section-heading">
    <div>
        <h2>Executive summary export</h2>
        <p>Download a one-page PDF summary of the current scenario for stakeholder review.</p>
    </div>
    <div class="section-kicker">PDF ready</div>
</div>
""",
    unsafe_allow_html=True,
)

export_left, export_right = st.columns([1.55, 1], gap="medium")

with export_left:
    export_client_label = client_name.strip() or "Current modeled scenario"
    st.markdown(
        f"""
<div class="export-card">
    <div class="export-card-title">Prepared for {escape(export_client_label)}</div>
    <div class="export-card-copy">The PDF includes current assumptions, executive outcomes, value-ramp milestones, deployment posture, and the calculation method. It reflects the model exactly as it is currently configured.</div>
</div>
""",
        unsafe_allow_html=True,
    )

with export_right:
    safe_name = "".join(
        character.lower() if character.isalnum() else "_"
        for character in (client_name.strip() or "plus_ai")
    ).strip("_")
    pdf_filename = f"{safe_name or 'plus_ai'}_executive_value_summary.pdf"
    executive_pdf = build_executive_summary_pdf(
        client_name=client_name,
        scenario_name=scenario_name,
        curr=curr,
        team_size=final_team_size,
        decks_per_month=final_decks_per_month,
        hours_per_deck=final_hours_per_deck,
        hourly_rate=hourly_rate,
        total_monthly_decks=total_monthly_decks,
        annual_hours_saved=annual_hours_saved,
        annual_cost_savings=annual_cost_savings,
        cumulative_hours=cumulative_hours,
        cumulative_savings=cumulative_savings,
        deployment=deployment,
    )
    st.download_button(
        label="Download executive PDF",
        data=executive_pdf,
        file_name=pdf_filename,
        mime="application/pdf",
        key="download_executive_pdf",
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

st.markdown(
    """
<style>
    /* Remove empty visual capsules rendered above configuration card content. */
    div[data-testid="stVerticalBlockBorderWrapper"]:has(
        div[data-testid="stMarkdownContainer"]:empty
    ) {
        display: none !important;
    }
</style>
""",
    unsafe_allow_html=True,
)
