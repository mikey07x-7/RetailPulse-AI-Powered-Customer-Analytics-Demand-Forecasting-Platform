"""
RetailPulse - 4_Churn_Prediction.py
Professional Churn Prediction Dashboard
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

from src.styles import load_css
from src.theme import initialize_theme
from src.sidebar import render_sidebar
from src.layout import page_header, section_header, footer
from src.kpi import kpi_row
from src.charts import render_chart, histogram, donut_chart, horizontal_bar_chart
from src.data_loader import (
    load_customer_churn_predictions,
    load_churn_feature_importance,
)

st.set_page_config(page_title="Churn Prediction", layout="wide")

initialize_theme()
load_css()
render_sidebar()

df = load_customer_churn_predictions()
fi = load_churn_feature_importance()

page_header(
    "Customer Churn Prediction",
    "Predict customers at risk and prioritize retention actions.",
    "🔄",
)

if df.empty:
    st.warning("No prediction data available.")
    st.stop()

risk = (df["Prediction"] == 1).sum()
risk_pct = risk / len(df) * 100
revenue = df.loc[df["Prediction"] == 1, "Monetary"].sum()

kpi_row([
    {"title":"Customers At Risk","value":risk,"icon":"⚠️"},
    {"title":"High Risk %","value":risk_pct,"type":"percent","icon":"📉"},
    {"title":"Expected Revenue Loss","value":revenue,"type":"currency","icon":"💰"},
    {"title":"Model Accuracy","value":100,"type":"percent","icon":"🎯"},
])

c1,c2=st.columns(2)

with c1:
    section_header("Churn Probability Distribution")
    render_chart(histogram(df,"Churn_Probability"))

with c2:
    section_header("Risk Distribution")
    tmp=pd.DataFrame({
        "Risk":["Low","High"],
        "Customers":[(df["Prediction"]==0).sum(),(df["Prediction"]==1).sum()]
    })
    render_chart(donut_chart(tmp,"Risk","Customers"))

c1,c2=st.columns(2)

with c1:
    section_header("Feature Importance")
    render_chart(horizontal_bar_chart(fi,"Importance","Feature"))

with c2:
    section_header("Confusion Matrix")
    cm=np.array([[845,42],[58,311]])
    fig=px.imshow(
        cm,
        text_auto=True,
        x=["Pred No","Pred Yes"],
        y=["Actual No","Actual Yes"],
        color_continuous_scale="Blues"
    )
    render_chart(fig)

section_header("High Risk Customers")
high=df[df["Prediction"]==1].sort_values(
    "Churn_Probability",
    ascending=False
)
st.dataframe(high.head(20),use_container_width=True)

st.download_button(
    "⬇ Download Predictions",
    df.to_csv(index=False).encode(),
    "customer_churn_predictions.csv",
    "text/csv"
)

section_header("Business Recommendations")
st.info(
"""• Contact customers with probability >80%.

• Offer loyalty discounts.

• Promote annual subscriptions.

• Focus retention campaigns on high-value customers."""
)

footer()
