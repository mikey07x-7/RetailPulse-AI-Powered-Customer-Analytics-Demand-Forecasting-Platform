"""
RetailPulse
Reusable KPI Components

Professional KPI cards for all dashboard pages.
"""

from __future__ import annotations

from typing import Optional

import streamlit as st

from src.utils import (
    format_currency,
    format_number,
)


# ==========================================================
# FORMAT VALUE
# ==========================================================

def _format_value(
    value,
    value_type: str = "number",
    currency_symbol: str = "$",
):
    """
    Format KPI values.
    """

    if value_type == "currency":
        return format_currency(value, currency_symbol)

    if value_type == "percent":
        return f"{value:.2f}%"

    return format_number(value)


# ==========================================================
# SINGLE KPI CARD
# ==========================================================

def kpi_card(
    title: str,
    value,
    *,
    icon: str = "📊",
    delta: Optional[float] = None,
    value_type: str = "number",
    currency_symbol: str = "$",
):
    """
    Render a reusable KPI card.
    """

    formatted = _format_value(
        value,
        value_type,
        currency_symbol,
    )

    delta_section = ""

    if delta is not None:

        color = "#22C55E" if delta >= 0 else "#EF4444"
        arrow = "▲" if delta >= 0 else "▼"

        delta_section = (
            f'<div class="kpi-change" '
            f'style="color:{color};font-weight:600;margin-top:10px;">'
            f'{arrow} {abs(delta):.2f}%'
            f'</div>'
        )

    html = (
        '<div class="kpi-card fade-in">'
            '<div style="display:flex;justify-content:space-between;align-items:center;">'

                '<div>'

                    f'<div class="kpi-label">{title}</div>'

                    f'<div class="kpi-value">{formatted}</div>'

                    f'{delta_section}'

                '</div>'

                f'<div style="font-size:42px;">{icon}</div>'

            '</div>'
        '</div>'
    )

    st.markdown(
        html,
        unsafe_allow_html=True,
    )

# ==========================================================
# KPI ROW
# ==========================================================

def kpi_row(cards: list[dict]):
    """
    Automatically generate KPI cards.

    Example
    -------
    cards = [
        {
            "title":"Sales",
            "value":120000,
            "icon":"💰",
            "type":"currency"
        }
    ]
    """

    columns = st.columns(len(cards))

    for col, card in zip(columns, cards):

        with col:

            kpi_card(

                title=card["title"],

                value=card["value"],

                icon=card.get("icon", "📊"),

                delta=card.get("delta"),

                value_type=card.get(
                    "type",
                    "number",
                ),

                currency_symbol=card.get(
                    "currency",
                    "$",
                ),
            )


# ==========================================================
# DIVIDER
# ==========================================================

def kpi_divider():

    st.markdown("<br>", unsafe_allow_html=True)