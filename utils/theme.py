"""Shared styling helpers for a consistent cybersecurity look across pages."""

import streamlit as st

PRIMARY = "#00E5A0"      # neon green-teal accent
PRIMARY_DIM = "#0FA37A"
DANGER = "#FF4B5C"
BG_DARK = "#0B1220"
CARD_BG = "#121B2E"
BORDER = "#1E2A45"
TEXT_MUTED = "#9BB0CE"

CUSTOM_CSS = f"""
<style>
    .stApp {{
        background-color: {BG_DARK};
    }}

    /* Headings */
    h1, h2, h3 {{
        letter-spacing: 0.3px;
    }}

    /* Metric cards */
    div[data-testid="stMetric"] {{
        background-color: {CARD_BG};
        border: 1px solid {BORDER};
        border-radius: 12px;
        padding: 14px 18px;
    }}
    div[data-testid="stMetricLabel"] {{
        color: {TEXT_MUTED};
    }}

    /* Custom badge / pill */
    .cs-badge {{
        display: inline-block;
        background-color: rgba(0, 229, 160, 0.12);
        color: {PRIMARY};
        border: 1px solid rgba(0, 229, 160, 0.35);
        border-radius: 999px;
        padding: 4px 14px;
        margin: 3px 6px 3px 0;
        font-size: 0.85rem;
        font-weight: 600;
    }}

    .cs-hero {{
        padding: 28px 32px;
        border-radius: 16px;
        background: linear-gradient(135deg, rgba(0,229,160,0.10) 0%, rgba(18,27,46,0.4) 60%);
        border: 1px solid {BORDER};
        margin-bottom: 18px;
    }}

    .cs-card {{
        background-color: {CARD_BG};
        border: 1px solid {BORDER};
        border-radius: 14px;
        padding: 20px 22px;
        margin-bottom: 14px;
    }}

    .cs-section-title {{
        color: {PRIMARY};
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-size: 0.8rem;
        font-weight: 700;
        margin-bottom: 4px;
    }}

    .cs-muted {{
        color: {TEXT_MUTED};
    }}

    .cs-footer {{
        text-align: center;
        color: {TEXT_MUTED};
        font-size: 0.82rem;
        padding-top: 24px;
        border-top: 1px solid {BORDER};
        margin-top: 32px;
    }}

    /* Dataframe tweak */
    div[data-testid="stDataFrame"] {{
        border: 1px solid {BORDER};
        border-radius: 10px;
    }}
</style>
"""


def apply_theme(page_title: str, page_icon: str = "🛡️"):
    st.set_page_config(
        page_title=f"{page_title} · CyberShield AI",
        page_icon=page_icon,
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def render_sidebar():
    with st.sidebar:
        st.markdown("### 🛡️ CyberShield AI")
        st.caption("GPU-Accelerated Network Intrusion Detection")
        st.markdown("---")
        st.markdown(
            """
            **Dataset:** CIC-IDS2017
            **Records processed:** 1.5M
            **Best model:** cuML Random Forest
            **F1-score:** 99.55%
            """
        )
        st.markdown("---")
        st.markdown("**Links**")
        st.markdown("- [GitHub Repository](https://github.com/iYm10/CyberShield-AI)")
        st.markdown("- [Project Notebook](https://github.com/iYm10/CyberShield-AI/blob/main/CyberShield_AI.ipynb)")
        st.markdown("- [Full PDF Report](https://github.com/iYm10/CyberShield-AI/blob/main/CyberShield_AI_Report.pdf)")
        st.markdown("---")
        st.caption("Diploma in Data Science and AI · Tuwaiq Academy")
        st.caption("Author: Yahya Ali Majrashi")


def footer():
    st.markdown(
        """
        <div class="cs-footer">
            CyberShield AI — GPU-Accelerated Network Intrusion Detection using RAPIDS cuDF &amp; cuML on the CIC-IDS2017 dataset.<br>
            Built as part of the Diploma in Data Science and AI, Tuwaiq Academy (Scalable Data Science course).
        </div>
        """,
        unsafe_allow_html=True,
    )
