"""
RetailPulse
Global CSS Styling

Contains all custom CSS used throughout the dashboard.
"""

from __future__ import annotations

import streamlit as st

from src.constants import (
    BACKGROUND_COLOR,
    CARD_BACKGROUND,
    BORDER_COLOR,
    PRIMARY_COLOR,
    SECONDARY_COLOR,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    CARD_RADIUS,
    CARD_SHADOW,
)


def load_css() -> None:
    """
    Inject custom CSS into the Streamlit application.
    """

    st.markdown(
        f"""
<style>

/* ==========================================================
   GOOGLE FONT
========================================================== */

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');


html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif;
}}


/* ==========================================================
   MAIN APP
========================================================== */

.stApp {{
    background: {BACKGROUND_COLOR};
    color: {TEXT_PRIMARY};
}}


/* ==========================================================
   REMOVE STREAMLIT DEFAULT PADDING
========================================================== */

.block-container {{
    padding-top: 1.2rem;
    padding-bottom: 2rem;
    padding-left: 2rem;
    padding-right: 2rem;
    max-width: 100%;
}}


/* ==========================================================
   HEADER
========================================================== */

.dashboard-title {{
    font-size: 40px;
    font-weight: 800;
    color: white;
    margin-bottom: 5px;
}}

.dashboard-subtitle {{
    font-size: 16px;
    color: {TEXT_SECONDARY};
    margin-bottom: 25px;
}}


/* ==========================================================
   CARD
========================================================== */

.dashboard-card {{

    background: {CARD_BACKGROUND};

    border: 1px solid {BORDER_COLOR};

    border-radius: {CARD_RADIUS};

    padding: 24px;

    box-shadow: {CARD_SHADOW};

    transition: 0.25s ease;

}}

.dashboard-card:hover {{

    transform: translateY(-4px);

    border-color: {PRIMARY_COLOR};

}}


/* ==========================================================
   KPI CARD
========================================================== */

.kpi-card {{

    background: linear-gradient(
        135deg,
        {CARD_BACKGROUND},
        #23324b
    );

    border-radius: {CARD_RADIUS};

    padding: 24px;

    border: 1px solid {BORDER_COLOR};

    transition: all .25s ease;

}}

.kpi-card:hover {{

    border-color: {PRIMARY_COLOR};

    transform: translateY(-5px);

}}

.kpi-label {{

    color:{TEXT_SECONDARY};

    font-size:14px;

    margin-bottom:10px;

}}

.kpi-value {{

    color:white;

    font-size:34px;

    font-weight:700;

}}

.kpi-change {{

    margin-top:12px;

    color:#22c55e;

    font-size:14px;

}}


/* ==========================================================
   SIDEBAR
========================================================== */

section[data-testid="stSidebar"] {{

    background:{CARD_BACKGROUND};

    border-right:1px solid {BORDER_COLOR};

}}

section[data-testid="stSidebar"] * {{

    color:white;

}}


/* ==========================================================
   BUTTONS
========================================================== */

.stButton>button {{

    width:100%;

    border-radius:12px;

    border:none;

    padding:.65rem;

    font-weight:600;

    background:{PRIMARY_COLOR};

    color:white;

}}

.stButton>button:hover {{

    background:{SECONDARY_COLOR};

}}


/* ==========================================================
   METRIC
========================================================== */

div[data-testid="metric-container"] {{

    background:{CARD_BACKGROUND};

    border:1px solid {BORDER_COLOR};

    padding:18px;

    border-radius:{CARD_RADIUS};

}}

div[data-testid="metric-container"]:hover {{

    border-color:{PRIMARY_COLOR};

}}


/* ==========================================================
   SELECTBOX
========================================================== */

.stSelectbox > div > div {{

    background:{CARD_BACKGROUND};

}}


/* ==========================================================
   MULTISELECT
========================================================== */

.stMultiSelect > div > div {{

    background:{CARD_BACKGROUND};

}}


/* ==========================================================
   DATE INPUT
========================================================== */

.stDateInput > div > div {{

    background:{CARD_BACKGROUND};

}}


/* ==========================================================
   DATAFRAME
========================================================== */

[data-testid="stDataFrame"] {{

    border-radius:{CARD_RADIUS};

    border:1px solid {BORDER_COLOR};

}}


/* ==========================================================
   TABS
========================================================== */

.stTabs [data-baseweb="tab"] {{

    height:52px;

    border-radius:10px;

}}

.stTabs [aria-selected="true"] {{

    background:{PRIMARY_COLOR};

    color:white;

}}


/* ==========================================================
   EXPANDER
========================================================== */

.streamlit-expanderHeader {{

    font-weight:600;

}}


/* ==========================================================
   PROGRESS BAR
========================================================== */

.stProgress > div > div > div > div {{

    background:{PRIMARY_COLOR};

}}


/* ==========================================================
   SCROLLBAR
========================================================== */

::-webkit-scrollbar {{

    width:8px;

}}

::-webkit-scrollbar-thumb {{

    background:{PRIMARY_COLOR};

    border-radius:10px;

}}

::-webkit-scrollbar-track {{

    background:{BACKGROUND_COLOR};

}}


/* ==========================================================
   PLOTLY
========================================================== */

.js-plotly-plot {{

    border-radius:{CARD_RADIUS};

}}


/* ==========================================================
   HIDE STREAMLIT BRANDING
========================================================== */

#MainMenu {{
    visibility:hidden;
}}

footer {{
    visibility:hidden;
}}

header {{
    visibility:hidden;
}}


/* ==========================================================
   FADE ANIMATION
========================================================== */

.fade-in {{

    animation: fadeIn .4s ease;

}}

@keyframes fadeIn {{

    from {{

        opacity:0;

        transform:translateY(10px);

    }}

    to {{

        opacity:1;

        transform:translateY(0);

    }}

}}

</style>
""",
        unsafe_allow_html=True,
    )