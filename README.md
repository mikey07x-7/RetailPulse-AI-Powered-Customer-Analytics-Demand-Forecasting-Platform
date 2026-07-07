# 📊 RetailPulse – AI-Powered Customer Analytics & Demand Forecasting Platform

> An end-to-end Data Science & Analytics platform that leverages Machine Learning to forecast demand, analyze customer behavior, predict churn, and optimize inventory through an interactive Streamlit dashboard.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red)
![TensorFlow](https://img.shields.io/badge/TensorFlow-LSTM-orange)
![Prophet](https://img.shields.io/badge/Prophet-Time%20Series-green)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-ML-yellow)
![License](https://img.shields.io/badge/License-MIT-blue)

---

# 🚀 Overview

RetailPulse is an AI-powered retail analytics platform developed as part of the **Zidio Development Data Science & Analytics Internship**.

The project transforms raw retail transaction data into actionable business insights using Machine Learning and Interactive Business Intelligence.

The application enables retailers to:

- 📈 Forecast future sales
- 👥 Segment customers using RFM Analysis
- ❤️ Predict customer churn
- 📦 Optimize inventory levels
- 📊 Monitor business KPIs
- 💡 Generate strategic business insights

The complete solution follows an end-to-end Data Science workflow including data preprocessing, feature engineering, machine learning, visualization, and dashboard deployment.

---

# ✨ Features

## 🏠 Home Dashboard

- Executive KPI Dashboard
- Revenue Analysis
- Sales Trends
- Customer Overview
- Business Performance Metrics
- Interactive Filters

---

## 👥 Customer Segmentation

- RFM Analysis
- Customer Segmentation
- ABC Analysis
- XYZ Analysis
- Customer Lifetime Insights
- Segment-wise Revenue Distribution

---

## 📈 Demand Forecasting

- Prophet Forecasting
- LSTM Forecasting
- Historical vs Forecast Comparison
- Future Sales Prediction
- Trend Analysis
- Forecast KPIs

---

## ❤️ Churn Prediction

- Customer Churn Prediction
- Feature Importance
- Churn Probability
- Risk Distribution
- High-Risk Customer Analysis
- Retention Recommendations

---

## 📦 Inventory Optimization

- Inventory KPIs
- Reorder Recommendations
- Overstock Detection
- Understock Detection
- Inventory Health Score
- Stock Optimization Strategy

---

## 💼 Business Insights

- Executive Summary
- Key Business Findings
- Revenue Opportunities
- Customer Insights
- Inventory Recommendations
- Strategic Decision Support

---

# 🧠 Machine Learning Models

| Model | Purpose |
|---------|---------|
| Prophet | Demand Forecasting |
| LSTM (TensorFlow/Keras) | Time Series Forecasting |
| KMeans | Customer Segmentation |
| Random Forest / XGBoost | Churn Prediction |
| RFM Analysis | Customer Behaviour Analysis |

---

# 📂 Project Structure

```text
RetailPulse/
│
├── app.py
│
├── assets/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── models/
│   ├── prophet_model.pkl
│   ├── lstm_forecasting_model.keras
│   └── ...
│
├── notebooks/
│
├── pages/
│   ├── 1_Home.py
│   ├── 2_Customer_Segmentation.py
│   ├── 3_Demand_Forecasting.py
│   ├── 4_Churn_Prediction.py
│   ├── 5_Inventory_Optimization.py
│   └── 6_Business_Insights.py
│
├── src/
│   ├── charts.py
│   ├── constants.py
│   ├── data_loader.py
│   ├── filters.py
│   ├── kpi.py
│   ├── layout.py
│   ├── sidebar.py
│   ├── styles.py
│   ├── theme.py
│   └── utils.py
│
├── requirements.txt
├── README.md
└── LICENSE
```

---

# 🛠️ Technology Stack

## Programming

- Python 3.11

## Dashboard

- Streamlit

## Machine Learning

- Scikit-Learn
- TensorFlow
- Prophet
- XGBoost

## Data Processing

- Pandas
- NumPy

## Visualization

- Plotly
- Matplotlib
- Seaborn

## Model Storage

- Pickle
- Keras Models

---

# 📊 Data Science Workflow

```
Raw Dataset
      │
      ▼
Data Cleaning
      │
      ▼
Feature Engineering
      │
      ▼
EDA
      │
      ▼
Customer Segmentation
      │
      ▼
Demand Forecasting
      │
      ▼
Churn Prediction
      │
      ▼
Inventory Optimization
      │
      ▼
Interactive Dashboard
```

---

# 📈 Key Modules

### Customer Analytics

- Customer Segmentation
- RFM Analysis
- ABC Analysis
- XYZ Analysis

---

### Sales Forecasting

- Time Series Forecasting
- Prophet Model
- LSTM Forecasting

---

### Inventory Analytics

- Inventory KPIs
- Stock Recommendation
- Safety Stock Analysis

---

### Customer Retention

- Churn Prediction
- Customer Risk Analysis
- Retention Strategy

---

# 📦 Installation

Clone the repository

```bash
git clone https://github.com/yourusername/RetailPulse.git
```

Navigate into the project

```bash
cd RetailPulse
```

Create Virtual Environment

```bash
python -m venv venv
```

Activate Environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Run the Project

```bash
streamlit run app.py
```

The dashboard will open at

```
http://localhost:8501
```

---

# 📸 Dashboard Preview

> Replace these placeholders with your actual screenshots before submission.

## Home Dashboard

```
assets/screenshots/home.png
```

---

## Customer Segmentation

```
assets/screenshots/customer_segmentation.png
```

---

## Demand Forecasting

```
assets/screenshots/forecast.png
```

---

## Churn Prediction

```
assets/screenshots/churn.png
```

---

## Inventory Optimization

```
assets/screenshots/inventory.png
```

---

# 📊 Business Impact

RetailPulse helps businesses by:

- 📈 Improving demand forecasting accuracy
- 📉 Reducing stockouts
- 💰 Increasing profitability
- ❤️ Improving customer retention
- 📦 Optimizing inventory
- 📊 Supporting strategic decision-making

---

# 🚀 Future Enhancements

- Live Database Integration
- Real-time Sales Dashboard
- MLflow Integration
- Drift Detection
- Explainable AI (SHAP)
- Docker Deployment
- FastAPI Backend
- Streamlit Cloud Deployment
- Automated Retraining Pipeline

---

# 📚 Learning Outcomes

This project demonstrates practical experience in:

- Data Cleaning
- Feature Engineering
- Machine Learning
- Time Series Forecasting
- Customer Analytics
- Business Intelligence
- Dashboard Development
- Data Visualization
- Model Deployment
- End-to-End Data Science Pipeline

---

# 👨‍💻 Author

**Junaid Iqbal A Chouri**

Electronics & Communication Engineering Student

Bangalore Institute of Technology

Data Science & Machine Learning Enthusiast

---

# 🙏 Acknowledgements

- Zidio Development
- Streamlit
- Scikit-Learn
- TensorFlow
- Prophet
- Plotly
- Pandas
- Open Source Community

---

# ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub.

---

## 📄 License

This project is developed for educational and internship purposes under the **Zidio Development Data Science & Analytics Internship Program**.

MIT License © 2026 Junaid Iqbal A Chouri
