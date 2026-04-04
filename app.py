import streamlit as st
import pandas as pd
from analyzer import analyze
from recommendations import generate_recommendations
from health import compute_health_score
from insights import generate_feature_importance
import matplotlib.pyplot as plt

st.set_page_config(page_title="AutoEDA", page_icon="📊", layout="wide")

st.title("📊 AutoEDA — Automated Dataset Analysis")
st.markdown("Upload any CSV and get instant data quality insights.")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.success(f"Loaded: {df.shape[0]} rows, {df.shape[1]} columns")

    # Dataset Summary
    st.header("📋 Dataset Summary")
    col1, col2, col3 = st.columns(3)
    col1.metric("Rows", df.shape[0])
    col2.metric("Columns", df.shape[1])
    col3.metric("Duplicates", int(df.duplicated().sum()))

    # Column Overview
    st.header("🗂 Column Overview")
    st.dataframe(df.dtypes.reset_index().rename(columns={"index": "Column", 0: "Type"}))

    # Health Score
    score, label, breakdown = compute_health_score(df)
    st.header("📈 Dataset Health Score")

    color = "green" if label == "Good" else "orange" if label == "Moderate" else "red"
    st.markdown(f"<h1 style='color:{color}'>{score}/100 — {label}</h1>", unsafe_allow_html=True)

    st.subheader("Score Breakdown")
    for k, v in breakdown.items():
        st.write(f"**{k}:** -{v}")

    # Recommendations
    st.header("🧠 Recommendations")
    recs = generate_recommendations(df)
    for r in recs:
        if "DROPPING" in r:
            st.error(r)
        elif "convert" in r.lower():
            st.warning(r)
        else:
            st.info(r)

    # Correlation Table
    st.header("🔗 Correlation Table")
    numeric_df = df.select_dtypes(include='number')
    if not numeric_df.empty:
        st.dataframe(numeric_df.corr().round(2))

    # Distributions
    st.header("📊 Distributions")
    for col in numeric_df.columns:
        fig, ax = plt.subplots(figsize=(6, 3))
        numeric_df[col].dropna().hist(bins=30, ax=ax, color='steelblue', edgecolor='white')
        ax.set_title(f"Distribution: {col}")
        ax.set_xlabel(col)
        ax.set_ylabel("Frequency")
        st.pyplot(fig, use_container_width=False)
        plt.close()

    # Feature Importance
    st.header("🎯 Feature Importance")
    target = st.selectbox("Select target column", options=df.columns)
    if st.button("Run Feature Importance"):
        importance_df = generate_feature_importance(df, target)
        if importance_df is not None:
            st.dataframe(importance_df)
            fig, ax = plt.subplots(figsize=(6, 3))
            ax.barh(importance_df["Feature"][:10][::-1],
                    importance_df["Importance"][:10][::-1],
                    color='steelblue')
            ax.set_title(f"Feature Importance → Target: {target}")
            ax.set_xlabel("Importance Score")
            st.pyplot(fig, use_container_width=False)
            plt.close()
        else:
            st.warning("Could not compute feature importance for selected target.")