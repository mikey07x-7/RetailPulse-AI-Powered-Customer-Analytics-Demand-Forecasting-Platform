"""
RetailPulse
Sidebar Components

Centralized sidebar used across all dashboard pages.
"""

from __future__ import annotations

from pathlib import Path

import streamlit as st

from src.constants import (
    APP_NAME,
    APP_TAGLINE,
    VERSION,
    IMAGE_DIR,
)


# ==========================================================
# LOGO
# ==========================================================

def _show_logo() -> None:
    """
    Display application logo if available.
    """

    logo_path = IMAGE_DIR / "logo.png"

    if logo_path.exists():
        st.image(str(logo_path), use_container_width=True)
    else:
        st.markdown(
            """
            <h1 style="text-align:center;font-size:42px;">
                📊
            </h1>
            """,
            unsafe_allow_html=True,
        )


# ==========================================================
# BRANDING
# ==========================================================

def _branding() -> None:

    st.markdown(
        f"""
        <div style="text-align:center">

        <h2 style="margin-bottom:0;">
        {APP_NAME}
        </h2>

        <p style="color:#94A3B8;font-size:14px;">
        {APP_TAGLINE}
        </p>

        </div>
        """,
        unsafe_allow_html=True,
    )


# ==========================================================
# DATASET STATUS
# ==========================================================

def _dataset_status() -> None:

    st.markdown("### 📂 Dataset")

    if "df" in st.session_state:

        rows = len(st.session_state.df)

        st.success(f"Loaded ({rows:,} rows)")

    else:

        st.warning("Dataset not loaded")


# ==========================================================
# SESSION INFO
# ==========================================================

def _session_info() -> None:

    st.markdown("### ⚙ Session")

    theme = st.session_state.get("theme", "dark")

    st.write(f"**Theme:** {theme.title()}")

    st.write(f"**Version:** {VERSION}")


# ==========================================================
# QUICK HELP
# ==========================================================

def _help_box() -> None:

    with st.expander("ℹ About RetailPulse"):

        st.markdown(
            """
RetailPulse is an AI-powered retail analytics dashboard.

### Modules

- Executive Dashboard
- Customer Segmentation
- Demand Forecasting
- Churn Prediction
- Inventory Optimization
- Business Insights
"""
        )


# ==========================================================
# FOOTER
# ==========================================================

def _footer() -> None:

    st.markdown("---")

    st.caption(
        f"{APP_NAME} v{VERSION}"
    )


# ==========================================================
# PUBLIC FUNCTION
# ==========================================================

def render_sidebar() -> None:
    """
    Render the complete sidebar.
    """

    with st.sidebar:

        _show_logo()

        _branding()

        st.divider()

        _dataset_status()

        st.divider()

        _session_info()

        st.divider()

        _help_box()

        _footer()