"""
RetailPulse
Theme Management

Handles dashboard theme initialization and Plotly theme configuration.
"""

from __future__ import annotations

import streamlit as st
import plotly.io as pio

from src.constants import (
    BACKGROUND_COLOR,
    CARD_BACKGROUND,
    PRIMARY_COLOR,
    SECONDARY_COLOR,
    SUCCESS_COLOR,
    WARNING_COLOR,
    ERROR_COLOR,
    INFO_COLOR,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    BORDER_COLOR,
    CHART_COLORS,
)


# ==========================================================
# SESSION STATE
# ==========================================================

def initialize_theme() -> None:
    """
    Initialize dashboard theme variables.
    """

    defaults = {
        "theme": "dark",
        "primary_color": PRIMARY_COLOR,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    _register_plotly_theme()


# ==========================================================
# PLOTLY THEME
# ==========================================================

def _register_plotly_theme() -> None:
    """
    Register a custom Plotly theme used across the dashboard.
    """

    pio.templates["retailpulse"] = {
        "layout": {

            # Background
            "paper_bgcolor": BACKGROUND_COLOR,
            "plot_bgcolor": CARD_BACKGROUND,

            # Font
            "font": {
                "family": "Inter, Segoe UI, sans-serif",
                "color": TEXT_PRIMARY,
                "size": 14,
            },

            # Titles
            "title": {
                "font": {
                    "size": 22,
                    "color": TEXT_PRIMARY,
                },
                "x": 0.02,
                "xanchor": "left",
            },

            # Color sequence
            "colorway": CHART_COLORS,

            # Axes
            "xaxis": {
                "gridcolor": BORDER_COLOR,
                "linecolor": BORDER_COLOR,
                "zerolinecolor": BORDER_COLOR,
                "tickfont": {
                    "color": TEXT_SECONDARY,
                    },
                "title": {
                    "font": {
                        "color": TEXT_PRIMARY,
                    }
                },
            },

            "yaxis": {
                "gridcolor": BORDER_COLOR,
                "linecolor": BORDER_COLOR,
                "zerolinecolor": BORDER_COLOR,
                "tickfont": {
                    "color": TEXT_SECONDARY,
                    },
                "title": {
                    "font": {
                        "color": TEXT_PRIMARY,
                    }
                },
            },

            # Legend
            "legend": {
                "bgcolor": "rgba(0,0,0,0)",
                "borderwidth": 0,
                "font": {
                    "color": TEXT_PRIMARY,
                },
            },

            # Hover
            "hoverlabel": {
                "bgcolor": CARD_BACKGROUND,
                "font": {
                    "color": TEXT_PRIMARY,
                },
            },

            # Margins
            "margin": {
                "l": 25,
                "r": 25,
                "t": 60,
                "b": 25,
            },

            # Modebar
            "modebar": {
                "bgcolor": BACKGROUND_COLOR,
            },

            "hovermode": "x unified",
        }
    }

    pio.templates.default = "retailpulse"


# ==========================================================
# COLOR HELPERS
# ==========================================================

STATUS_COLORS = {
    "success": SUCCESS_COLOR,
    "warning": WARNING_COLOR,
    "error": ERROR_COLOR,
    "info": INFO_COLOR,
    "primary": PRIMARY_COLOR,
    "secondary": SECONDARY_COLOR,
}


def get_status_color(status: str) -> str:
    """
    Return dashboard color based on status name.
    """

    return STATUS_COLORS.get(status.lower(), PRIMARY_COLOR)


def get_color_palette() -> list[str]:
    """
    Return dashboard chart palette.
    """

    return CHART_COLORS.copy()


# ==========================================================
# CHART DEFAULTS
# ==========================================================

CHART_CONFIG = {
    "displaylogo": False,
    "responsive": True,
    "scrollZoom": False,
    "displayModeBar": True,
    "modeBarButtonsToRemove": [
        "lasso2d",
        "select2d",
        "zoomIn2d",
        "zoomOut2d",
        "autoScale2d",
    ],
}