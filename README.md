# 📦 E-commerce Sales & Customer Analytics

Interactive Business Intelligence Dashboard analyzing sales performance,
customer behaviour, RFM segmentation and churn prediction.

## 🔗 Live Demo
[👉 Click here to open the dashboard](https://ecommerce-sales-analytics-cvzea9myzgctmubxadff5s.streamlit.app/)

## 📊 Key Business Findings
- Only 41.1% of orders successfully delivered — critical operational issue
- Cleaning products generate 2x more revenue than any other category
- Gold tier customers generate 3x more revenue than Silver/Bronze
- Female customers generate 47% more revenue than male customers
- 2% churn rate with extreme class imbalance (dataset limitation noted)

## 🧠 What This Project Covers
- Full data cleaning pipeline (typos, missing values, inconsistent categories)
- Merging 3 relational tables (sales, customers, products)
- Exploratory Data Analysis with 6 business-driven visualizations
- RFM Customer Segmentation (Loyal Customers vs Potential Loyalists)
- Churn Prediction — Logistic Regression vs Random Forest
- Model Evaluation — Confusion Matrix, ROC-AUC, Classification Report
- Honest discussion of model limitations and data quality issues

## 🧱 Tech Stack
Python, Pandas, NumPy, Scikit-learn, Matplotlib, Seaborn, Streamlit

## 🤖 ML Models Used
| Model | Type | Purpose |
|---|---|---|
| Logistic Regression | Classification | Baseline churn prediction |
| Random Forest | Ensemble Classification | Main churn prediction model |

## 📈 Model Comparison
| Metric | Logistic Regression | Random Forest |
|---|---|---|
| Accuracy | 95% | 100% |
| ROC-AUC | 1.000 | 1.000 |
| Precision (Churn) | 0.29 | 1.00 |
| Recall (Churn) | 1.00 | 1.00 |
| False Positives | 5 | 0 |
| Winner | ❌ | ✅ |

## 🔍 Libraries & Tools
| Library | Version | Purpose |
|---|---|---|
| Pandas | 2.0+ | Data manipulation and cleaning |
| NumPy | 1.24+ | Numerical operations |
| Scikit-learn | 1.3+ | ML models and evaluation |
| Matplotlib | 3.7+ | Base visualizations |
| Seaborn | 0.12+ | Statistical visualizations |
| Streamlit | 1.32+ | Interactive web dashboard |
| Joblib | 1.3+ | Model serialization |

## 📂 Project Structure

ecommerce_dashboard/
├── app.py                  # Streamlit dashboard
├── requirements.txt        # Dependencies
├── ecommerce_EDA.ipynb     # Full analysis notebook
├── kpi_summary.csv         # Precomputed KPIs
├── rfm_summary.csv         # RFM analysis results
├── rfm_with_churn.csv      # Customer segments + churn labels
├── sales_data.csv          # Cleaned sales data
├── *.png                   # Saved visualizations
└── *.joblib                # Trained ML models


## ⚠️ Honest Model Note
ROC-AUC = 1.0 reflects target leakage and extreme class imbalance
(2% churn rate, single-date dataset). In production, time-based
behavioural features would produce more realistic and useful results.

## 👤 Author
Aniqua Nawar — Data Science Portfolio Project
