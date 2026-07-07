# 🛍️ RetailPulse

### AI-Powered Retail Analytics & Business Intelligence Dashboard

RetailPulse is an end-to-end **Retail Analytics Dashboard** built using **Python, Streamlit, Machine Learning, and Interactive Visualizations**. The project helps retail businesses make data-driven decisions by analyzing customer behavior, forecasting sales, predicting customer churn, optimizing inventory, and generating business insights.

This project was developed as part of a **Data Science & Analytics Internship** to demonstrate practical applications of data analytics and machine learning in the retail industry.

---

## 📌 Features

### 🏠 Home Dashboard

* Executive KPI cards
* Sales overview
* Revenue trends
* Interactive visualizations
* Business summary

### 👥 Customer Segmentation

* RFM Analysis
* Customer Segmentation
* Segment Distribution
* ABC Analysis
* XYZ Analysis
* Customer Insights

### 📈 Demand Forecasting

* Sales Forecasting
* Historical Sales Trends
* Forecast Visualization
* Time-Series Analysis

### ⚠️ Customer Churn Prediction

* Churn Risk Analysis
* Feature Importance
* Customer Risk Distribution
* Business Recommendations

### 📦 Inventory Optimization

* Inventory KPIs
* ABC-XYZ Inventory Matrix
* Overstock & Understock Detection
* Inventory Recommendations

### 📊 Business Insights

* Executive Dashboard
* Revenue Analysis
* Profit Trends
* Sales Performance
* Interactive Business Reports

---

# 🧠 Machine Learning Models

This project integrates Machine Learning models for predictive analytics.

* LSTM Neural Network (Demand Forecasting)
* Prophet Time-Series Forecasting
* Customer Segmentation
* Churn Prediction
* Inventory Analysis

---

# 🛠️ Tech Stack

### Programming

* Python 3.12+

### Dashboard

* Streamlit

### Data Processing

* Pandas
* NumPy

### Data Visualization

* Plotly
* Matplotlib

### Machine Learning

* Scikit-learn
* TensorFlow / Keras
* Prophet

### Utilities

* Joblib
* Pickle

---

# 📂 Project Structure

```text
RetailPulse/
│
├── app.py
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
├── data/
│   ├── processed/
│   └── raw/
│
├── models/
│
├── assets/
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

# 📊 Dataset

The project utilizes processed retail datasets containing information such as:

* Customer Information
* Sales Transactions
* Inventory Records
* Product Categories
* Revenue Metrics
* Customer Segments
* Sales Forecast Data
* Churn Prediction Data

---

# 🚀 Installation

## Clone the repository

```bash
git clone https://github.com/yourusername/RetailPulse.git
```

```bash
cd RetailPulse
```

## Create a virtual environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

## Install dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Run the Application

```bash
streamlit run app.py
```

The application will open automatically in your browser.

---

# 📸 Dashboard Preview

Add screenshots of the following pages after uploading them to the repository:

* Home Dashboard
* Customer Segmentation
* Demand Forecasting
* Churn Prediction
* Inventory Optimization
* Business Insights

Example:

```
assets/screenshots/home.png
assets/screenshots/customer_segmentation.png
assets/screenshots/forecasting.png
```

---

# 💼 Business Value

RetailPulse enables businesses to:

* Improve customer retention
* Forecast future demand
* Reduce inventory costs
* Identify high-value customers
* Optimize stock levels
* Support strategic business decisions
* Visualize key performance indicators in real time

---

# 🔮 Future Enhancements

* Live Database Integration
* Cloud Deployment
* Real-Time Sales Streaming
* Automated Report Generation
* Role-Based Authentication
* AI Chat Assistant
* Advanced Demand Forecasting
* Explainable AI (XAI)

---

# 👨‍💻 Author

**Junaid Iqbal A. Chouri**

Electronics & Communication Engineering Student
Bangalore Institute of Technology

---

# 📄 License

This project is intended for educational and internship purposes.

Feel free to fork, explore, and learn from the implementation.
