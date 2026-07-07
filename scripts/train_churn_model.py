
"""
RetailPulse - train_churn_model.py

Train a churn model from the Online Retail dataset using RFM features.

Outputs
-------
data/processed/customer_churn_predictions.csv
data/processed/churn_feature_importance.csv
models/churn_model.pkl
"""

from pathlib import Path
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
RAW = DATA / "raw"
PROCESSED = DATA / "processed"
MODELS = ROOT / "models"

PROCESSED.mkdir(parents=True, exist_ok=True)
MODELS.mkdir(parents=True, exist_ok=True)


def load_data():
    """
    Load the Online Retail dataset from either
    data/processed or data/raw.
    """

    possible_files = [
        ROOT / "data" / "processed" / "online_processed1.csv",
        ROOT / "data" / "raw" / "online_processed1.csv",
        ROOT / "data" / "processed" / "online_processed.csv",
        ROOT / "data" / "raw" / "online_processed.csv",
    ]

    for file in possible_files:
        if file.exists():
            print(f"Loading dataset: {file}")
            return pd.read_csv(
                file,
                parse_dates=["InvoiceDate"]
            )

    raise FileNotFoundError(
        "online_processed1.csv not found in data/raw or data/processed."
    )


def build_rfm(df: pd.DataFrame) -> pd.DataFrame:
    df = df.dropna(subset=["Customer ID"]).copy()
    df["Revenue"] = df["Quantity"] * df["Price"]

    snapshot = df["InvoiceDate"].max() + pd.Timedelta(days=1)

    rfm = (
        df.groupby("Customer ID")
        .agg(
            Recency=("InvoiceDate", lambda x: (snapshot - x.max()).days),
            Frequency=("Invoice", "nunique"),
            Monetary=("Revenue", "sum"),
            Quantity=("Quantity", "sum"),
            Country=("Country", "first"),
        )
        .reset_index()
    )

    rfm["AvgOrderValue"] = rfm["Monetary"] / rfm["Frequency"]
    rfm["Churn"] = (rfm["Recency"] > 90).astype(int)
    return rfm


def train(rfm: pd.DataFrame):
    X = rfm[["Recency", "Frequency", "Monetary", "Quantity", "AvgOrderValue"]]
    y = rfm["Churn"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=300,
        random_state=42,
        class_weight="balanced",
    )
    model.fit(X_train, y_train)

    pred = model.predict(X_test)
    print(f"Accuracy: {accuracy_score(y_test, pred):.4f}")
    print(classification_report(y_test, pred))

    probs = model.predict_proba(X)[:, 1]
    rfm["Churn_Probability"] = probs
    rfm["Prediction"] = (probs >= 0.5).astype(int)

    fi = pd.DataFrame({
        "Feature": X.columns,
        "Importance": model.feature_importances_
    }).sort_values("Importance", ascending=False)

    rfm.to_csv(PROCESSED / "customer_churn_predictions.csv", index=False)
    fi.to_csv(PROCESSED / "churn_feature_importance.csv", index=False)
    joblib.dump(model, MODELS / "churn_model.pkl")

    print("\nFiles generated:")
    print(PROCESSED / "customer_churn_predictions.csv")
    print(PROCESSED / "churn_feature_importance.csv")
    print(MODELS / "churn_model.pkl")


def main():
    df = load_data()
    rfm = build_rfm(df)
    train(rfm)


if __name__ == "__main__":
    main()
