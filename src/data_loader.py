"""
===========================================================
RetailPulse - Central Data Loader
===========================================================

Loads all processed datasets used throughout the dashboard.

Author : Junaid
Project: RetailPulse
"""

from pathlib import Path
import pandas as pd
import streamlit as st

# ==========================================================
# Project Paths
# ==========================================================

ROOT_DIR = Path(__file__).resolve().parents[1]

DATA_DIR = ROOT_DIR / "data" / "processed"

# ==========================================================
# Internal CSV Loader
# ==========================================================

@st.cache_data(show_spinner=False)
def _read_csv(filename: str) -> pd.DataFrame:
    """
    Reads a CSV file from data/processed.
    """

    filepath = DATA_DIR / filename

    if not filepath.exists():
        raise FileNotFoundError(
            f"\nDataset '{filename}' not found.\n"
            f"Expected Location:\n{filepath}"
        )

    return pd.read_csv(filepath)


# ==========================================================
# Individual Dataset Loaders
# ==========================================================

@st.cache_data(show_spinner=False)
def load_inventory_kpis():
    return _read_csv("inventory_kpis.csv")


@st.cache_data(show_spinner=False)
def load_customer_segments():
    return _read_csv("customer_segments.csv")


@st.cache_data(show_spinner=False)
def load_customer_rfm():
    return _read_csv("customer_rfm1.csv")

@st.cache_data(show_spinner=False)
def load_customer_churn_predictions():
    return _read_csv("customer_churn_predictions.csv")

@st.cache_data(show_spinner=False)
def load_inventory_optimization():
    return _read_csv("inventory_optimization.csv")


@st.cache_data(show_spinner=False)
def load_inventory_recommendations():
    return _read_csv("inventory_recommendations.csv")


@st.cache_data(show_spinner=False)
def load_sales_forecast():
    return _read_csv("sales_forecast.csv")


@st.cache_data(show_spinner=False)
def load_abc_analysis():
    return _read_csv("abc_analysis.csv")


@st.cache_data(show_spinner=False)
def load_xyz_analysis():
    return _read_csv("xyz_analysis.csv")


@st.cache_data(show_spinner=False)
def load_abc_xyz_matrix():
    return _read_csv("abc_xyz_matrix.csv")


@st.cache_data(show_spinner=False)
def load_segment_summary():
    return _read_csv("segment_summary.csv")


@st.cache_data(show_spinner=False)
def load_churn_feature_importance():
    return _read_csv("churn_feature_importance.csv")


@st.cache_data(show_spinner=False)
def load_online_processed():
    return _read_csv("online_processed1.csv")


@st.cache_data(show_spinner=False)
def load_rossmann_processed():
    return _read_csv("rossmann_processed1.csv")


# ==========================================================
# Dashboard Loader
# ==========================================================

@st.cache_data(show_spinner=False)
def load_dashboard_data():
    """
    Load every processed dataset.

    Returns:
        dict[str, pd.DataFrame]
    """

    return {

        "inventory_kpis": load_inventory_kpis(),

        "customer_segments": load_customer_segments(),

        "customer_rfm": load_customer_rfm(),

        "inventory_optimization": load_inventory_optimization(),

        "inventory_recommendations": load_inventory_recommendations(),

        "sales_forecast": load_sales_forecast(),

        "abc_analysis": load_abc_analysis(),

        "xyz_analysis": load_xyz_analysis(),

        "abc_xyz_matrix": load_abc_xyz_matrix(),

        "segment_summary": load_segment_summary(),

        "churn_feature_importance": load_churn_feature_importance(),

        "online_processed": load_online_processed(),

        "rossmann_processed": load_rossmann_processed(),
        
        "customer_churn_predictions": load_customer_churn_predictions(),
    }


# ==========================================================
# Utility Functions
# ==========================================================

def dataset_exists(filename: str) -> bool:
    """Check if a dataset exists."""

    return (DATA_DIR / filename).exists()


def get_dataset_path(filename: str) -> Path:
    """Return full dataset path."""

    return DATA_DIR / filename


def list_available_datasets():
    """List all CSV datasets."""

    if not DATA_DIR.exists():
        return []

    return sorted(
        [file.name for file in DATA_DIR.glob("*.csv")]
    )


def dataset_status():
    """
    Returns dashboard dataset status.

    Returns:
        dict
    """

    expected = [

        "inventory_kpis.csv",

        "customer_segments.csv",

        "customer_rfm1.csv",

        "inventory_optimization.csv",

        "inventory_recommendations.csv",

        "sales_forecast.csv",

        "abc_analysis.csv",

        "abc_xyz_matrix.csv",

        "xyz_analysis.csv",

        "segment_summary.csv",

        "churn_feature_importance.csv",

        "online_processed1.csv",

        "rossmann_processed1.csv",
    ]

    available = list_available_datasets()

    loaded = sum(file in available for file in expected)

    return {

        "loaded": loaded,

        "total": len(expected),

        "missing": sorted(list(set(expected) - set(available))),

        "available": available
    }


# ==========================================================
# Dashboard Health Check
# ==========================================================

def health_check():
    """
    Dashboard startup validation.
    """

    status = dataset_status()

    if status["loaded"] != status["total"]:

        raise FileNotFoundError(

            f"""
RetailPulse Startup Failed

Expected : {status['total']} datasets

Found : {status['loaded']}

Missing:

{chr(10).join(status['missing'])}
"""
        )

    return True

# ==========================================================
# Customer Segmentation Utilities
# ==========================================================

def calculate_customer_kpis(
    rfm_df: pd.DataFrame,
) -> dict:
    """
    Calculate dashboard KPI metrics for Customer Segmentation.
    """

    if rfm_df.empty:
        return {
            "total_customers": 0,
            "avg_monetary": 0.0,
            "avg_frequency": 0.0,
            "avg_recency": 0.0,
            "repeat_customers": 0,
        }

    frequency_col = "Frequency"
    monetary_col = "Monetary"
    recency_col = "Recency"

    return {

        "total_customers": len(rfm_df),

        "avg_monetary": round(
            rfm_df[monetary_col].mean(),
            2,
        ),

        "avg_frequency": round(
            rfm_df[frequency_col].mean(),
            2,
        ),

        "avg_recency": round(
            rfm_df[recency_col].mean(),
            1,
        ),

        "repeat_customers": int(
            (rfm_df[frequency_col] > 1).sum()
        ),
    }


# ==========================================================
# Customer Filters
# ==========================================================

def filter_customer_segments(
    df: pd.DataFrame,
    segment: str = "All",
    frequency_range=None,
    monetary_range=None,
    recency_range=None,
) -> pd.DataFrame:
    """
    Apply filters to customer dataframe.
    """

    filtered = df.copy()

    if segment != "All" and "Segment" in filtered.columns:
        filtered = filtered[
            filtered["Segment"] == segment
        ]

    if (
        frequency_range is not None
        and "Frequency" in filtered.columns
    ):
        filtered = filtered[
            filtered["Frequency"].between(
                frequency_range[0],
                frequency_range[1],
            )
        ]

    if (
        monetary_range is not None
        and "Monetary" in filtered.columns
    ):
        filtered = filtered[
            filtered["Monetary"].between(
                monetary_range[0],
                monetary_range[1],
            )
        ]

    if (
        recency_range is not None
        and "Recency" in filtered.columns
    ):
        filtered = filtered[
            filtered["Recency"].between(
                recency_range[0],
                recency_range[1],
            )
        ]

    return filtered


# ==========================================================
# Segment Summary
# ==========================================================

def segment_summary(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Generate summary statistics for each customer segment.
    """

    if df.empty:
        return pd.DataFrame()

    summary = (
        df.groupby("Segment")
        .agg(
            Customers=("Customer ID", "count"),
            Revenue=("Monetary", "sum"),
            AvgSpend=("Monetary", "mean"),
            AvgFrequency=("Frequency", "mean"),
            AvgRecency=("Recency", "mean"),
        )
        .reset_index()
    )

    summary["Revenue"] = summary["Revenue"].round(2)
    summary["AvgSpend"] = summary["AvgSpend"].round(2)
    summary["AvgFrequency"] = summary["AvgFrequency"].round(2)
    summary["AvgRecency"] = summary["AvgRecency"].round(1)

    return summary.sort_values(
        "Revenue",
        ascending=False,
    )
# ==========================================================
# Main (Testing)
# ==========================================================

if __name__ == "__main__":

    print("=" * 60)
    print("RetailPulse Data Loader")
    print("=" * 60)

    print("Root Directory")
    print(ROOT_DIR)

    print()

    print("Processed Data Directory")
    print(DATA_DIR)

    print()

    health_check()

    datasets = load_dashboard_data()

    print("Datasets Loaded Successfully\n")

    for name, df in datasets.items():
        print(f"{name:<30} {df.shape}")

    print("\nAvailable Files")

    for file in list_available_datasets():
        print("✓", file)