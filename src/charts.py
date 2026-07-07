"""
RetailPulse
Reusable Plotly Charts

Author : Junaid

This module provides reusable Plotly chart functions
used across all dashboard pages.
"""

from __future__ import annotations

from typing import Optional

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from src.constants import (
    DEFAULT_CHART_HEIGHT,
    CHART_COLORS,
)

from src.theme import CHART_CONFIG


# ==========================================================
# INTERNAL HELPERS
# ==========================================================

def _validate_dataframe(df: pd.DataFrame) -> None:
    """
    Validate dataframe before plotting.
    """

    if df is None:
        raise ValueError("DataFrame cannot be None.")

    if df.empty:
        raise ValueError("DataFrame is empty.")


def _validate_columns(
    df: pd.DataFrame,
    columns: list[str],
) -> None:
    """
    Ensure all requested columns exist.
    """

    missing = [
        col for col in columns
        if col not in df.columns
    ]

    if missing:
        raise KeyError(
            f"Missing columns: {', '.join(missing)}"
        )


# ==========================================================
# COMMON LAYOUT
# ==========================================================

def _apply_layout(
    fig: go.Figure,
    *,
    title: Optional[str] = None,
    height: int = DEFAULT_CHART_HEIGHT,
) -> go.Figure:
    """
    Apply common dashboard styling.
    """

    fig.update_layout(

        title=title,

        height=height,

        margin=dict(
            l=20,
            r=20,
            t=55,
            b=20,
        ),

        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
        ),

        hovermode="x unified",
    )

    return fig


# ==========================================================
# STREAMLIT RENDERER
# ==========================================================

def render_chart(
    fig: go.Figure,
    *,
    use_container_width: bool = True,
):
    """
    Display a Plotly chart in Streamlit.
    """

    st.plotly_chart(
        fig,
        use_container_width=use_container_width,
        config=CHART_CONFIG,
    )


# ==========================================================
# EMPTY FIGURE
# ==========================================================

def empty_chart(
    message: str = "No data available"
) -> go.Figure:
    """
    Return an empty placeholder chart.
    """

    fig = go.Figure()

    fig.add_annotation(

        text=message,

        showarrow=False,

        font=dict(
            size=18,
        ),

        x=0.5,
        y=0.5,

        xref="paper",
        yref="paper",
    )

    fig.update_xaxes(
        visible=False,
    )

    fig.update_yaxes(
        visible=False,
    )

    fig.update_layout(
        height=DEFAULT_CHART_HEIGHT,
    )

    return fig


# ==========================================================
# COLOR HELPER
# ==========================================================

def get_colors(
    n: Optional[int] = None,
):
    """
    Return dashboard color palette.
    """

    if n is None:
        return CHART_COLORS

    return CHART_COLORS[:n]


# ==========================================================
# AXIS FORMATTER
# ==========================================================

def update_axis_titles(
    fig: go.Figure,
    *,
    x_title: Optional[str] = None,
    y_title: Optional[str] = None,
) -> go.Figure:
    """
    Update chart axis titles.
    """

    fig.update_xaxes(
        title=x_title
    )

    fig.update_yaxes(
        title=y_title
    )

    return fig


# ==========================================================
# TITLE HELPER
# ==========================================================

def update_title(
    fig: go.Figure,
    title: str,
) -> go.Figure:
    """
    Update figure title.
    """

    fig.update_layout(
        title=title,
    )

    return fig
# ==========================================================
# LINE CHART
# ==========================================================

def line_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    *,
    color: Optional[str] = None,
    title: Optional[str] = None,
    markers: bool = False,
    height: int = DEFAULT_CHART_HEIGHT,
) -> go.Figure:
    """
    Create a reusable line chart.
    """

    _validate_dataframe(df)
    _validate_columns(df, [x, y])

    if color:
        _validate_columns(df, [color])

    fig = px.line(
        df,
        x=x,
        y=y,
        color=color,
        markers=markers,
        color_discrete_sequence=get_colors(),
    )

    return _apply_layout(
        fig,
        title=title,
        height=height,
    )


# ==========================================================
# BAR CHART
# ==========================================================

def bar_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    *,
    color: Optional[str] = None,
    title: Optional[str] = None,
    text_auto: bool = False,
    height: int = DEFAULT_CHART_HEIGHT,
) -> go.Figure:
    """
    Create a reusable vertical bar chart.
    """

    _validate_dataframe(df)
    _validate_columns(df, [x, y])

    if color:
        _validate_columns(df, [color])

    fig = px.bar(
        df,
        x=x,
        y=y,
        color=color,
        text_auto=text_auto,
        color_discrete_sequence=get_colors(),
    )

    return _apply_layout(
        fig,
        title=title,
        height=height,
    )


# ==========================================================
# HORIZONTAL BAR CHART
# ==========================================================

def horizontal_bar_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    *,
    color: Optional[str] = None,
    title: Optional[str] = None,
    text_auto: bool = False,
    height: int = DEFAULT_CHART_HEIGHT,
) -> go.Figure:
    """
    Create a reusable horizontal bar chart.
    """

    _validate_dataframe(df)
    _validate_columns(df, [x, y])

    if color:
        _validate_columns(df, [color])

    fig = px.bar(
        df,
        x=x,
        y=y,
        color=color,
        orientation="h",
        text_auto=text_auto,
        color_discrete_sequence=get_colors(),
    )

    return _apply_layout(
        fig,
        title=title,
        height=height,
    )


# ==========================================================
# AREA CHART
# ==========================================================

def area_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    *,
    color: Optional[str] = None,
    title: Optional[str] = None,
    height: int = DEFAULT_CHART_HEIGHT,
) -> go.Figure:
    """
    Create a reusable area chart.
    """

    _validate_dataframe(df)
    _validate_columns(df, [x, y])

    if color:
        _validate_columns(df, [color])

    fig = px.area(
        df,
        x=x,
        y=y,
        color=color,
        color_discrete_sequence=get_colors(),
    )

    return _apply_layout(
        fig,
        title=title,
        height=height,
    )


# ==========================================================
# SCATTER PLOT
# ==========================================================

def scatter_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    *,
    color: Optional[str] = None,
    size: Optional[str] = None,
    hover_name: Optional[str] = None,
    title: Optional[str] = None,
    height: int = DEFAULT_CHART_HEIGHT,
) -> go.Figure:
    """
    Create a reusable scatter chart.
    """

    _validate_dataframe(df)
    _validate_columns(df, [x, y])

    required = []

    if color:
        required.append(color)

    if size:
        required.append(size)

    if hover_name:
        required.append(hover_name)

    if required:
        _validate_columns(df, required)

    fig = px.scatter(
        df,
        x=x,
        y=y,
        color=color,
        size=size,
        hover_name=hover_name,
        color_discrete_sequence=get_colors(),
    )

    return _apply_layout(
        fig,
        title=title,
        height=height,
    )
# ==========================================================
# HISTOGRAM
# ==========================================================

def histogram(
    df: pd.DataFrame,
    x: str,
    *,
    color: Optional[str] = None,
    nbins: int = 30,
    title: Optional[str] = None,
    height: int = DEFAULT_CHART_HEIGHT,
) -> go.Figure:
    """
    Create a reusable histogram.
    """

    _validate_dataframe(df)
    _validate_columns(df, [x])

    if color:
        _validate_columns(df, [color])

    fig = px.histogram(
        df,
        x=x,
        color=color,
        nbins=nbins,
        color_discrete_sequence=get_colors(),
    )

    return _apply_layout(
        fig,
        title=title,
        height=height,
    )


# ==========================================================
# BOX PLOT
# ==========================================================

def box_plot(
    df: pd.DataFrame,
    x: Optional[str],
    y: str,
    *,
    color: Optional[str] = None,
    points: str = "outliers",
    title: Optional[str] = None,
    height: int = DEFAULT_CHART_HEIGHT,
) -> go.Figure:
    """
    Create a reusable box plot.
    """

    _validate_dataframe(df)

    required = [y]

    if x:
        required.append(x)

    if color:
        required.append(color)

    _validate_columns(df, required)

    fig = px.box(
        df,
        x=x,
        y=y,
        color=color,
        points=points,
        color_discrete_sequence=get_colors(),
    )

    return _apply_layout(
        fig,
        title=title,
        height=height,
    )


# ==========================================================
# VIOLIN PLOT
# ==========================================================

def violin_plot(
    df: pd.DataFrame,
    x: Optional[str],
    y: str,
    *,
    color: Optional[str] = None,
    box: bool = True,
    points: bool = False,
    title: Optional[str] = None,
    height: int = DEFAULT_CHART_HEIGHT,
) -> go.Figure:
    """
    Create a reusable violin plot.
    """

    _validate_dataframe(df)

    required = [y]

    if x:
        required.append(x)

    if color:
        required.append(color)

    _validate_columns(df, required)

    fig = px.violin(
        df,
        x=x,
        y=y,
        color=color,
        box=box,
        points="all" if points else False,
        color_discrete_sequence=get_colors(),
    )

    return _apply_layout(
        fig,
        title=title,
        height=height,
    )


# ==========================================================
# DENSITY HEATMAP
# ==========================================================

def density_heatmap(
    df: pd.DataFrame,
    x: str,
    y: str,
    *,
    title: Optional[str] = None,
    height: int = DEFAULT_CHART_HEIGHT,
) -> go.Figure:
    """
    Create a density heatmap.
    """

    _validate_dataframe(df)
    _validate_columns(df, [x, y])

    fig = px.density_heatmap(
        df,
        x=x,
        y=y,
    )

    return _apply_layout(
        fig,
        title=title,
        height=height,
    )


# ==========================================================
# CORRELATION HEATMAP
# ==========================================================

def correlation_heatmap(
    df: pd.DataFrame,
    *,
    title: str = "Correlation Matrix",
    height: int = DEFAULT_CHART_HEIGHT,
) -> go.Figure:
    """
    Generate a correlation heatmap for numeric columns.
    """

    _validate_dataframe(df)

    numeric_df = df.select_dtypes(include="number")

    if numeric_df.shape[1] < 2:
        raise ValueError(
            "At least two numeric columns are required."
        )

    corr = numeric_df.corr(numeric_only=True)

    fig = px.imshow(
        corr,
        text_auto=".2f",
        aspect="auto",
        color_continuous_scale="RdBu_r",
        zmin=-1,
        zmax=1,
    )

    return _apply_layout(
        fig,
        title=title,
        height=height,
    )
# ==========================================================
# PIE CHART
# ==========================================================

def pie_chart(
    df: pd.DataFrame,
    names: str,
    values: str,
    *,
    title: Optional[str] = None,
    hole: float = 0.0,
    height: int = DEFAULT_CHART_HEIGHT,
) -> go.Figure:
    """
    Create a reusable pie chart.
    """

    _validate_dataframe(df)
    _validate_columns(df, [names, values])

    fig = px.pie(
        df,
        names=names,
        values=values,
        hole=hole,
        color_discrete_sequence=get_colors(),
    )

    fig.update_traces(
        textposition="inside",
        textinfo="percent+label",
    )

    return _apply_layout(
        fig,
        title=title,
        height=height,
    )


# ==========================================================
# DONUT CHART
# ==========================================================

def donut_chart(
    df: pd.DataFrame,
    names: str,
    values: str,
    *,
    title: Optional[str] = None,
    height: int = DEFAULT_CHART_HEIGHT,
) -> go.Figure:
    """
    Create a reusable donut chart.
    """

    return pie_chart(
        df=df,
        names=names,
        values=values,
        hole=0.55,
        title=title,
        height=height,
    )


# ==========================================================
# TREEMAP
# ==========================================================

def treemap(
    df: pd.DataFrame,
    path: list[str],
    values: str,
    *,
    color: Optional[str] = None,
    title: Optional[str] = None,
    height: int = DEFAULT_CHART_HEIGHT,
) -> go.Figure:
    """
    Create a reusable treemap.
    """

    _validate_dataframe(df)

    required = path + [values]

    if color:
        required.append(color)

    _validate_columns(df, required)

    fig = px.treemap(
        df,
        path=path,
        values=values,
        color=color,
        color_continuous_scale="Blues",
    )

    return _apply_layout(
        fig,
        title=title,
        height=height,
    )


# ==========================================================
# SUNBURST
# ==========================================================

def sunburst_chart(
    df: pd.DataFrame,
    path: list[str],
    values: str,
    *,
    title: Optional[str] = None,
    height: int = DEFAULT_CHART_HEIGHT,
) -> go.Figure:
    """
    Create a reusable sunburst chart.
    """

    _validate_dataframe(df)

    required = path + [values]

    _validate_columns(df, required)

    fig = px.sunburst(
        df,
        path=path,
        values=values,
        color_discrete_sequence=get_colors(),
    )

    return _apply_layout(
        fig,
        title=title,
        height=height,
    )


# ==========================================================
# FUNNEL CHART
# ==========================================================

def funnel_chart(
    df: pd.DataFrame,
    stage: str,
    value: str,
    *,
    title: Optional[str] = None,
    height: int = DEFAULT_CHART_HEIGHT,
) -> go.Figure:
    """
    Create a reusable funnel chart.
    """

    _validate_dataframe(df)
    _validate_columns(df, [stage, value])

    fig = go.Figure(
        go.Funnel(
            y=df[stage],
            x=df[value],
            textinfo="value+percent initial",
            marker=dict(
                color=get_colors(len(df))
            ),
        )
    )

    return _apply_layout(
        fig,
        title=title,
        height=height,
    )
# ==========================================================
# GAUGE CHART
# ==========================================================

def gauge_chart(
    value: float,
    *,
    title: str = "",
    min_value: float = 0,
    max_value: float = 100,
    suffix: str = "%",
    height: int = DEFAULT_CHART_HEIGHT,
) -> go.Figure:
    """
    Create a KPI gauge chart.
    """

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=value,
            number={"suffix": suffix},
            title={"text": title},
            gauge={
                "axis": {
                    "range": [min_value, max_value]
                },
                "bar": {
                    "thickness": 0.35
                },
                "steps": [
                    {
                        "range": [min_value, max_value * 0.5],
                        "color": "#EF4444",
                    },
                    {
                        "range": [max_value * 0.5, max_value * 0.8],
                        "color": "#F59E0B",
                    },
                    {
                        "range": [max_value * 0.8, max_value],
                        "color": "#22C55E",
                    },
                ],
            },
        )
    )

    return _apply_layout(
        fig,
        title=title,
        height=height,
    )


# ==========================================================
# WATERFALL CHART
# ==========================================================

def waterfall_chart(
    labels: list,
    values: list,
    *,
    title: str = "",
    height: int = DEFAULT_CHART_HEIGHT,
) -> go.Figure:
    """
    Create a waterfall chart.
    """

    fig = go.Figure(
        go.Waterfall(
            x=labels,
            y=values,
            measure=["relative"] * len(values),
        )
    )

    return _apply_layout(
        fig,
        title=title,
        height=height,
    )


# ==========================================================
# BUBBLE CHART
# ==========================================================

def bubble_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    size: str,
    *,
    color: Optional[str] = None,
    hover_name: Optional[str] = None,
    title: Optional[str] = None,
    height: int = DEFAULT_CHART_HEIGHT,
) -> go.Figure:
    """
    Create a reusable bubble chart.
    """

    required = [x, y, size]

    if color:
        required.append(color)

    if hover_name:
        required.append(hover_name)

    _validate_dataframe(df)
    _validate_columns(df, required)

    fig = px.scatter(
        df,
        x=x,
        y=y,
        size=size,
        color=color,
        hover_name=hover_name,
        size_max=55,
        color_discrete_sequence=get_colors(),
    )

    return _apply_layout(
        fig,
        title=title,
        height=height,
    )


# ==========================================================
# EXPORT IMAGE
# ==========================================================

def save_chart(
    fig: go.Figure,
    filename: str,
    width: int = 1400,
    height: int = 800,
):
    """
    Save chart as PNG.

    Requires:
    pip install kaleido
    """

    fig.write_image(
        filename,
        width=width,
        height=height,
    )


# ==========================================================
# EXPORT HTML
# ==========================================================

def save_html(
    fig: go.Figure,
    filename: str,
):
    """
    Export chart as standalone HTML.
    """

    fig.write_html(filename)


# ==========================================================
# MODULE EXPORTS
# ==========================================================

__all__ = [

    # Basic Charts
    "line_chart",
    "bar_chart",
    "horizontal_bar_chart",
    "area_chart",
    "scatter_chart",

    # Distribution
    "histogram",
    "box_plot",
    "violin_plot",
    "density_heatmap",
    "correlation_heatmap",

    # Business
    "pie_chart",
    "donut_chart",
    "treemap",
    "sunburst_chart",
    "funnel_chart",

    # Advanced
    "bubble_chart",
    "waterfall_chart",
    "gauge_chart",

    # Utilities
    "render_chart",
    "save_chart",
    "save_html",
]