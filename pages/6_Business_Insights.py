"""
=========================================================
RetailPulse - Business Insights
=========================================================

Executive Dashboard

Author : Junaid
"""

from __future__ import annotations

import streamlit as st
import pandas as pd

from src.styles import load_css
from src.theme import initialize_theme

from src.layout import (
    page_header,
    section_header,
    divider,
    footer,
)

from src.kpi import kpi_row

from src.charts import (
    line_chart,
    bar_chart,
    donut_chart,
    treemap,
    render_chart,
)

from src.data_loader import load_dashboard_data


# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------

st.set_page_config(
    page_title="Business Insights",
    page_icon="📊",
    layout="wide",
)

initialize_theme()
load_css()

page_header(
    "Business Insights",
    "Executive overview of RetailPulse",
    "📊",
)
# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

data = load_dashboard_data()

online = data["online_processed"]

rossmann = data["rossmann_processed"]

forecast = data["sales_forecast"]

segments = data["customer_segments"]

rfm = data["customer_rfm"]

segment_summary = data["segment_summary"]

inventory = data["inventory_kpis"]

inventory_opt = data["inventory_optimization"]

inventory_rec = data["inventory_recommendations"]

abc = data["abc_analysis"]

xyz = data["xyz_analysis"]

abcxyz = data["abc_xyz_matrix"]

churn = data["customer_churn_predictions"]

importance = data["churn_feature_importance"]
divider()

section_header(
    "Executive Overview",
    "Overall business performance"
)

total_revenue = online["Revenue"].sum()

customers = online["Customer ID"].nunique()

forecast_revenue = forecast["ForecastSales"].sum()

stores = rossmann["Store"].nunique()

churn_rate = churn["Churn"].mean() * 100

kpi_row(

[
    {
        "title":"Revenue",
        "value":total_revenue,
        "type":"currency",
        "currency":"$",
        "icon":"💰"
    },

    {
        "title":"Customers",
        "value":customers,
        "icon":"👥"
    },

    {
        "title":"Stores",
        "value":stores,
        "icon":"🏪"
    },

    {
        "title":"Forecast",
        "value":forecast_revenue,
        "type":"currency",
        "currency":"$",
        "icon":"📈"
    },

    {
        "title":"Churn",
        "value":churn_rate,
        "type":"percent",
        "icon":"⚠️"
    }

]
)
# ==========================================================
# SALES ANALYTICS
# ==========================================================

divider()

section_header(
    "Sales Analytics",
    "Revenue trends and store performance"
)

online["InvoiceDate"] = pd.to_datetime(
    online["InvoiceDate"],
    errors="coerce"
)

online["Month"] = (
    online["InvoiceDate"]
    .dt.to_period("M")
    .astype(str)
)
monthly_sales = (

    online

    .groupby("Month")["Revenue"]

    .sum()

    .reset_index()
)
top_products = (

    online

    .groupby("Description")["Revenue"]

    .sum()

    .sort_values(ascending=False)

    .head(10)

    .reset_index()
)
store_sales = (

    rossmann

    .groupby("Store")["Sales"]

    .sum()

    .sort_values(ascending=False)

    .head(10)

    .reset_index()
)
country_sales = (

    online

    .groupby("Country")["Revenue"]

    .sum()

    .sort_values(ascending=False)

    .head(10)

    .reset_index()
)
col1, col2 = st.columns(2)

with col1:

    st.subheader("Monthly Revenue")

    fig = line_chart(

        monthly_sales,

        x="Month",

        y="Revenue",

        markers=True,

    )

    render_chart(fig)

with col2:

    st.subheader("Top Products")

    fig = bar_chart(

        top_products,

        x="Description",

        y="Revenue",

        text_auto=True,

    )

    render_chart(fig)
col1, col2 = st.columns(2)

with col1:

    st.subheader("Top Performing Stores")

    fig = bar_chart(

        store_sales,

        x="Store",

        y="Sales",

        text_auto=True,

    )

    render_chart(fig)

with col2:

    st.subheader("Revenue by Country")

    fig = donut_chart(

        country_sales,

        names="Country",

        values="Revenue",

        title="Country Contribution",

    )

    render_chart(fig)
st.subheader("Top Revenue Products")

st.dataframe(

    top_products,

    use_container_width=True,

    hide_index=True,
)
# ==========================================================
# CUSTOMER INTELLIGENCE
# ==========================================================

divider()

section_header(
    "Customer Intelligence",
    "Understand customer behaviour and segment performance"
)
col1, col2, col3, col4 = st.columns(4)

total_customers = rfm["Customer ID"].nunique()

avg_spend = rfm["Monetary"].mean()

avg_frequency = rfm["Frequency"].mean()

avg_recency = rfm["Recency"].mean()

with col1:
    st.metric(
        "Customers",
        f"{total_customers:,}"
    )

with col2:
    st.metric(
        "Average Spend",
        f"${avg_spend:,.2f}"
    )

with col3:
    st.metric(
        "Avg Frequency",
        f"{avg_frequency:.2f}"
    )

with col4:
    st.metric(
        "Avg Recency",
        f"{avg_recency:.1f} Days"
    )
segment_count = (

    segments

    .groupby("Segment")

    .size()

    .reset_index(name="Customers")
)
segment_revenue = (

    segments

    .groupby("Segment")["Monetary"]

    .sum()

    .reset_index()
)
persona_count = (

    segments

    .groupby("Persona")

    .size()

    .reset_index(name="Customers")
)
col1, col2 = st.columns(2)

with col1:

    st.subheader("Customer Segments")

    fig = donut_chart(

        segment_count,

        names="Segment",

        values="Customers",

        title="Customer Segments",

    )

    render_chart(fig)

with col2:

    st.subheader("Revenue by Segment")

    fig = bar_chart(

        segment_revenue,

        x="Segment",

        y="Monetary",

        text_auto=True,

    )

    render_chart(fig)
st.subheader("Customer Personas")

fig = donut_chart(

    persona_count,

    names="Persona",

    values="Customers",

    title="Customer Personas",

)

render_chart(fig)
st.subheader("Top 10 High Value Customers")

top_customers = (

    rfm

    .sort_values(
        "Monetary",
        ascending=False
    )

    .head(10)
)

st.dataframe(

    top_customers[
        [
            "Customer ID",
            "Recency",
            "Frequency",
            "Monetary"
        ]
    ],

    hide_index=True,

    use_container_width=True,
)
st.subheader("Segment Summary")

st.dataframe(

    segment_summary,

    hide_index=True,

    use_container_width=True,
)
# ==========================================================
# DEMAND FORECASTING
# ==========================================================

divider()

section_header(
    "Demand Forecasting",
    "Projected sales trends and business outlook"
)
forecast["Date"] = pd.to_datetime(
    forecast["Date"],
    errors="coerce"
)

forecast = forecast.sort_values("Date")
col1, col2, col3, col4 = st.columns(4)

forecast_total = forecast["ForecastSales"].sum()

forecast_average = forecast["ForecastSales"].mean()

forecast_peak = forecast["ForecastSales"].max()

forecast_growth = (
    (
        forecast["ForecastSales"].iloc[-1]
        -
        forecast["ForecastSales"].iloc[0]
    )
    /
    forecast["ForecastSales"].iloc[0]
) * 100

with col1:
    st.metric(
        "Forecast Revenue",
        f"${forecast_total:,.0f}"
    )

with col2:
    st.metric(
        "Daily Average",
        f"${forecast_average:,.0f}"
    )

with col3:
    st.metric(
        "Peak Forecast",
        f"${forecast_peak:,.0f}"
    )

with col4:
    st.metric(
        "Growth",
        f"{forecast_growth:.1f}%"
    )
st.subheader("Forecast Trend")

fig = line_chart(

    forecast,

    x="Date",

    y="ForecastSales",

    markers=True,

)

render_chart(fig)
forecast_bins = forecast.copy()

forecast_bins["Range"] = pd.cut(

    forecast_bins["ForecastSales"],

    bins=5
).astype(str)

distribution = (

    forecast_bins

    .groupby("Range")

    .size()

    .reset_index(name="Days")
)
col1, col2 = st.columns(2)

with col1:

    st.subheader("Forecast Distribution")

    fig = bar_chart(

        distribution,

        x="Range",

        y="Days",

        text_auto=True,

    )

    render_chart(fig)

with col2:

    st.subheader("Forecast Data")

    st.dataframe(

        forecast,

        hide_index=True,

        use_container_width=True,
    )
st.subheader("Business Outlook")

if forecast_growth >= 10:

    st.success(
        """
### 📈 Strong Growth Expected

Demand is projected to increase significantly.

Recommended Actions:

- Increase inventory levels.
- Prepare additional logistics capacity.
- Focus marketing on high-performing products.
"""
    )

elif forecast_growth >= 0:

    st.info(
        """
### 📊 Stable Demand

Sales are expected to remain steady.

Recommended Actions:

- Maintain current inventory.
- Continue monitoring customer demand.
"""
    )

else:

    st.warning(
        """
### 📉 Demand Slowdown

Sales are forecast to decline.

Recommended Actions:

- Reduce procurement.
- Optimize stock levels.
- Run promotional campaigns.
"""
    )
# ==========================================================
# INVENTORY INTELLIGENCE
# ==========================================================

divider()

section_header(
    "Inventory Intelligence",
    "Inventory optimization and product classification"
)
kpi_dict = dict(
    zip(
        inventory["KPI"],
        inventory["Value"]
    )
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Inventory Value",
        kpi_dict.get("Inventory Value", "-")
    )

with col2:
    st.metric(
        "Inventory Turnover",
        kpi_dict.get("Inventory Turnover", "-")
    )

with col3:
    st.metric(
        "Stockout Rate",
        kpi_dict.get("Stockout Rate", "-")
    )

with col4:
    st.metric(
        "Holding Cost",
        kpi_dict.get("Holding Cost", "-")
    )
inventory_status = (

    inventory_opt

    .groupby("InventoryStatus")

    .size()

    .reset_index(name="Products")
)
abc_summary = (

    abc

    .groupby("ABC")

    .size()

    .reset_index(name="Products")
)
xyz_summary = (

    xyz

    .groupby("XYZ")

    .size()

    .reset_index(name="Products")
)
col1, col2 = st.columns(2)

with col1:

    st.subheader("Inventory Status")

    fig = donut_chart(

        inventory_status,

        names="InventoryStatus",

        values="Products",

        title="Inventory Status"

    )

    render_chart(fig)

with col2:

    st.subheader("ABC Classification")

    fig = donut_chart(

        abc_summary,

        names="ABC",

        values="Products",

        title="ABC Analysis"

    )

    render_chart(fig)
col1, col2 = st.columns(2)

with col1:

    st.subheader("XYZ Classification")

    fig = donut_chart(

        xyz_summary,

        names="XYZ",

        values="Products",

        title="XYZ Analysis"

    )

    render_chart(fig)

with col2:

    st.subheader("Inventory Recommendation Count")

    recommendation_summary = (

        inventory_rec

        .groupby("Recommendation")

        .size()

        .reset_index(name="Products")
    )

    fig = bar_chart(

        recommendation_summary,

        x="Recommendation",

        y="Products",

        text_auto=True,

    )

    render_chart(fig)
st.subheader("ABC–XYZ Matrix")

matrix = (

    abcxyz

    .groupby("ABC_XYZ")

    .size()

    .reset_index(name="Products")
)

fig = bar_chart(

    matrix,

    x="ABC_XYZ",

    y="Products",

    text_auto=True,

)

render_chart(fig)
st.subheader("Highest Revenue Products")

top_inventory = (

    inventory_opt

    .sort_values(
        "Revenue",
        ascending=False
    )

    .head(10)
)

fig = bar_chart(

    top_inventory,

    x="ProductID",

    y="Revenue",

    text_auto=True,

)

render_chart(fig)
st.subheader("Optimization Recommendations")

display_columns = [

    "ProductID",

    "ABC",

    "XYZ",

    "InventoryStatus",

    "CurrentStock",

    "Recommendation"

]

st.dataframe(

    inventory_opt[display_columns],

    hide_index=True,

    use_container_width=True,
)
st.subheader("Inventory Insights")

overstock = (

    inventory_opt["InventoryStatus"]

    .eq("Overstock")

    .sum()
)

understock = (

    inventory_opt["InventoryStatus"]

    .eq("Understock")

    .sum()
)

optimal = (

    inventory_opt["InventoryStatus"]

    .eq("Optimal")

    .sum()
)

st.info(f"""
### Inventory Overview

• 🟢 Optimal Products : **{optimal}**

• 🔴 Overstock Products : **{overstock}**

• 🟠 Understock Products : **{understock}**

Recommendation:

Focus replenishment on understock products while reducing excess inventory to improve inventory turnover and minimize holding costs.
""")
# ==========================================================
# CHURN INTELLIGENCE
# ==========================================================

divider()

section_header(
    "Churn Intelligence",
    "Customer retention analysis and business recommendations"
)
col1, col2, col3, col4 = st.columns(4)

customers_analyzed = len(churn)

churn_customers = churn["Prediction"].sum()

retention_rate = (
    (customers_analyzed - churn_customers)
    / customers_analyzed
) * 100

avg_probability = (
    churn["Churn_Probability"].mean()
) * 100

with col1:
    st.metric(
        "Customers",
        f"{customers_analyzed:,}"
    )

with col2:
    st.metric(
        "Predicted Churn",
        churn_customers
    )

with col3:
    st.metric(
        "Retention Rate",
        f"{retention_rate:.1f}%"
    )

with col4:
    st.metric(
        "Average Risk",
        f"{avg_probability:.1f}%"
    )
churn_distribution = (

    churn

    .groupby("Prediction")

    .size()

    .reset_index(name="Customers")
)
risk = churn.copy()

risk["Risk"] = pd.cut(

    risk["Churn_Probability"],

    bins=[0,0.4,0.7,1],

    labels=[
        "Low",
        "Medium",
        "High"
    ]
)

risk_summary = (

    risk

    .groupby("Risk")

    .size()

    .reset_index(name="Customers")
)
col1, col2 = st.columns(2)

with col1:

    st.subheader("Predicted Churn")

    fig = donut_chart(

        churn_distribution,

        names="Prediction",

        values="Customers",

        title="Churn Prediction"

    )

    render_chart(fig)

with col2:

    st.subheader("Customer Risk")

    fig = bar_chart(

        risk_summary,

        x="Risk",

        y="Customers",

        text_auto=True,

    )

    render_chart(fig)
st.subheader("Top Churn Drivers")

top_features = (

    importance

    .sort_values(
        "Importance",
        ascending=False
    )

    .head(10)
)

fig = bar_chart(

    top_features,

    x="Feature",

    y="Importance",

    text_auto=True,

)

render_chart(fig)
st.subheader("Highest Risk Customers")

high_risk = (

    churn

    .sort_values(
        "Churn_Probability",
        ascending=False
    )

    .head(15)
)

st.dataframe(

    high_risk,

    hide_index=True,

    use_container_width=True,
)
divider()

section_header(
    "AI Business Recommendations",
    "Key strategic recommendations"
)

recommendations = []

if forecast_growth > 10:
    recommendations.append(
        "📈 Increase inventory to meet expected demand."
    )

if understock > overstock:
    recommendations.append(
        "📦 Restock products classified as Understock."
    )

if overstock > understock:
    recommendations.append(
        "📉 Reduce excess inventory for slow-moving products."
    )

if retention_rate < 90:
    recommendations.append(
        "👥 Launch customer retention campaigns."
    )

recommendations.append(
    "⭐ Prioritize A-Class products for inventory planning."
)

recommendations.append(
    "🎯 Reward high-value customer segments."
)

for rec in recommendations:
    st.success(rec)
divider()

section_header(
    "Executive Summary",
    "RetailPulse Management Report"
)

summary = f"""
## 📊 RetailPulse Executive Report

### Business Performance

- **Revenue Generated:** ${total_revenue:,.0f}
- **Customers:** {customers:,}
- **Stores:** {stores}
- **Forecast Revenue:** ${forecast_total:,.0f}

### Customer Analytics

- **Retention Rate:** {retention_rate:.1f}%
- **Average Customer Spend:** ${avg_spend:,.2f}

### Inventory

- Overstock Products: {overstock}

- Understock Products: {understock}

- Optimal Inventory: {optimal}

### Forecast

Forecast indicates a projected growth of **{forecast_growth:.1f}%** over the coming period.

### Conclusion

RetailPulse integrates customer analytics, demand forecasting, inventory optimization, and churn prediction into a unified decision-support platform.

The analytics indicate opportunities to:

- Improve inventory efficiency
- Increase customer retention
- Optimize product availability
- Support data-driven strategic planning
"""

st.markdown(summary)
footer()
