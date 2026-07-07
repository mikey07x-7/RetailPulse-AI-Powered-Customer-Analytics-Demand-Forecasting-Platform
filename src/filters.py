"""
RetailPulse
Dynamic Filter Engine

Reusable sidebar filters for all dashboard pages.
"""

from __future__ import annotations

from typing import Optional

import pandas as pd
import streamlit as st


class FilterEngine:
    """
    Generic DataFrame filter engine.
    """

    def __init__(
        self,
        df: pd.DataFrame,
        *,
        key_prefix: str = "",
    ):

        self.df = df.copy()
        self.filtered_df = df.copy()
        self.key_prefix = key_prefix

    # ======================================================
    # MULTISELECT
    # ======================================================

    def multiselect(
        self,
        column: str,
        label: Optional[str] = None,
    ):

        if column not in self.filtered_df.columns:
            return

        values = sorted(
            self.filtered_df[column]
            .dropna()
            .unique()
            .tolist()
        )

        selected = st.sidebar.multiselect(
            label or column,
            values,
            default=values,
            key=f"{self.key_prefix}_{column}",
        )

        self.filtered_df = self.filtered_df[
            self.filtered_df[column].isin(selected)
        ]

    # ======================================================
    # SELECTBOX
    # ======================================================

    def selectbox(
        self,
        column: str,
        label: Optional[str] = None,
    ):

        if column not in self.filtered_df.columns:
            return

        values = sorted(
            self.filtered_df[column]
            .dropna()
            .unique()
            .tolist()
        )

        values = ["All"] + values

        selected = st.sidebar.selectbox(
            label or column,
            values,
            key=f"{self.key_prefix}_{column}",
        )

        if selected != "All":

            self.filtered_df = self.filtered_df[
                self.filtered_df[column] == selected
            ]

    # ======================================================
    # SLIDER
    # ======================================================

    def slider(
        self,
        column: str,
        label: Optional[str] = None,
    ):

        if column not in self.filtered_df.columns:
            return

        minimum = float(self.filtered_df[column].min())
        maximum = float(self.filtered_df[column].max())

        selected = st.sidebar.slider(
            label or column,
            minimum,
            maximum,
            (minimum, maximum),
            key=f"{self.key_prefix}_{column}",
        )

        self.filtered_df = self.filtered_df[
            self.filtered_df[column].between(
                selected[0],
                selected[1],
            )
        ]

    # ======================================================
    # DATE RANGE
    # ======================================================

    def date_range(
        self,
        column: str,
        label: Optional[str] = None,
    ):

        if column not in self.filtered_df.columns:
            return

        dates = pd.to_datetime(
            self.filtered_df[column]
        )

        start = dates.min()
        end = dates.max()

        selected = st.sidebar.date_input(
            label or column,
            value=(start, end),
            key=f"{self.key_prefix}_{column}",
        )

        if len(selected) == 2:

            start_date, end_date = selected

            self.filtered_df = self.filtered_df[
                dates.between(
                    pd.to_datetime(start_date),
                    pd.to_datetime(end_date),
                )
            ]

    # ======================================================
    # RESET
    # ======================================================

    def reset_button(self):

        if st.sidebar.button("🔄 Reset Filters"):

            for key in list(st.session_state.keys()):

                if key.startswith(self.key_prefix):

                    del st.session_state[key]

            st.rerun()

    # ======================================================
    # RETURN DATAFRAME
    # ======================================================

    def get_dataframe(self) -> pd.DataFrame:

        return self.filtered_df

    # ======================================================
    # COMPLETE FILTER PANEL
    # ======================================================

    def render(
        self,
        *,
        categorical: list[str] | None = None,
        numeric: list[str] | None = None,
        dates: list[str] | None = None,
    ) -> pd.DataFrame:

        st.sidebar.markdown("## 🔍 Filters")

        if categorical:

            for col in categorical:

                self.multiselect(col)

        if numeric:

            for col in numeric:

                self.slider(col)

        if dates:

            for col in dates:

                self.date_range(col)

        self.reset_button()

        return self.filtered_df