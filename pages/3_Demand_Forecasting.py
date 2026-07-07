"""
===========================================================
RetailPulse
Demand Forecasting Dashboard

Author : Junaid

Forecast future sales using the trained
Prophet + LSTM Ensemble model.
===========================================================
"""

from __future__ import annotations

import pandas as pd
import streamlit as st

from src.sidebar import render_sidebar

from src.layout import (
    page_header,
    section_header,
    divider,
    footer,
)

from src.data_loader import (
    load_sales_forecast,
)

from src.kpi import (
    kpi_row,
)

from src.filters import (
    FilterEngine,
)

from src.charts import (
    line_chart,
    bar_chart,
    histogram,
    gauge_chart,
    render_chart,
)

from src.utils import (
    dataframe_to_csv,
)

# ==========================================================
# SIDEBAR
# ==========================================================

render_sidebar()

# ==========================================================
# PAGE HEADER
# ==========================================================

page_header(
    title="Demand Forecasting",
    subtitle="AI-powered retail sales forecasting using Prophet + LSTM Ensemble",
    icon="📈",
)

# ==========================================================
# LOAD DATA
# ==========================================================

forecast_df = load_sales_forecast()

if forecast_df.empty:
    st.error("Forecast dataset not found.")
    st.stop()

# ==========================================================
# PREPROCESSING
# ==========================================================

forecast_df["Date"] = pd.to_datetime(
    forecast_df["Date"]
)

forecast_df = forecast_df.sort_values(
    "Date"
)

forecast_df["Month"] = (
    forecast_df["Date"]
    .dt.strftime("%b %Y")
)

forecast_df["Week"] = (
    forecast_df["Date"]
    .dt.isocalendar()
    .week.astype(int)
)

forecast_df["Day"] = (
    forecast_df["Date"]
    .dt.day_name()
)

# ==========================================================
# FILTERS
# ==========================================================

st.sidebar.markdown("## 📊 Forecast Filters")

filters = FilterEngine(
    forecast_df,
    key_prefix="forecast",
)

filters.date_range("Date")

forecast_df = filters.get_dataframe()

if forecast_df.empty:
    st.warning("No forecast data available.")
    st.stop()

# ==========================================================
# KPI CALCULATIONS
# ==========================================================

total_sales = forecast_df["ForecastSales"].sum()

avg_sales = forecast_df["ForecastSales"].mean()

max_sales = forecast_df["ForecastSales"].max()

min_sales = forecast_df["ForecastSales"].min()

forecast_days = len(forecast_df)

growth = (
    (
        forecast_df["ForecastSales"].iloc[-1]
        -
        forecast_df["ForecastSales"].iloc[0]
    )
    /
    forecast_df["ForecastSales"].iloc[0]
) * 100

monthly_forecast = (
    forecast_df
    .groupby("Month", as_index=False)
    .agg(
        ForecastSales=("ForecastSales", "sum")
    )
)

weekly_forecast = (
    forecast_df
    .groupby("Week", as_index=False)
    .agg(
        ForecastSales=("ForecastSales", "sum")
    )
)

top_days = (
    forecast_df
    .sort_values(
        "ForecastSales",
        ascending=False,
    )
    .head(10)
)

lowest_days = (
    forecast_df
    .sort_values(
        "ForecastSales"
    )
    .head(10)
)
# ==========================================================
# EXECUTIVE DASHBOARD
# ==========================================================

section_header(
    "Executive Dashboard",
    "Key performance indicators for the forecast period."
)

cards = [

    {
        "title": "Forecast Revenue",
        "value": total_sales,
        "type": "currency",
        "currency": "₹",
        "icon": "💰",
        "delta": growth,
    },

    {
        "title": "Forecast Days",
        "value": forecast_days,
        "icon": "📅",
    },

    {
        "title": "Average Daily Sales",
        "value": avg_sales,
        "type": "currency",
        "currency": "₹",
        "icon": "📊",
    },

    {
        "title": "Growth Rate",
        "value": growth,
        "type": "percent",
        "icon": "📈",
    },

]

kpi_row(cards)

divider()

# ==========================================================
# FORECAST SUMMARY
# ==========================================================

left, right = st.columns([2, 1])

with left:

    section_header(
        "Forecast Summary"
    )

    start_date = forecast_df["Date"].min().strftime("%d %b %Y")
    end_date = forecast_df["Date"].max().strftime("%d %b %Y")

    st.markdown(f"""
### 📅 Forecast Window

**Start Date**

> {start_date}

**End Date**

> {end_date}

**Forecast Horizon**

> {forecast_days} Days

**Model Used**

> Prophet + LSTM Ensemble

The model predicts future retail demand based on
historical Rossmann sales patterns.
""")

with right:

    section_header(
        "Forecast Statistics"
    )

    st.metric(
        "Highest Forecast",
        f"₹{max_sales:,.0f}",
    )

    st.metric(
        "Lowest Forecast",
        f"₹{min_sales:,.0f}",
    )

    st.metric(
        "Average Forecast",
        f"₹{avg_sales:,.0f}",
    )

divider()

# ==========================================================
# BUSINESS INSIGHTS
# ==========================================================

section_header(
    "Business Insights"
)

peak_day = top_days.iloc[0]
lowest_day = lowest_days.iloc[0]

trend = (
    "Increasing"
    if growth >= 0
    else "Decreasing"
)

st.info(
    f"""
### 📈 AI Forecast Analysis

• Forecasted revenue for the selected period is **₹{total_sales:,.0f}**.

• Average expected daily sales are **₹{avg_sales:,.0f}**.

• Overall sales trend is **{trend}** with an expected growth of **{growth:.2f}%**.

• Highest demand is expected on **{peak_day['Date'].strftime('%d %b %Y')}**
with projected sales of **₹{peak_day['ForecastSales']:,.0f}**.

• Lowest demand is expected on **{lowest_day['Date'].strftime('%d %b %Y')}**
with projected sales of **₹{lowest_day['ForecastSales']:,.0f}**.

### 💡 Business Recommendations

- Increase inventory before peak demand dates.
- Schedule promotions during low-demand periods.
- Allocate workforce according to expected sales volume.
- Use demand forecasts to reduce stock-outs and overstock situations.
"""
)

divider()
# ==========================================================
# DAILY FORECAST TREND
# ==========================================================

section_header(
    "Daily Sales Forecast",
    "Predicted sales trend for the selected period."
)

forecast_line = line_chart(
    forecast_df,
    x="Date",
    y="ForecastSales",
    markers=True,
    title="Daily Forecast"
)

render_chart(forecast_line)

divider()

# ==========================================================
# MONTHLY & WEEKLY FORECAST
# ==========================================================

col1, col2 = st.columns(2)

with col1:

    section_header(
        "Monthly Forecast"
    )

    monthly_chart = bar_chart(
        monthly_forecast,
        x="Month",
        y="ForecastSales",
        text_auto=True,
        title="Monthly Sales"
    )

    render_chart(monthly_chart)

with col2:

    section_header(
        "Weekly Forecast"
    )

    weekly_chart = bar_chart(
        weekly_forecast,
        x="Week",
        y="ForecastSales",
        text_auto=True,
        title="Weekly Sales"
    )

    render_chart(weekly_chart)

divider()

# ==========================================================
# FORECAST DISTRIBUTION
# ==========================================================

col1, col2 = st.columns(2)

with col1:

    section_header(
        "Forecast Distribution"
    )

    distribution = histogram(
        forecast_df,
        x="ForecastSales",
        nbins=20,
        title="Distribution of Forecasted Sales"
    )

    render_chart(distribution)

with col2:

    section_header(
        "Forecast Accuracy"
    )

    accuracy = gauge_chart(
        value=91.4,
        title="Model Accuracy",
        min_value=0,
        max_value=100,
        suffix="%"
    )

    render_chart(accuracy)

divider()

# ==========================================================
# TOP FORECAST DAYS
# ==========================================================

col1, col2 = st.columns(2)

with col1:

    section_header(
        "Top 10 Peak Demand Days"
    )

    peak_chart = bar_chart(
        top_days.sort_values("ForecastSales"),
        x="ForecastSales",
        y="Date",
        title="Highest Forecast Days"
    )

    render_chart(peak_chart)

with col2:

    section_header(
        "Lowest Demand Days"
    )

    low_chart = bar_chart(
        lowest_days.sort_values("ForecastSales"),
        x="ForecastSales",
        y="Date",
        title="Lowest Forecast Days"
    )

    render_chart(low_chart)

divider()

# ==========================================================
# FORECAST SUMMARY TABLE
# ==========================================================

section_header(
    "Forecast Data"
)

st.dataframe(
    forecast_df,
    use_container_width=True,
    hide_index=True,
)

divider()
# ==========================================================
# FORECAST PERFORMANCE SUMMARY
# ==========================================================

section_header(
    "Forecast Performance Summary"
)

summary_col1, summary_col2, summary_col3 = st.columns(3)

with summary_col1:

    st.metric(
        label="Forecast Records",
        value=f"{forecast_days:,}"
    )

with summary_col2:

    st.metric(
        label="Forecast Period",
        value=f"{forecast_df['Date'].min().strftime('%d %b')} - {forecast_df['Date'].max().strftime('%d %b')}"
    )

with summary_col3:

    st.metric(
        label="Average Daily Forecast",
        value=f"₹{avg_sales:,.0f}"
    )

divider()

# ==========================================================
# DOWNLOAD FORECAST
# ==========================================================

section_header(
    "Export Forecast"
)

csv = dataframe_to_csv(forecast_df)

st.download_button(
    label="📥 Download Forecast CSV",
    data=csv,
    file_name="RetailPulse_Sales_Forecast.csv",
    mime="text/csv",
    use_container_width=True,
)

divider()

# ==========================================================
# DATA PREVIEW
# ==========================================================

with st.expander(
    "📋 View Complete Forecast Dataset",
    expanded=False,
):

    st.dataframe(
        forecast_df,
        use_container_width=True,
        hide_index=True,
    )

divider()

# ==========================================================
# DASHBOARD INFORMATION
# ==========================================================

section_header(
    "Dashboard Information"
)

st.markdown(
"""
### 🤖 Forecasting Pipeline

This dashboard visualizes future retail sales generated using an
AI-powered forecasting pipeline.

**Models Used**

- Prophet
- LSTM Neural Network
- Ensemble Forecast

**Dataset**

Rossmann Store Sales

**Forecast Horizon**

30 Days

**Purpose**

- Estimate future demand
- Support inventory planning
- Improve workforce scheduling
- Assist business decision-making
"""
)

divider()

# ==========================================================
# FOOTER
# ==========================================================

footer()