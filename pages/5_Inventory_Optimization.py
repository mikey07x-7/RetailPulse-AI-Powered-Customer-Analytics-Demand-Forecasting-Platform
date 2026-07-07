"""
==============================================================
RetailPulse
Inventory Optimization
==============================================================
"""

from __future__ import annotations

import streamlit as st
import pandas as pd
import numpy as np

from src.styles import load_css
from src.theme import initialize_theme
from src.sidebar import render_sidebar

from src.layout import (
    page_header,
    section_header,
    divider,
    footer,
)
import plotly.graph_objects as go
import plotly.express as px
from src.charts import (
    bar_chart,
    gauge_chart,
    render_chart,
    donut_chart,
    bubble_chart,
)
from src.kpi import kpi_row

from src.data_loader import (
    load_inventory_optimization,
    load_inventory_kpis,
    load_inventory_recommendations,
    load_abc_analysis,
    load_xyz_analysis,
    load_abc_xyz_matrix,
)

from src.utils import (
    format_currency,
    format_number,
)

# ==========================================================
# Page Config
# ==========================================================

st.set_page_config(
    page_title="Inventory Optimization",
    page_icon="📦",
    layout="wide",
)

initialize_theme()
load_css()
render_sidebar()

# ==========================================================
# Load Data
# ==========================================================

inventory_df = load_inventory_optimization()
kpi_df = load_inventory_kpis()
recommendation_df = load_inventory_recommendations()
abc_df = load_abc_analysis()
xyz_df = load_xyz_analysis()
matrix_df = load_abc_xyz_matrix()

# ==========================================================
# Validation
# ==========================================================

if inventory_df.empty:

    st.error(
        "Inventory dataset could not be loaded."
    )

    st.stop()

# ==========================================================
# Header
# ==========================================================

page_header(

    title="Inventory Optimization",

    subtitle=(
        "AI-powered inventory planning using "
        "ABC–XYZ analysis, EOQ optimization "
        "and intelligent reorder recommendations."
    ),

    icon="📦",

)

divider()

# ==========================================================
# KPI Extraction
# ==========================================================

inventory_value = 0
products = len(inventory_df)
average_eoq = inventory_df["EOQ"].mean()
critical_items = 0

if not kpi_df.empty:

    # Convert KPI table to dictionary
    # Supports two-column CSV:
    # KPI | Value

    if len(kpi_df.columns) >= 2:

        kpis = dict(
            zip(
                kpi_df.iloc[:,0],
                kpi_df.iloc[:,1]
            )
        )

        inventory_value = kpis.get(
            "Inventory Value",
            inventory_df["Revenue"].sum()
        )

        products = kpis.get(
            "Products",
            products,
        )

        average_eoq = kpis.get(
            "Average EOQ",
            average_eoq,
        )

        critical_items = kpis.get(
            "Critical",
            (
                inventory_df["InventoryStatus"]
                == "Critical"
            ).sum(),
        )

else:

    inventory_value = inventory_df["Revenue"].sum()

    critical_items = (

        inventory_df["InventoryStatus"]

        == "Critical"

    ).sum()

# ==========================================================
# Executive KPIs
# ==========================================================

kpi_row(

    [

        {

            "title": "Inventory Value",

            "value": inventory_value,

            "type": "currency",

            "icon": "💰",

        },

        {

            "title": "Products",

            "value": products,

            "icon": "📦",

        },

        {

            "title": "Average EOQ",

            "value": average_eoq,

            "icon": "📈",

        },

        {

            "title": "Critical Items",

            "value": critical_items,

            "icon": "⚠",

        },

    ]

)

divider()

# ==========================================================
# Quick Statistics
# ==========================================================

left, right = st.columns(2)

with left:

    st.info(f"""

### 📊 Inventory Overview

• Products : **{format_number(products)}**

• Inventory Value : **{format_currency(inventory_value)}**

• Average EOQ : **{format_number(average_eoq)}**

""")

with right:

    turnover = inventory_df["InventoryTurnover"].mean()

    dio = inventory_df["DIO"].mean()

    st.success(f"""

### 🚚 Warehouse Performance

• Avg Inventory Turnover : **{turnover:.2f}**

• Average DIO : **{dio:.1f} Days**

• Critical Items : **{critical_items}**

""")

divider()
# ==========================================================
# Inventory Status & Health
# ==========================================================

left, right = st.columns(2)

# ----------------------------------------------------------
# Inventory Status
# ----------------------------------------------------------

with left:

    section_header(
        "Inventory Status",
        "Distribution of inventory health"
    )

    if "InventoryStatus" in inventory_df.columns:

        status_df = (
            inventory_df["InventoryStatus"]
            .value_counts()
            .reset_index()
        )

        status_df.columns = [
            "Inventory Status",
            "Products",
        ]

        fig = bar_chart(

            status_df,

            x="Inventory Status",

            y="Products",

            text_auto=True,

        )

        render_chart(fig)

    else:

        st.warning(
            "InventoryStatus column not found."
        )

# ----------------------------------------------------------
# Inventory Health Gauge
# ----------------------------------------------------------

with right:

    section_header(
        "Inventory Health",
        "Overall inventory quality"
    )

    total_products = len(inventory_df)

    healthy_products = 0

    if "InventoryStatus" in inventory_df.columns:

        healthy_products = (

            inventory_df["InventoryStatus"]

            .str.lower()

            .isin(

                [

                    "healthy",

                    "normal",

                    "optimal",

                ]

            )

            .sum()

        )

    inventory_health = (

        healthy_products

        /

        max(total_products, 1)

        * 100

    )

    fig = gauge_chart(

        inventory_health,

        title="Inventory Health",

        suffix="%",

    )

    render_chart(fig)

divider()
# ==========================================================
# Inventory Health Summary
# ==========================================================

healthy = 0
critical = 0
overstock = 0

if "InventoryStatus" in inventory_df.columns:

    status = inventory_df["InventoryStatus"].str.lower()

    healthy = status.isin(
        ["healthy", "normal", "optimal"]
    ).sum()

    critical = status.str.contains(
        "critical",
        case=False,
        na=False,
    ).sum()

    overstock = status.str.contains(
        "over",
        case=False,
        na=False,
    ).sum()

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(

        "Healthy Products",

        f"{healthy:,}"

    )

with col2:

    st.metric(

        "Critical Stock",

        f"{critical:,}"

    )

with col3:

    st.metric(

        "Overstock Items",

        f"{overstock:,}"

    )

divider()
# ==========================================================
# ABC Analysis & XYZ Analysis
# ==========================================================

left, right = st.columns(2)

# ----------------------------------------------------------
# ABC Analysis
# ----------------------------------------------------------

with left:

    section_header(
        "ABC Analysis",
        "Inventory classification by annual consumption"
    )

    abc_summary = (

        inventory_df

        .groupby("ABC")

        .size()

        .reset_index(name="Products")

        .sort_values("ABC")

    )

    fig = donut_chart(

        abc_summary,

        names="ABC",

        values="Products",

    )

    render_chart(fig)

# ----------------------------------------------------------
# XYZ Analysis
# ----------------------------------------------------------

with right:

    section_header(
        "XYZ Analysis",
        "Demand variability classification"
    )

    xyz_summary = (

        inventory_df

        .groupby("XYZ")

        .size()

        .reset_index(name="Products")

        .sort_values("XYZ")

    )

    fig = donut_chart(

        xyz_summary,

        names="XYZ",

        values="Products",

    )

    render_chart(fig)

divider()
# ==========================================================
# ABC XYZ Matrix
# ==========================================================

left, right = st.columns(2)

with left:

    section_header(
        "ABC–XYZ Matrix",
        "Product distribution"
    )

    matrix = pd.crosstab(

        inventory_df["ABC"],

        inventory_df["XYZ"]

    )

    fig = px.imshow(

        matrix,

        text_auto=True,

        aspect="auto",

        color_continuous_scale="Viridis",

    )

    fig.update_layout(

        xaxis_title="XYZ",

        yaxis_title="ABC",

    )

    render_chart(fig)
with right:

    section_header(
        "Inventory Turnover",
        "Demand vs Stock"
    )

    bubble_df = inventory_df.copy()

    bubble_df = bubble_df.nlargest(

        50,

        "Revenue"

    )

    fig = bubble_chart(

        bubble_df,

        x="InventoryTurnover",

        y="Revenue",

        size="AnnualDemand",

        hover_name="ProductID",

        color="ABC",

    )

    render_chart(fig)

divider()
# ==========================================================
# Inventory Distribution
# ==========================================================

section_header(
    "Inventory Classification Summary"
)

summary = pd.DataFrame({

    "Metric":[

        "A Class",

        "B Class",

        "C Class",

        "X Class",

        "Y Class",

        "Z Class",

    ],

    "Products":[

        (inventory_df["ABC"]=="A").sum(),

        (inventory_df["ABC"]=="B").sum(),

        (inventory_df["ABC"]=="C").sum(),

        (inventory_df["XYZ"]=="X").sum(),

        (inventory_df["XYZ"]=="Y").sum(),

        (inventory_df["XYZ"]=="Z").sum(),

    ]

})

st.dataframe(

    summary,

    use_container_width=True,

    hide_index=True,

)
# ==========================================================
# Top Reorder Recommendations
# ==========================================================

section_header(
    "Top Reorder Recommendations",
    "Products requiring immediate action"
)

# ----------------------------------------------------------
# Build recommendation dataframe
# ----------------------------------------------------------

recommendation_cards = inventory_df.copy()

# Priority order for inventory status
priority_map = {
    "Critical": 1,
    "Understock": 2,
    "Overstock": 3,
    "Excess Stock": 4,
    "Optimal": 5,
}

recommendation_cards["Priority"] = (
    recommendation_cards["InventoryStatus"]
    .map(priority_map)
    .fillna(99)
)

recommendation_cards = recommendation_cards.sort_values(
    ["Priority", "Revenue"],
    ascending=[True, False]
)

recommendation_cards = recommendation_cards.head(8)

# ----------------------------------------------------------
# Display Cards
# ----------------------------------------------------------

cols = st.columns(4)

for i, (_, row) in enumerate(recommendation_cards.iterrows()):

    with cols[i % 4]:

        status = str(row["InventoryStatus"])

        if status == "Critical":
            color = "#ff4b4b"
            icon = "🔴"

        elif status == "Understock":
            color = "#ffa500"
            icon = "🟠"

        elif status == "Overstock":
            color = "#f1c40f"
            icon = "🟡"

        elif status == "Excess Stock":
            color = "#3498db"
            icon = "🔵"

        else:
            color = "#2ecc71"
            icon = "🟢"

        reorder_qty = max(
            int(row["EOQ"] - row["CurrentStock"]),
            0
        )

        st.markdown(
            f"""
<div style="
background:#232F45;
padding:18px;
border-radius:14px;
border-left:6px solid {color};
margin-bottom:18px;
box-shadow:0 4px 12px rgba(0,0,0,.25);
">

<h4 style="margin-bottom:12px;">
{icon} Product {int(row['ProductID'])}
</h4>

<table style="width:100%;font-size:15px;">

<tr>
<td><b>Status</b></td>
<td>{row['InventoryStatus']}</td>
</tr>

<tr>
<td><b>Current Stock</b></td>
<td>{int(row['CurrentStock'])}</td>
</tr>

<tr>
<td><b>Reorder Point</b></td>
<td>{int(row['ReorderPoint'])}</td>
</tr>

<tr>
<td><b>EOQ</b></td>
<td>{int(row['EOQ'])}</td>
</tr>

<tr>
<td><b>Recommended Qty</b></td>
<td>{reorder_qty}</td>
</tr>

<tr>
<td><b>Annual Demand</b></td>
<td>{int(row['AnnualDemand'])}</td>
</tr>

<tr>
<td><b>Revenue</b></td>
<td>₹{row['Revenue']:,.0f}</td>
</tr>

</table>

<div style="
margin-top:14px;
padding:8px;
border-radius:8px;
background:{color};
color:white;
text-align:center;
font-weight:bold;
">

{row['Recommendation']}

</div>

</div>
""",
            unsafe_allow_html=True,
        )

divider()
# ==========================================================
# Inventory Performance
# ==========================================================

section_header(
    "Inventory Performance",
    "Detailed inventory metrics"
)

table = inventory_df.copy()

columns = [

    "ProductID",

    "ABC",

    "XYZ",

    "CurrentStock",

    "SafetyStock",

    "ReorderPoint",

    "EOQ",

    "InventoryTurnover",

    "DIO",

    "Recommendation",

]

columns = [

    c

    for c in columns

    if c in table.columns

]

table = table[columns]

styled = (

    table

    .style

    .background_gradient(

        subset=["CurrentStock"],

        cmap="Blues",

    )

    .background_gradient(

        subset=["InventoryTurnover"],

        cmap="Greens",

    )

)

st.dataframe(

    styled,

    use_container_width=True,

    height=600,

)
divider()

section_header(
    "Download Reports"
)

download1, download2 = st.columns(2)

with download1:

    st.download_button(

        "⬇ Inventory Report",

        inventory_df.to_csv(index=False).encode(),

        file_name="inventory_report.csv",

        mime="text/csv",

        use_container_width=True,

    )

with download2:

    st.download_button(

        "⬇ Reorder Recommendations",

        recommendation_cards.to_csv(index=False).encode(),

        file_name="inventory_recommendations.csv",

        mime="text/csv",

        use_container_width=True,

    )

divider()
section_header(
    "Executive Inventory Summary"
)

summary1, summary2, summary3, summary4 = st.columns(4)

with summary1:

    st.metric(

        "Products",

        f"{len(inventory_df):,}"

    )

with summary2:

    st.metric(

        "Revenue",

        f"₹{inventory_df['Revenue'].sum():,.0f}"

    )

with summary3:

    st.metric(

        "Average Turnover",

        f"{inventory_df['InventoryTurnover'].mean():.2f}"

    )

with summary4:

    st.metric(

        "Average DIO",

        f"{inventory_df['DIO'].mean():.1f}"

    )

divider()
# ==========================================================
# AI Business Insights
# ==========================================================

section_header(
    "Business Insights",
    "AI-powered inventory recommendations"
)

critical_products = (
    inventory_df["InventoryStatus"]
    .str.contains("Critical", case=False, na=False)
    .sum()
)

overstock_products = (
    inventory_df["CurrentStock"]
    >
    inventory_df["EOQ"] * 2
).sum()

healthy_products = len(inventory_df) - critical_products

inventory_health = (
    healthy_products /
    max(len(inventory_df), 1)
) * 100

c1, c2 = st.columns(2)

with c1:

    st.success(f"""
### 📦 Inventory Health

✅ Healthy Products : **{healthy_products:,}**

⚠ Critical Products : **{critical_products:,}**

📊 Overall Inventory Health : **{inventory_health:.1f}%**
""")

with c2:

    st.warning(f"""
### 💰 Optimization Opportunities

📦 Overstocked Products : **{overstock_products:,}**

💵 Inventory Value : **₹{inventory_df['Revenue'].sum():,.0f}**

🎯 Average EOQ : **{inventory_df['EOQ'].mean():.0f}**
""")

divider()
# ==========================================================
# Strategic Recommendations
# ==========================================================

section_header(
    "Strategic Recommendations"
)

cards = st.columns(4)

recommendations = [

    (
        "📦",
        "Reduce Overstock",
        "Lower purchase frequency for products whose current stock exceeds twice the EOQ."
    ),

    (
        "⚠",
        "Prevent Stockouts",
        "Increase replenishment frequency for products below the reorder point."
    ),

    (
        "💰",
        "Prioritize A-Class Items",
        "Allocate more capital to high-value A-category inventory."
    ),

    (
        "📈",
        "Improve Turnover",
        "Promote slow-moving inventory through targeted campaigns."
    ),

]

for col, (icon, title, text) in zip(cards, recommendations):

    with col:

        st.markdown(
            f"""
<div class="dashboard-card">

<h2>{icon}</h2>

<h4>{title}</h4>

<p>{text}</p>

</div>
""",
            unsafe_allow_html=True,
        )

divider()
# ==========================================================
# Inventory Alerts
# ==========================================================

section_header(
    "Inventory Alerts"
)

if critical_products > 0:

    st.error(
        f"🔴 {critical_products:,} products require immediate replenishment."
    )

else:

    st.success(
        "🟢 No critical inventory issues detected."
    )

if overstock_products > 0:

    st.warning(
        f"🟡 {overstock_products:,} products are overstocked."
    )

else:

    st.success(
        "🟢 No overstock issues detected."
    )
divider()

section_header(
    "Executive Summary"
)

st.markdown(
f"""
### 📊 Inventory Performance Overview

- **Products Managed:** {len(inventory_df):,}
- **Inventory Value:** ₹{inventory_df['Revenue'].sum():,.0f}
- **Average Inventory Turnover:** {inventory_df['InventoryTurnover'].mean():.2f}
- **Average Days in Inventory (DIO):** {inventory_df['DIO'].mean():.1f}
- **Critical Products:** {critical_products:,}
- **Inventory Health:** {inventory_health:.1f}%

### Recommendation

Focus replenishment efforts on products below their reorder point while reducing
investment in overstocked inventory. Prioritize A-class products to maximize
revenue and improve inventory turnover.
"""
)

divider()
footer()

st.caption(
    "📦 Inventory Optimization • RetailPulse v1.0 • Developed by Junaid"
)