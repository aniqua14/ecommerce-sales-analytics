
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
import joblib
import os

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="E-commerce Analytics Dashboard",
    page_icon="📦",
    layout="wide"
)

# ============================================================
# LOAD DATA
# ============================================================
base = os.path.dirname(os.path.abspath(__file__))

@st.cache_data
def load_data():
    kpi       = pd.read_csv(f"{base}/kpi_summary.csv")
    rfm       = pd.read_csv(f"{base}/rfm_summary.csv")
    rfm_churn = pd.read_csv(f"{base}/rfm_with_churn.csv")
    sales     = pd.read_csv(f"{base}/sales_data.csv")
    customers = pd.read_csv(f"{base}/customer_info.csv")
    return kpi, rfm, rfm_churn, sales, customers

kpi_df, rfm_df, rfm_churn_df, sales_df, customers_df = load_data()

# Helper to get a KPI value by name
def get_kpi(name):
    row = kpi_df.loc[kpi_df["Metric"] == name, "Value"]
    return row.values[0] if len(row) else "N/A"

# ============================================================
# HEADER
# ============================================================
st.title("📦 E-commerce Sales & Customer Analytics")
st.markdown("**Green Cart Ltd** — Interactive Business Intelligence Dashboard")
st.markdown("---")

# ============================================================
# TAB LAYOUT
# ============================================================
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 KPIs",
    "📈 Sales Analysis",
    "👥 RFM & Segments",
    "🤖 Model Evaluation"
])

# ============================================================
# TAB 1 — KPIs
# ============================================================
with tab1:
    st.subheader("Business Performance Overview")
    st.markdown("Key metrics summarising overall business health.")

    # Row 1 — Financial KPIs
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💰 Total Revenue",
                f"{float(get_kpi('Total_Revenue')):,.0f} BDT")
    col2.metric("🛒 Total Orders",
                f"{int(float(get_kpi('Total_Orders'))):,}")
    col3.metric("👤 Total Customers",
                f"{int(float(get_kpi('Total_Customers'))):,}")
    col4.metric("🧾 Avg Order Value",
                f"{float(get_kpi('Avg_Order_Value')):,.2f} BDT")

    st.markdown("")

    # Row 2 — Operational KPIs
    col5, col6, col7, col8 = st.columns(4)
    col5.metric("📦 Delivery Success",
                f"{float(get_kpi('Delivery_Success_Rate')):.1f}%",
                delta="-58.9% orders delayed/cancelled",
                delta_color="inverse")
    col6.metric("🔄 Churn Rate",
                f"{float(get_kpi('Churn_Rate')):.1f}%")
    col7.metric("📋 Avg Orders/Customer",
                f"{float(get_kpi('Avg_Orders_Per_Customer')):.1f}")
    col8.metric("🏷️ Avg Discount",
                f"{float(get_kpi('Avg_Discount')):.1f}%")

    st.markdown("")

    # Row 3 — Top performers
    col9, col10 = st.columns(2)
    col9.info(f"🏆 **Top Region:** {str(get_kpi('Top_Region')).title()}")
    col10.info(f"🏆 **Top Category:** {str(get_kpi('Top_Category')).title()}")

    st.markdown("---")
    st.warning(
        "⚠️ **Key Business Alert:** Only 41.1% of orders are successfully "
        "delivered. 39.1% are delayed and 19.7% are cancelled. "
        "This is a critical operational issue requiring immediate attention."
    )

# ============================================================
# TAB 2 — SALES ANALYSIS
# ============================================================
with tab2:
    st.subheader("Sales Performance Analysis")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Revenue by Region**")
        img = Image.open(f"{base}/region_revenue.png")
        st.image(img, use_container_width=True)
        st.caption(
            "South leads slightly but all regions contribute similarly, "
            "suggesting no region-specific marketing is needed."
        )

    with col2:
        st.markdown("**Top 10 Categories by Revenue**")
        img = Image.open(f"{base}/top_categories.png")
        st.image(img, use_container_width=True)
        st.caption(
            "Cleaning products generate nearly 2x more revenue than "
            "any other category. Priority stocking recommended."
        )

    col3, col4 = st.columns(2)

    with col3:
        st.markdown("**Revenue by Loyalty Tier**")
        img = Image.open(f"{base}/loyalty_revenue.png")
        st.image(img, use_container_width=True)
        st.caption(
            "Gold customers generate 3x more revenue than Silver or Bronze. "
            "Loyalty program is clearly driving high-value behaviour."
        )

    with col4:
        st.markdown("**Payment Method Distribution**")
        img = Image.open(f"{base}/payment_methods.png")
        st.image(img, use_container_width=True)
        st.caption(
            "Credit card dominates at 48%. All three methods are active "
            "so supporting all payment options is important."
        )

    col5, col6 = st.columns(2)

    with col5:
        st.markdown("**Delivery Status Distribution**")
        img = Image.open(f"{base}/delivery_status.png")
        st.image(img, use_container_width=True)
        st.caption(
            "⚠️ Critical finding: 59% of orders are delayed or cancelled. "
            "Immediate logistics review recommended."
        )

    with col6:
        st.markdown("**Revenue by Gender**")
        img = Image.open(f"{base}/gender_revenue.png")
        st.image(img, use_container_width=True)
        st.caption(
            "Female customers generate significantly more revenue (119K) "
            "vs male (81K). Consider gender-targeted campaigns."
        )

# ============================================================
# TAB 3 — RFM & SEGMENTS
# ============================================================
with tab3:
    st.subheader("Customer Segmentation — RFM Analysis")
    st.markdown(
        "RFM stands for **Recency, Frequency, Monetary**. "
        "Each customer is scored on these three dimensions "
        "to identify their value and behaviour pattern."
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Customer Segments**")
        img = Image.open(f"{base}/rfm_segments.png")
        st.image(img, use_container_width=True)
        st.caption(
            "272 Loyal Customers vs 227 Potential Loyalists. "
            "Focus retention efforts on converting Potential Loyalists."
        )

    with col2:
        st.markdown("**Segment Summary (Averages)**")
        seg_cols = ["segment", "recency", "frequency", "monetary"]
        available = [c for c in seg_cols if c in rfm_churn_df.columns]
        if available:
            seg_summary = rfm_churn_df.groupby("segment")[
                ["frequency","monetary"]
            ].mean().round(2)
            st.dataframe(seg_summary, use_container_width=True)
            st.caption(
                "Loyal Customers average 7.7 orders and 625 BDT revenue. "
                "Potential Loyalists average 3.9 orders and 304 BDT revenue."
            )

    st.markdown("---")
    st.subheader("Churn Analysis")

    col3, col4 = st.columns(2)

    with col3:
        # Churn distribution chart
        churn_counts = rfm_churn_df["churn"].value_counts()                         .rename(index={0: "Not Churned", 1: "Churned"})
        fig, ax = plt.subplots(figsize=(5, 4))
        sns.barplot(
            x=churn_counts.index,
            y=churn_counts.values,
            hue=churn_counts.index,
            palette=["steelblue", "tomato"],
            legend=False,
            ax=ax
        )
        ax.set_title("Churn Distribution", fontweight="bold")
        ax.set_ylabel("Number of Customers")
        for i, v in enumerate(churn_counts.values):
            ax.text(i, v + 2, str(v), ha="center", fontweight="bold")
        plt.tight_layout()
        st.pyplot(fig)
        st.caption("Only 2% churn rate (10 customers). "
                   "Dataset limitation — single date orders.")

    with col4:
        st.markdown("**RFM Data Sample**")
        st.dataframe(
            rfm_churn_df[[
                "customer_id","frequency","monetary","segment","churn"
            ]].head(10),
            use_container_width=True
        )

    st.markdown("---")
    st.info(
        "📌 **Note on Recency:** All orders in this dataset occur on the "
        "same date (July 6, 2025), so recency is identical for all customers. "
        "In a production system, time-based recency would be a key differentiator."
    )

# ============================================================
# TAB 4 — MODEL EVALUATION
# ============================================================
with tab4:
    st.subheader("Churn Prediction — Model Evaluation")
    st.markdown(
        "Two models were trained and compared: "
        "**Logistic Regression** (baseline) and **Random Forest**. "
        "Both use customer frequency and monetary value as features."
    )

    # Model comparison chart
    st.markdown("**Model Comparison — ROC-AUC Score**")
    img = Image.open(f"{base}/model_comparison.png")
    st.image(img, use_container_width=True)

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Logistic Regression — Confusion Matrix**")
        img = Image.open(f"{base}/cm_logistic.png")
        st.image(img, use_container_width=True)
        st.caption(
            "Correctly identified both churned customers. "
            "5 false positives (non-churners flagged as churners)."
        )

    with col2:
        st.markdown("**Random Forest — Confusion Matrix**")
        img = Image.open(f"{base}/cm_random_forest.png")
        st.image(img, use_container_width=True)
        st.caption(
            "Perfect classification on test set. "
            "0 false positives, 0 false negatives."
        )

    st.markdown("---")
    st.markdown("**ROC Curve — Both Models**")
    img = Image.open(f"{base}/roc_curve.png")
    st.image(img, use_container_width=True)
    st.caption(
        "Both models achieve AUC = 1.0 on this dataset. "
        "This reflects the dataset limitation (2% churn, single date). "
        "In production with richer features, scores would be more realistic."
    )

    st.markdown("---")
    st.markdown("### Understanding the Metrics")

    col3, col4, col5 = st.columns(3)
    col3.info(
        "**Precision**\n\n"
        "Of all customers predicted to churn, "
        "how many actually churned?"
    )
    col4.info(
        "**Recall**\n\n"
        "Of all customers who actually churned, "
        "how many did we catch?"
    )
    col5.info(
        "**ROC-AUC**\n\n"
        "Overall model quality score. "
        "1.0 = perfect, 0.5 = random guess."
    )

    st.markdown("---")
    st.warning(
        "⚠️ **Honest Model Limitation:** The perfect AUC score is due to "
        "target leakage — churn was defined using frequency, which is also "
        "a model feature. In a real project, time-based behavioural features "
        "would be used instead."
    )

# ============================================================
# FOOTER
# ============================================================
st.markdown("---")
st.caption(
    "Built by Aniqua Nawar | "
    "Data Science Portfolio Project | "
    "Dataset: Green Cart Ltd (Kaggle)"
)
