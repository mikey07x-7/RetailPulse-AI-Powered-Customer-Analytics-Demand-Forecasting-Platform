"""
RetailPulse
Reusable Layout Components

Author: Junaid

This module contains reusable UI components used across
all dashboard pages.
"""

from __future__ import annotations

from contextlib import contextmanager

import streamlit as st

from src.constants import (
    APP_NAME,
    APP_TAGLINE,
)


# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

def page_header(title, subtitle=None, icon=""):

    st.markdown(
        f"""
        <h1 style="color:white;">
            {icon} {title}
        </h1>

        <p style="color:#94A3B8;">
            {subtitle}
        </p>
        """,
        unsafe_allow_html=True,
    )

# ==========================================================
# SECTION HEADER
# ==========================================================

def section_header(
    title: str,
    description: str | None = None
) -> None:
    """
    Display section title.
    """

    st.markdown(f"### {title}")

    if description:
        st.caption(description)


# ==========================================================
# CARD
# ==========================================================

@contextmanager
def card():
    """
    Card container.

    Usage

    with card():
        st.write(...)
    """

    st.markdown(
        '<div class="dashboard-card">',
        unsafe_allow_html=True,
    )

    yield

    st.markdown(
        "</div>",
        unsafe_allow_html=True,
    )


# ==========================================================
# KPI ROW
# ==========================================================

def columns_2():
    return st.columns(2)


def columns_3():
    return st.columns(3)


def columns_4():
    return st.columns(4)


def columns_5():
    return st.columns(5)


# ==========================================================
# SPACERS
# ==========================================================

def space(
    height: float = 1
) -> None:
    """
    Add vertical spacing.
    """

    for _ in range(int(height)):
        st.write("")


# ==========================================================
# DIVIDER
# ==========================================================

def divider():
    st.divider()


# ==========================================================
# INFO BOX
# ==========================================================

def info(message: str):

    st.info(message)


def success(message: str):

    st.success(message)


def warning(message: str):

    st.warning(message)


def error(message: str):

    st.error(message)


# ==========================================================
# EMPTY STATE
# ==========================================================

def empty_state(
    title: str,
    description: str
):

    st.markdown(
        f"""
        <div class="dashboard-card"
             style="text-align:center;padding:50px;">

            <h2>{title}</h2>

            <p>{description}</p>

        </div>
        """,
        unsafe_allow_html=True,
    )


# ==========================================================
# LOADING PLACEHOLDER
# ==========================================================

@contextmanager
def loading(text: str = "Loading..."):

    with st.spinner(text):

        yield


# ==========================================================
# PAGE FOOTER
# ==========================================================

def footer():

    st.markdown("---")

    st.caption(
        f"{APP_NAME} • AI-Powered Retail Analytics Dashboard"
    )


# ==========================================================
# HERO BANNER
# ==========================================================

def hero_banner():

    st.markdown(
        f"""
        <div class="dashboard-card fade-in">

            <h1 style="margin-bottom:5px;">
                📊 {APP_NAME}
            </h1>

            <p style="font-size:18px;color:#CBD5E1;">

                Transform retail data into actionable business insights.

            </p>

        </div>
        """,
        unsafe_allow_html=True,
    )


# ==========================================================
# PAGE CONTAINER
# ==========================================================

@contextmanager
def page():

    st.container()

    yield