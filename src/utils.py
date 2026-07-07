"""
RetailPulse
Utility Functions

Common helper functions used throughout the application.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

import pandas as pd
import streamlit as st


# ==========================================================
# NUMBER FORMATTING
# ==========================================================

def format_number(value: float | int) -> str:
    """
    Format large numbers using K, M, B notation.
    """

    if pd.isna(value):
        return "-"

    value = float(value)

    if abs(value) >= 1_000_000_000:
        return f"{value/1_000_000_000:.1f}B"

    if abs(value) >= 1_000_000:
        return f"{value/1_000_000:.1f}M"

    if abs(value) >= 1_000:
        return f"{value/1_000:.1f}K"

    if value.is_integer():
        return f"{int(value):,}"

    return f"{value:,.2f}"


# ==========================================================
# CURRENCY
# ==========================================================

def format_currency(value: float | int, symbol: str = "$") -> str:
    """
    Format currency values.
    """

    if pd.isna(value):
        return "-"

    return f"{symbol}{value:,.2f}"


# ==========================================================
# PERCENTAGE
# ==========================================================

def format_percentage(value: float) -> str:
    """
    Convert decimal to percentage string.
    """

    if pd.isna(value):
        return "-"

    return f"{value:.2f}%"


# ==========================================================
# DATE
# ==========================================================

def format_date(value: Any) -> str:
    """
    Format dates consistently.
    """

    if pd.isna(value):
        return "-"

    try:
        return pd.to_datetime(value).strftime("%d %b %Y")
    except Exception:
        return str(value)


# ==========================================================
# SAFE DIVISION
# ==========================================================

def safe_divide(
    numerator: float,
    denominator: float,
    default: float = 0,
) -> float:
    """
    Prevent division by zero.
    """

    if denominator == 0:
        return default

    return numerator / denominator


# ==========================================================
# DATAFRAME CHECK
# ==========================================================

def is_dataframe_empty(df: pd.DataFrame) -> bool:
    """
    Check if dataframe is None or empty.
    """

    return df is None or df.empty


# ==========================================================
# DOWNLOAD
# ==========================================================

def dataframe_to_csv(df: pd.DataFrame) -> bytes:
    """
    Convert dataframe to CSV bytes.
    """

    return df.to_csv(index=False).encode("utf-8")


# ==========================================================
# SESSION HELPERS
# ==========================================================

def set_state(key: str, value: Any) -> None:
    """
    Store a value in Streamlit session state.
    """

    st.session_state[key] = value


def get_state(key: str, default: Any = None) -> Any:
    """
    Retrieve a value from Streamlit session state.
    """

    return st.session_state.get(key, default)


# ==========================================================
# CURRENT TIME
# ==========================================================

def current_timestamp() -> str:
    """
    Return current timestamp.
    """

    return datetime.now().strftime("%d %b %Y %H:%M")


# ==========================================================
# COLUMN EXISTENCE
# ==========================================================

def has_columns(
    df: pd.DataFrame,
    columns: list[str],
) -> bool:
    """
    Check whether required columns exist.
    """

    return all(col in df.columns for col in columns)


# ==========================================================
# RESET FILTERS
# ==========================================================

def reset_filters() -> None:
    """
    Clear all user-defined filters from session state.
    """

    for key in list(st.session_state.keys()):
        if key.startswith("filter_"):
            del st.session_state[key]