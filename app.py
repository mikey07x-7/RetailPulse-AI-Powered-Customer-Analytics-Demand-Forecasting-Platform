"""
RetailPulse
Main Entry Point

Author : Junaid
"""

from pathlib import Path
import streamlit as st


# -------------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------------

st.set_page_config(
    page_title="RetailPulse",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# -------------------------------------------------------
# IMPORTS
# -------------------------------------------------------

from src.styles import load_css
from src.theme import initialize_theme


# -------------------------------------------------------
# INITIALIZATION
# -------------------------------------------------------

initialize_theme()
load_css()


# -------------------------------------------------------
# LANDING PAGE
# -------------------------------------------------------

st.markdown(
    """
    <div style="padding-top:120px;text-align:center">

    <h1 style="font-size:64px;">
    📊 RetailPulse
    </h1>

    <p style="font-size:22px;color:gray;">
    AI Powered Retail Analytics Dashboard
    </p>

    <br>

    Open the sidebar and select a dashboard page.

    </div>
    """,
    unsafe_allow_html=True,
)