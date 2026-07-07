"""
=========================================================
RetailPulse
Executive Dashboard
=========================================================

Home Dashboard

Author : Junaid
Project : RetailPulse
"""

from __future__ import annotations

import streamlit as st
import pandas as pd
import numpy as np

# ==========================================================
# PROJECT MODULES
# ==========================================================

from src.styles import load_css
from src.theme import initialize_theme
from src.sidebar import render_sidebar

from src.layout import (
    page_header,
    section_header,
    footer,
)

from src.kpi import kpi_row

from src.charts import (
    line_chart,
    bar_chart,
    donut_chart,
    horizontal_bar_chart,
    gauge_chart,
    render_chart,
)

from src.data_loader import (
    load_dashboard_data,
)

from src.utils import (
    dataframe_to_csv,
    current_timestamp,
)

# ==========================================================
# PAGE INITIALIZATION
# ==========================================================

st.set_page_config(
    page_title="RetailPulse | Executive Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

initialize_theme()
load_css()

render_sidebar()

# ==========================================================
# LOAD DATASETS
# ==========================================================

try:

    datasets = load_dashboard_data()

except Exception as e:

    st.error("Unable to load dashboard datasets.")

    st.exception(e)

    st.stop()

inventory_kpis = datasets["inventory_kpis"]

customer_segments = datasets["customer_segments"]

customer_rfm = datasets["customer_rfm"]

inventory_optimization = datasets["inventory_optimization"]

inventory_recommendations = datasets["inventory_recommendations"]

sales_forecast = datasets["sales_forecast"]

abc_analysis = datasets["abc_analysis"]

abc_xyz_matrix = datasets["abc_xyz_matrix"]

xyz_analysis = datasets["xyz_analysis"]

segment_summary = datasets["segment_summary"]

churn_importance = datasets["churn_feature_importance"]

online_processed = datasets["online_processed"]

rossmann_processed = datasets["rossmann_processed"]

# ==========================================================
# SESSION STATE
# ==========================================================

st.session_state["dashboard_loaded"] = True

# Sidebar dataset indicator
st.session_state["df"] = inventory_kpis

# ==========================================================
# SAFE KPI HELPERS
# ==========================================================

def first_numeric(df: pd.DataFrame):
    """
    Returns first numeric value from dataframe.
    """

    if df.empty:
        return 0

    numeric = df.select_dtypes(include="number")

    if numeric.empty:
        return 0

    return numeric.iloc[0, 0]


def find_metric(df: pd.DataFrame, keywords):
    """
    Search dataframe for a metric row.

    Works with inventory_kpis.csv irrespective
    of column names.
    """

    if df.empty:
        return None

    cols = df.columns.tolist()

    for col in cols:

        if df[col].dtype == object:

            for keyword in keywords:

                mask = (
                    df[col]
                    .astype(str)
                    .str.lower()
                    .str.contains(keyword.lower())
                )

                if mask.any():

                    row = df[mask].iloc[0]

                    nums = row.select_dtypes(include="number")

                    if len(nums) > 0:
                        return nums.iloc[0]

    return None


# ==========================================================
# EXECUTIVE KPI VALUES
# ==========================================================

total_sales = (
    find_metric(inventory_kpis, ["sales", "revenue"])
    or first_numeric(inventory_kpis)
)

total_profit = (
    find_metric(inventory_kpis, ["profit"])
    or 0
)

orders = (
    find_metric(inventory_kpis, ["orders"])
    or len(online_processed)
)

customers = (
    customer_segments.shape[0]
)

forecast_points = len(sales_forecast)

inventory_items = len(inventory_optimization)

abc_products = len(abc_analysis)

# ==========================================================
# PAGE HEADER
# ==========================================================

page_header(
    title="RetailPulse Executive Dashboard",
    subtitle="AI-Powered Retail Analytics & Decision Intelligence",
    icon="📊",
)

st.markdown(
"""
Welcome to **RetailPulse**, an end-to-end AI-powered retail analytics platform.

This dashboard combines machine learning outputs from customer segmentation,
demand forecasting, churn prediction, inventory optimization, and ABC-XYZ
analysis into a unified executive view for data-driven business decisions.
"""
)

st.divider()
# ==========================================================
# EXECUTIVE KPI DASHBOARD
# ==========================================================

section_header(
    "Executive Overview",
    "High-level business performance indicators generated from processed datasets."
)

# ----------------------------------------------------------
# Additional KPIs
# ----------------------------------------------------------

forecast_accuracy = 0

if not sales_forecast.empty:

    numeric_cols = sales_forecast.select_dtypes(include="number").columns

    for col in numeric_cols:

        if "accuracy" in col.lower():

            forecast_accuracy = float(
                sales_forecast[col].mean()
            )

            break

inventory_health = 0

if not inventory_recommendations.empty:

    numeric_cols = inventory_recommendations.select_dtypes(include="number").columns

    if len(numeric_cols):

        inventory_health = float(
            inventory_recommendations[numeric_cols[0]].mean()
        )

# ----------------------------------------------------------
# KPI Cards
# ----------------------------------------------------------

cards = [

    {
        "title": "Total Revenue",
        "value": total_sales,
        "icon": "💰",
        "type": "currency",
    },

    {
        "title": "Total Profit",
        "value": total_profit,
        "icon": "📈",
        "type": "currency",
    },

    {
        "title": "Customers",
        "value": customers,
        "icon": "👥",
    },

    {
        "title": "Orders",
        "value": orders,
        "icon": "🛒",
    },

    {
        "title": "Inventory Items",
        "value": inventory_items,
        "icon": "📦",
    },

    {
        "title": "Forecast Records",
        "value": forecast_points,
        "icon": "📊",
    },

]

kpi_row(cards)

st.write("")

# ----------------------------------------------------------
# Secondary Metrics
# ----------------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(

        "ABC Products",

        f"{abc_products:,}"

    )

with col2:

    st.metric(

        "Customer Segments",

        f"{customer_segments.shape[0]:,}"

    )

with col3:

    st.metric(

        "Forecast Accuracy",

        f"{forecast_accuracy:.2f}%"

        if forecast_accuracy

        else "N/A"

    )

with col4:

    st.metric(

        "Inventory Health",

        f"{inventory_health:.1f}"

        if inventory_health

        else "N/A"

    )

st.divider()

# ==========================================================
# DASHBOARD SNAPSHOT
# ==========================================================

section_header(
    "Dashboard Snapshot",
    "Overall operational performance at a glance."
)

left, right = st.columns([2, 1])

# ----------------------------------------------------------
# LEFT PANEL
# ----------------------------------------------------------

with left:

    st.markdown(
        """
### 🚀 Executive Summary

RetailPulse combines multiple machine learning modules into a
single executive dashboard.

The dashboard provides:

- Customer Segmentation
- Demand Forecasting
- Inventory Optimization
- ABC–XYZ Analysis
- Churn Prediction
- Executive Business Insights

Use the navigation menu to explore each analytical module in
greater detail.
"""
    )

# ----------------------------------------------------------
# RIGHT PANEL
# ----------------------------------------------------------

with right:

    score = 0

    completed = 0

    if not customer_segments.empty:
        completed += 1

    if not sales_forecast.empty:
        completed += 1

    if not inventory_optimization.empty:
        completed += 1

    if not abc_analysis.empty:
        completed += 1

    if not churn_importance.empty:
        completed += 1

    score = (completed / 5) * 100

    fig = gauge_chart(

        score,

        title="Dashboard Readiness",

        min_value=0,

        max_value=100,

        suffix="%",

    )

    render_chart(fig)

st.divider()
# ==========================================================
# SALES FORECAST ANALYTICS
# ==========================================================

section_header(
    "Sales Forecast Analytics",
    "Demand forecasting trends and revenue projections."
)

forecast_df = sales_forecast.copy()

# ----------------------------------------------------------
# Identify Forecast Columns
# ----------------------------------------------------------

date_col = None
value_col = None

for col in forecast_df.columns:

    lower = col.lower()

    if date_col is None and any(
        key in lower
        for key in [
            "date",
            "month",
            "ds",
            "time"
        ]
    ):
        date_col = col

    if value_col is None and any(
        key in lower
        for key in [
            "forecast",
            "prediction",
            "sales",
            "yhat",
            "predicted"
        ]
    ):
        value_col = col

if value_col is None:

    numeric = forecast_df.select_dtypes(include="number").columns

    if len(numeric):
        value_col = numeric[0]

if date_col is None:

    forecast_df["Period"] = range(
        1,
        len(forecast_df) + 1
    )

    date_col = "Period"

# ----------------------------------------------------------
# Forecast Trend
# ----------------------------------------------------------

left, right = st.columns([2, 1])

with left:

    if value_col:

        fig = line_chart(

            forecast_df,

            x=date_col,

            y=value_col,

            title="Sales Forecast Trend",

            markers=True,

        )

        render_chart(fig)

    else:

        st.info("Forecast values unavailable.")

with right:

    if value_col:

        summary = pd.DataFrame({

            "Metric": [

                "Minimum",

                "Average",

                "Maximum",

                "Forecast Points"

            ],

            "Value": [

                round(
                    forecast_df[value_col].min(),
                    2,
                ),

                round(
                    forecast_df[value_col].mean(),
                    2,
                ),

                round(
                    forecast_df[value_col].max(),
                    2,
                ),

                len(forecast_df)

            ]

        })

        st.dataframe(

            summary,

            use_container_width=True,

            hide_index=True,

        )

st.write("")

# ----------------------------------------------------------
# Forecast Distribution
# ----------------------------------------------------------

if value_col:

    distribution = (

        forecast_df[value_col]

        .round(0)

        .value_counts()

        .reset_index()

    )

    distribution.columns = [

        "Forecast",

        "Count"

    ]

    col1, col2 = st.columns(2)

    with col1:

        fig = bar_chart(

            distribution,

            x="Forecast",

            y="Count",

            title="Forecast Distribution",

        )

        render_chart(fig)

    with col2:

        fig = donut_chart(

            distribution.head(6),

            names="Forecast",

            values="Count",

            title="Top Forecast Categories",

        )

        render_chart(fig)

st.divider()

# ==========================================================
# SALES SUMMARY
# ==========================================================

section_header(

    "Forecast Insights",

    "Automatically generated observations."

)

if value_col:

    highest = forecast_df.loc[
        forecast_df[value_col].idxmax()
    ]

    lowest = forecast_df.loc[
        forecast_df[value_col].idxmin()
    ]

    avg_sales = forecast_df[value_col].mean()

    col1, col2, col3 = st.columns(3)

    with col1:

        st.success(

            f"""
### 📈 Highest Forecast

**{highest[value_col]:,.2f}**

Period:

**{highest[date_col]}**
"""
        )

    with col2:

        st.warning(

            f"""
### 📉 Lowest Forecast

**{lowest[value_col]:,.2f}**

Period:

**{lowest[date_col]}**
"""
        )

    with col3:

        st.info(

            f"""
### 📊 Average Forecast

**{avg_sales:,.2f}**

Across

**{len(forecast_df):,} periods**
"""
        )

else:

    st.info(
        "Forecast summary unavailable."
    )

st.divider()
# ==========================================================
# CUSTOMER ANALYTICS
# ==========================================================

section_header(
    "Customer Analytics",
    "Customer segmentation and RFM insights."
)

segment_df = customer_segments.copy()
rfm_df = customer_rfm.copy()

# ----------------------------------------------------------
# Detect Columns
# ----------------------------------------------------------

segment_col = None

for col in segment_df.columns:

    if any(k in col.lower() for k in [
        "segment",
        "cluster",
        "label",
        "class"
    ]):
        segment_col = col
        break

customer_col = None

for col in segment_df.columns:

    if any(k in col.lower() for k in [
        "customer",
        "customer id",
        "id"
    ]):
        customer_col = col
        break

# ----------------------------------------------------------
# Segment Distribution
# ----------------------------------------------------------

if segment_col:

    segment_counts = (

        segment_df[segment_col]

        .value_counts()

        .reset_index()

    )

    segment_counts.columns = [

        "Segment",

        "Customers"

    ]

    col1, col2 = st.columns([2, 1])

    with col1:

        fig = bar_chart(

            segment_counts,

            x="Segment",

            y="Customers",

            title="Customer Segment Distribution",

            text_auto=True,

        )

        render_chart(fig)

    with col2:

        fig = donut_chart(

            segment_counts,

            names="Segment",

            values="Customers",

            title="Customer Mix",

        )

        render_chart(fig)

else:

    st.info("Customer segmentation columns not detected.")

st.write("")

# ----------------------------------------------------------
# Segment Summary
# ----------------------------------------------------------

if segment_col:

    best_segment = segment_counts.iloc[0]

    least_segment = segment_counts.iloc[-1]

    c1, c2 = st.columns(2)

    with c1:

        st.success(

            f"""
### 🏆 Largest Customer Segment

**{best_segment['Segment']}**

Customers:

**{best_segment['Customers']:,}**
"""
        )

    with c2:

        st.warning(

            f"""
### 📉 Smallest Customer Segment

**{least_segment['Segment']}**

Customers:

**{least_segment['Customers']:,}**
"""
        )

st.divider()

# ==========================================================
# RFM ANALYSIS
# ==========================================================

section_header(

    "Customer RFM Analysis",

    "Recency • Frequency • Monetary"

)

rfm_numeric = rfm_df.select_dtypes(include="number")

if not rfm_numeric.empty:

    averages = (

        rfm_numeric.mean()

        .round(2)

        .reset_index()

    )

    averages.columns = [

        "Metric",

        "Average"

    ]

    left, right = st.columns([2, 1])

    with left:

        fig = horizontal_bar_chart(

            averages,

            x="Average",

            y="Metric",

            title="Average RFM Metrics",

            text_auto=True,

        )

        render_chart(fig)

    with right:

        st.dataframe(

            averages,

            use_container_width=True,

            hide_index=True,

        )

else:

    st.info("No numeric RFM metrics available.")

st.write("")

# ----------------------------------------------------------
# Customer Health Metrics
# ----------------------------------------------------------

metric1, metric2, metric3, metric4 = st.columns(4)

with metric1:

    st.metric(

        "Customers",

        f"{len(segment_df):,}"

    )

with metric2:

    st.metric(

        "Segments",

        f"{segment_df[segment_col].nunique():,}"

        if segment_col else "N/A"

    )

with metric3:

    st.metric(

        "RFM Records",

        f"{len(rfm_df):,}"

    )

with metric4:

    st.metric(

        "Numeric Metrics",

        f"{len(rfm_numeric.columns):,}"

    )

st.divider()

# ==========================================================
# CUSTOMER INSIGHTS
# ==========================================================

section_header(

    "Customer Insights",

    "AI-generated customer observations."

)

col1, col2 = st.columns(2)

with col1:

    st.info(
        """
### 👥 Customer Segmentation

RetailPulse automatically clusters customers
into meaningful business groups.

Use the Customer Segmentation module
for detailed exploration.
"""
    )

    st.success(
        """
### 🎯 Marketing Opportunity

High-value customer segments should receive

• Loyalty rewards

• Personalized offers

• Premium campaigns
"""
    )

with col2:

    st.warning(
        """
### ⚠ Retention Strategy

Customers with

• Low Frequency

• High Recency

should be targeted with retention campaigns.
"""
    )

    st.success(
        """
### 💎 Business Value

RFM analysis enables

• Better targeting

• Higher customer lifetime value

• Improved campaign ROI
"""
    )

st.divider()
# ==========================================================
# INVENTORY OPTIMIZATION
# ==========================================================

section_header(
    "Inventory Optimization",
    "Inventory health, ABC analysis and optimization insights."
)

inventory_df = inventory_optimization.copy()
recommend_df = inventory_recommendations.copy()
abc_df = abc_analysis.copy()
abcxyz_df = abc_xyz_matrix.copy()

# ----------------------------------------------------------
# Inventory KPIs
# ----------------------------------------------------------

inventory_value = 0
reorder_items = len(recommend_df)
optimized_items = len(inventory_df)

if not inventory_df.empty:

    numeric_cols = inventory_df.select_dtypes(include="number").columns

    if len(numeric_cols):
        inventory_value = inventory_df[numeric_cols[0]].sum()

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Inventory Records",
        f"{optimized_items:,}"
    )

with col2:

    st.metric(
        "Recommendations",
        f"{reorder_items:,}"
    )

with col3:

    st.metric(
        "Inventory Value",
        f"₹{inventory_value:,.0f}"
    )

st.write("")

# ----------------------------------------------------------
# ABC Distribution
# ----------------------------------------------------------

abc_class = None

for col in abc_df.columns:

    if any(x in col.lower() for x in [
        "abc",
        "class",
        "category"
    ]):

        abc_class = col
        break

if abc_class:

    abc_summary = (

        abc_df[abc_class]

        .value_counts()

        .reset_index()

    )

    abc_summary.columns = [

        "Class",

        "Products"

    ]

    left, right = st.columns(2)

    with left:

        fig = bar_chart(

            abc_summary,

            x="Class",

            y="Products",

            title="ABC Classification",

            text_auto=True,

        )

        render_chart(fig)

    with right:

        fig = donut_chart(

            abc_summary,

            names="Class",

            values="Products",

            title="ABC Distribution",

        )

        render_chart(fig)

else:

    st.info("ABC classification unavailable.")

st.write("")

# ----------------------------------------------------------
# XYZ Matrix
# ----------------------------------------------------------

if not abcxyz_df.empty:

    matrix_cols = abcxyz_df.columns.tolist()

    numeric_cols = abcxyz_df.select_dtypes(include="number").columns

    if len(matrix_cols) >= 2 and len(numeric_cols):

        fig = horizontal_bar_chart(

            abcxyz_df.sort_values(
                numeric_cols[0],
                ascending=False
            ).head(10),

            x=numeric_cols[0],

            y=matrix_cols[0],

            title="ABC–XYZ Matrix Overview",

            text_auto=True,

        )

        render_chart(fig)

st.divider()

# ==========================================================
# INVENTORY RECOMMENDATIONS
# ==========================================================

section_header(
    "Inventory Recommendations",
    "Actionable inventory optimization suggestions."
)

if not recommend_df.empty:

    st.dataframe(

        recommend_df.head(15),

        use_container_width=True,

        hide_index=True,

    )

else:

    st.info("No inventory recommendations available.")

st.write("")

# ----------------------------------------------------------
# Dashboard Health
# ----------------------------------------------------------

health_score = 100

if reorder_items > 0:

    deduction = min(
        reorder_items * 2,
        60
    )

    health_score -= deduction

fig = gauge_chart(

    health_score,

    title="Inventory Health",

    min_value=0,

    max_value=100,

    suffix="%",

)

render_chart(fig)

st.divider()

# ==========================================================
# INVENTORY INSIGHTS
# ==========================================================

section_header(
    "Inventory Insights",
    "AI-generated inventory recommendations."
)

col1, col2 = st.columns(2)

with col1:

    st.success(
        f"""
### 📦 Inventory Overview

• Optimized Products : **{optimized_items:,}**

• ABC Products : **{len(abc_df):,}**

• Recommendations : **{reorder_items:,}**
"""
    )

    st.info(
        """
### 💡 Suggested Actions

• Prioritize A-Class inventory

• Review fast-moving products

• Reduce overstocked inventory

• Automate reorder planning
"""
    )

with col2:

    st.warning(
        """
### ⚠ Risk Indicators

Monitor products with:

• Low turnover

• High holding cost

• Demand uncertainty

• Frequent stockouts
"""
    )

    st.success(
        """
### 🚀 Expected Benefits

✓ Lower inventory cost

✓ Better service level

✓ Reduced stockouts

✓ Improved cash flow
"""
    )

st.divider()
# ==========================================================
# CHURN ANALYTICS
# ==========================================================

section_header(
    "Customer Churn Analytics",
    "Key drivers influencing customer churn."
)

churn_df = churn_importance.copy()

if not churn_df.empty:

    numeric_cols = churn_df.select_dtypes(include="number").columns
    object_cols = churn_df.select_dtypes(include="object").columns

    feature_col = object_cols[0] if len(object_cols) else churn_df.columns[0]

    importance_col = (
        numeric_cols[0]
        if len(numeric_cols)
        else churn_df.columns[-1]
    )

    top_features = (
        churn_df
        .sort_values(
            importance_col,
            ascending=False
        )
        .head(10)
    )

    fig = horizontal_bar_chart(
        top_features,
        x=importance_col,
        y=feature_col,
        title="Top Churn Drivers",
        text_auto=True,
    )

    render_chart(fig)

else:

    st.info("Churn feature importance not available.")

st.divider()

# ==========================================================
# EXECUTIVE INSIGHTS
# ==========================================================

section_header(
    "Executive Business Insights",
    "AI-generated recommendations from all analytical modules."
)

left, right = st.columns(2)

with left:

    st.success(
        f"""
### 📈 Revenue Outlook

• Forecast Records : **{forecast_points:,}**

• Customer Base : **{customers:,}**

• Inventory Records : **{inventory_items:,}**

RetailPulse predicts demand and supports
proactive business planning.
"""
    )

    st.info(
        f"""
### 👥 Customer Intelligence

• Segments Identified : **{customer_segments.shape[0]:,}**

• RFM Records : **{customer_rfm.shape[0]:,}**

Use customer segmentation for targeted
marketing campaigns.
"""
    )

    st.success(
        f"""
### 📦 Inventory Intelligence

ABC Products Analysed :

**{abc_products:,}**

Recommendations Generated :

**{len(recommend_df):,}**
"""
    )

with right:

    st.warning(
        """
### ⚠ Executive Recommendations

• Increase inventory for A-class products

• Reduce excess stock of slow movers

• Improve customer retention strategies

• Monitor forecast deviations weekly

• Personalize marketing campaigns
"""
    )

    st.info(
        """
### 🚀 Expected Business Benefits

✓ Better Forecast Accuracy

✓ Reduced Inventory Cost

✓ Higher Customer Retention

✓ Increased Profitability

✓ Data-driven Decision Making
"""
    )

st.divider()

# ==========================================================
# DASHBOARD SUMMARY
# ==========================================================

section_header(
    "Dashboard Summary",
    "Current dashboard status."
)

metric1, metric2, metric3, metric4 = st.columns(4)

with metric1:

    st.metric(
        "Datasets",
        len(datasets)
    )

with metric2:

    total_rows = sum(
        len(df)
        for df in datasets.values()
    )

    st.metric(
        "Total Records",
        f"{total_rows:,}"
    )

with metric3:

    st.metric(
        "Modules",
        "6"
    )

with metric4:

    st.metric(
        "Generated",
        current_timestamp()
    )

st.divider()

# ==========================================================
# DOWNLOAD CENTER
# ==========================================================

section_header(
    "Download Center",
    "Export processed datasets."
)

dataset_choice = st.selectbox(

    "Choose Dataset",

    list(datasets.keys())

)

csv = dataframe_to_csv(
    datasets[dataset_choice]
)

st.download_button(

    label=f"📥 Download {dataset_choice}",

    data=csv,

    file_name=f"{dataset_choice}.csv",

    mime="text/csv",

    use_container_width=True,

)

st.write("")

with st.expander("Preview Dataset"):

    st.dataframe(

        datasets[dataset_choice].head(25),

        use_container_width=True,

        hide_index=True,

    )

st.divider()

# ==========================================================
# SYSTEM STATUS
# ==========================================================

section_header(
    "System Health",
    "RetailPulse dashboard diagnostics."
)

status1, status2, status3 = st.columns(3)

with status1:

    st.success("✅ Data Loader")

    st.caption("Operational")

with status2:

    st.success("✅ Dashboard")

    st.caption("Operational")

with status3:

    st.success("✅ ML Pipeline")

    st.caption("Operational")

st.divider()

# ==========================================================
# FOOTER
# ==========================================================

footer()