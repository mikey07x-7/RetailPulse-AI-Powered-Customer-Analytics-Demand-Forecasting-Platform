"""
===========================================================
RetailPulse - Customer Segmentation
===========================================================

Analyze customer behaviour using RFM Segmentation.

Author : Junaid
Project : RetailPulse
"""

from __future__ import annotations

import streamlit as st

from src.styles import load_css
from src.theme import initialize_theme

from src.layout import (
    page_header,
    section_header,
    divider,
    space,
)

from src.kpi import kpi_card

from src.data_loader import (
    load_customer_segments,
    calculate_customer_kpis,
    filter_customer_segments,
    segment_summary,
)

from src.charts import (
    render_chart,
    histogram,
    treemap,
    donut_chart,
    bubble_chart,
)

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Customer Segmentation | RetailPulse",
    page_icon="👥",
    layout="wide",
)

initialize_theme()
load_css()

# ==========================================================
# LOAD DATA
# ==========================================================

try:

    customer_segments = load_customer_segments()

except Exception as e:

    st.error(f"Unable to load datasets.\n\n{e}")

    st.stop()

# ==========================================================
# KPI DATA
# ==========================================================

kpis = calculate_customer_kpis(customer_segments)

# ==========================================================
# PAGE HEADER
# ==========================================================

page_header(
    title="Customer Segmentation",
    subtitle="Analyze customer purchasing behaviour using RFM Analysis",
    icon="👥",
)

st.caption(
    f"""
    **Customer Records:** {customer_segments.shape[0]:,}

    **Available Segments:** {customer_segments['Segment'].nunique()}
    """
)
divider()
# ==========================================================
# CUSTOMER KPI DASHBOARD
# ==========================================================

section_header(
    "Customer Overview",
    "Key customer metrics from RFM analysis."
)

space()

col1, col2, col3, col4 = st.columns(4)

with col1:
    kpi_card(
        title="Total Customers",
        value=kpis['total_customers'],
        icon="👥",
    )

with col2:
    kpi_card(
        title="Average Spend",
        value=kpis['avg_monetary'],
        icon="💰",
    )

with col3:
    kpi_card(
        title="Average Frequency",
        value=kpis['avg_frequency'],
        icon="🛒",
    )

with col4:
    kpi_card(
        title="Average Recency",
        value=kpis['avg_recency'],
        icon="📅",
    )

space(2)

with st.expander("📈 KPI Summary", expanded=False):

    repeat_rate = (
        kpis["repeat_customers"] /
        kpis["total_customers"] * 100
        if kpis["total_customers"] > 0
        else 0
    )

    c1, c2 = st.columns(2)

    with c1:

        st.metric(
            "Repeat Customers",
            f"{kpis['repeat_customers']:,}",
        )

    with c2:

        st.metric(
            "Repeat Customer Rate",
            f"{repeat_rate:.1f}%",
        )

divider()
# ==========================================================
# CUSTOMER FILTERS
# ==========================================================

section_header(
    "Customer Filters",
    "Filter customers by segment and RFM metrics."
)

space()

filter_col1, filter_col2, filter_col3, filter_col4 = st.columns(4)

# ----------------------------------------------------------
# Segment Filter
# ----------------------------------------------------------

segment_options = ["All"]

if "Segment" in customer_segments.columns:
    segment_options.extend(
        sorted(customer_segments["Segment"].dropna().unique())
    )

with filter_col1:

    selected_segment = st.selectbox(
        "Customer Segment",
        options=segment_options,
    )

# ----------------------------------------------------------
# Frequency Filter
# ----------------------------------------------------------

freq_min = int(customer_segments["Frequency"].min())
freq_max = int(customer_segments["Frequency"].max())

with filter_col2:

    frequency_range = st.slider(
        "Purchase Frequency",
        min_value=freq_min,
        max_value=freq_max,
        value=(freq_min, freq_max),
    )

# ----------------------------------------------------------
# Monetary Filter
# ----------------------------------------------------------

money_min = float(customer_segments["Monetary"].min())
money_max = float(customer_segments["Monetary"].max())

with filter_col3:

    monetary_range = st.slider(
        "Monetary Value",
        min_value=money_min,
        max_value=money_max,
        value=(money_min, money_max),
    )

# ----------------------------------------------------------
# Recency Filter
# ----------------------------------------------------------

recency_min = int(customer_segments["Recency"].min())
recency_max = int(customer_segments["Recency"].max())

with filter_col4:

    recency_range = st.slider(
        "Recency (Days)",
        min_value=recency_min,
        max_value=recency_max,
        value=(recency_min, recency_max),
    )

# ==========================================================
# APPLY FILTERS
# ==========================================================

filtered_customers = filter_customer_segments(
    customer_segments,
    segment=selected_segment,
    frequency_range=frequency_range,
    monetary_range=monetary_range,
    recency_range=recency_range,
)

space()

st.caption(
    f"Showing **{len(filtered_customers):,}** customers after applying filters."
)

divider()
# ==========================================================
# RFM DISTRIBUTION ANALYSIS
# ==========================================================

section_header(
    "RFM Distribution Analysis",
    "Analyze the distribution of Recency, Frequency and Monetary values."
)

space()

tab_recency, tab_frequency, tab_monetary = st.tabs(
    [
        "📅 Recency",
        "🛒 Frequency",
        "💰 Monetary",
    ]
)
# ==========================================================
# RECENCY
# ==========================================================

with tab_recency:

    fig = histogram(
        filtered_customers,
        x="Recency",
        nbins=30,
        title="Recency Distribution",
    )

    render_chart(fig)

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Average",
        f"{filtered_customers['Recency'].mean():.1f}"
    )

    c2.metric(
        "Median",
        f"{filtered_customers['Recency'].median():.1f}"
    )

    c3.metric(
        "Maximum",
        f"{filtered_customers['Recency'].max():.0f}"
    )

# ==========================================================
# FREQUENCY
# ==========================================================

with tab_frequency:

    fig = histogram(
        filtered_customers,
        x="Frequency",
        nbins=25,
        title="Purchase Frequency Distribution",
    )

    render_chart(fig)

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Average",
        f"{filtered_customers['Frequency'].mean():.2f}"
    )

    c2.metric(
        "Median",
        f"{filtered_customers['Frequency'].median():.2f}"
    )

    c3.metric(
        "Maximum",
        f"{filtered_customers['Frequency'].max():.0f}"
    )

# ==========================================================
# MONETARY
# ==========================================================

with tab_monetary:

    fig = histogram(
        filtered_customers,
        x="Monetary",
        nbins=30,
        title="Customer Spending Distribution",
    )

    render_chart(fig)

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Average",
        f"${filtered_customers['Monetary'].mean():,.2f}"
    )

    c2.metric(
        "Median",
        f"${filtered_customers['Monetary'].median():,.2f}"
    )

    c3.metric(
        "Maximum",
        f"${filtered_customers['Monetary'].max():,.2f}"
    )

divider()
# ==========================================================
# CUSTOMER SEGMENT OVERVIEW
# ==========================================================

section_header(
    "Customer Segment Overview",
    "Revenue and customer distribution across RFM segments."
)

space()

summary_df = segment_summary(filtered_customers)

left, right = st.columns([1.4, 1])

# ==========================================================
# TREEMAP
# ==========================================================

with left:

    fig = treemap(
        summary_df,
        path=["Segment"],
        values="Revenue",
        color="Revenue",
        title="Revenue by Customer Segment",
    )

    render_chart(fig)

# ==========================================================
# DONUT CHART
# ==========================================================

with right:

    fig = donut_chart(
        summary_df,
        names="Segment",
        values="Customers",
        title="Customer Distribution",
    )

    render_chart(fig)

space()

# ==========================================================
# SEGMENT SUMMARY TABLE
# ==========================================================

st.dataframe(
    summary_df,
    use_container_width=True,
    hide_index=True,
)
# ==========================================================
# SEGMENT ANALYTICS
# ==========================================================

divider()

section_header(
    "Segment Analytics",
    "Quick business insights from customer segmentation."
)

space()

if not summary_df.empty:

    highest_revenue = summary_df.loc[
        summary_df["Revenue"].idxmax()
    ]

    highest_spend = summary_df.loc[
        summary_df["AvgSpend"].idxmax()
    ]

    loyal_segment = summary_df.loc[
        summary_df["AvgFrequency"].idxmax()
    ]

    at_risk_segment = summary_df.loc[
        summary_df["AvgRecency"].idxmax()
    ]

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.metric(
            label="🏆 Highest Revenue",
            value=highest_revenue["Segment"],
            delta=f"${highest_revenue['Revenue']:,.0f}",
        )

    with c2:

        st.metric(
            label="❤️ Most Loyal",
            value=loyal_segment["Segment"],
            delta=f"{loyal_segment['AvgFrequency']:.2f} Purchases",
        )

    with c3:

        st.metric(
            label="💰 Highest Avg Spend",
            value=highest_spend["Segment"],
            delta=f"${highest_spend['AvgSpend']:,.2f}",
        )

    with c4:

        st.metric(
            label="⚠ Highest Recency",
            value=at_risk_segment["Segment"],
            delta=f"{at_risk_segment['AvgRecency']:.0f} Days",
        )

else:

    st.info("No customer segment data available.")
# ==========================================================
# CUSTOMER EXPLORER
# ==========================================================

divider()

section_header(
    "Customer Explorer",
    "Browse, search and export filtered customer records."
)

space()

# ----------------------------------------------------------
# Search
# ----------------------------------------------------------

search_col, download_col = st.columns([3, 1])

with search_col:

    search_text = st.text_input(
        "🔍 Search Customer ID",
        placeholder="Enter Customer ID...",
    )

# ----------------------------------------------------------
# Search Filter
# ----------------------------------------------------------

display_df = filtered_customers.copy()

if search_text:

    if "Customer ID" in display_df.columns:

        display_df = display_df[
            display_df["Customer ID"]
            .astype(str)
            .str.contains(
                search_text,
                case=False,
                na=False,
            )
        ]

# ----------------------------------------------------------
# Sort by Monetary
# ----------------------------------------------------------

if "Monetary" in display_df.columns:

    display_df = display_df.sort_values(
        "Monetary",
        ascending=False,
    )

# ----------------------------------------------------------
# Download Button
# ----------------------------------------------------------

with download_col:

    st.download_button(
        label="📥 Download CSV",
        data=display_df.to_csv(index=False),
        file_name="customer_segments_filtered.csv",
        mime="text/csv",
        use_container_width=True,
    )

space()

st.caption(
    f"Showing {len(display_df):,} customer records."
)

# ----------------------------------------------------------
# Customer Table
# ----------------------------------------------------------

preferred_columns = [

    "Customer ID",

    "Segment",

    "Recency",

    "Frequency",

    "Monetary",
]

columns_to_show = [

    col

    for col in preferred_columns

    if col in display_df.columns
]

if columns_to_show:

    st.dataframe(

        display_df[columns_to_show],

        use_container_width=True,

        hide_index=True,

        height=450,
    )

else:

    st.dataframe(

        display_df,

        use_container_width=True,

        hide_index=True,

        height=450,
    )
# ==========================================================
# CUSTOMER LIFETIME VALUE ANALYSIS
# ==========================================================

divider()

section_header(
    "Customer Lifetime Value Analysis",
    "Relationship between purchase frequency, recency and customer value."
)

space()

if not display_df.empty:

    bubble_df = display_df.copy()

    # ------------------------------------------------------
    # Bubble Size
    # ------------------------------------------------------

    bubble_df["BubbleSize"] = (
        bubble_df["Monetary"]
        .clip(lower=1)
    )

    fig = bubble_chart(
        bubble_df,
        x="Frequency",
        y="Recency",
        size="BubbleSize",
        color="Segment",
        hover_name="Customer ID",
        title="Customer Lifetime Value Distribution",
    )

    fig.update_layout(
        xaxis_title="Purchase Frequency",
        yaxis_title="Recency (Days)",
    )

    render_chart(fig)

    space()

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(
            "Highest Customer Value",
            f"${bubble_df['Monetary'].max():,.2f}"
        )

    with c2:

        st.metric(
            "Average Customer Value",
            f"${bubble_df['Monetary'].mean():,.2f}"
        )

    with c3:

        st.metric(
            "Median Customer Value",
            f"${bubble_df['Monetary'].median():,.2f}"
        )

else:

    st.info("No customer data available.")
# ==========================================================
# EXECUTIVE INSIGHTS
# ==========================================================

divider()

section_header(
    "Business Recommendations",
    "Actionable insights generated from customer segmentation."
)

space()

if not summary_df.empty:

    highest_revenue = summary_df.loc[
        summary_df["Revenue"].idxmax()
    ]["Segment"]

    highest_spend = summary_df.loc[
        summary_df["AvgSpend"].idxmax()
    ]["Segment"]

    loyal_segment = summary_df.loc[
        summary_df["AvgFrequency"].idxmax()
    ]["Segment"]

    at_risk_segment = summary_df.loc[
        summary_df["AvgRecency"].idxmax()
    ]["Segment"]

    c1, c2 = st.columns(2)

    with c1:

        st.success(
            f"""
### 🏆 Highest Revenue Segment

**{highest_revenue}**

Continue targeting this segment with premium products,
exclusive offers and loyalty rewards.
"""
        )

        st.info(
            f"""
### ❤️ Most Loyal Customers

**{loyal_segment}**

Introduce referral campaigns and early-access benefits
to maximize lifetime value.
"""
        )

    with c2:

        st.warning(
            f"""
### 💰 Highest Spending Segment

**{highest_spend}**

Cross-sell complementary products and
bundle high-margin items.
"""
        )

        st.error(
            f"""
### ⚠ At-Risk Segment

**{at_risk_segment}**

Launch win-back campaigns,
discount coupons and personalized emails.
"""
        )

space(2)

# ==========================================================
# EXECUTIVE SUMMARY
# ==========================================================

st.markdown("### 📌 Executive Summary")

total_revenue = filtered_customers["Monetary"].sum()

avg_frequency = filtered_customers["Frequency"].mean()

avg_recency = filtered_customers["Recency"].mean()

st.markdown(
    f"""
- 👥 **Customers Analysed:** **{len(filtered_customers):,}**
- 💰 **Total Revenue:** **${total_revenue:,.2f}**
- 🛒 **Average Purchase Frequency:** **{avg_frequency:.2f}**
- 📅 **Average Recency:** **{avg_recency:.1f} Days**

### Key Takeaways

- High-frequency customers contribute significantly to revenue.
- Recent purchasers should receive loyalty rewards.
- Customers with high recency require re-engagement campaigns.
- Focus marketing efforts on high-value customer segments.
"""
)

divider()

st.caption(
    "RetailPulse • Customer Segmentation Dashboard • Powered by Streamlit & Plotly"
)