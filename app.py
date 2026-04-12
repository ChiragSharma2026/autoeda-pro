import streamlit as st
import pandas as pd
from analyzer import analyze
from recommendations import generate_recommendations
from health import compute_health_score
from insights import generate_feature_importance
import matplotlib.pyplot as plt
import os

st.set_page_config(page_title="AutoEDA", page_icon="📊", layout="wide")

# Custom CSS
st.markdown("""
    <style>
    .main { background-color: #0f1117; }
    .block-container { padding-top: 2rem; }
    .metric-card {
        background-color: #1e2130;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        border: 1px solid #2d3250;
    }
    .metric-value { font-size: 2rem; font-weight: bold; color: #4da6ff; }
    .metric-label { font-size: 0.9rem; color: #aaaaaa; margin-top: 5px; }
    .section-header {
        border-left: 4px solid #4da6ff;
        padding-left: 10px;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .good { color: #00cc66; }
    .moderate { color: #ffaa00; }
    .poor { color: #ff4444; }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("<h1 style='color:#4da6ff;'>📊 AutoEDA</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#aaaaaa; font-size:1.1rem;'>Automated Dataset Analysis & Quality Scoring</p>", unsafe_allow_html=True)
st.divider()

# Sidebar
with st.sidebar:
    st.markdown("### 📂 Upload Dataset")
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])
    st.divider()
    st.markdown("### ℹ️ About")
    st.markdown("AutoEDA analyzes any CSV and gives you:")
    st.markdown("- 📈 Health Score")
    st.markdown("- 🧠 Recommendations")
    st.markdown("- 🔗 Correlations")
    st.markdown("- 📊 Distributions")
    st.markdown("- 🎯 Feature Importance")
    st.divider()
    st.markdown("[GitHub](https://github.com/ChiragSharma2026/autoeda-pro) | [Live Demo](https://autoeda-pro.streamlit.app)")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success(f"✅ Loaded: **{df.shape[0]} rows** and **{df.shape[1]} columns**")

    # Dataset Summary
    st.markdown("<div class='section-header'><h2>📋 Dataset Summary</h2></div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"<div class='metric-card'><div class='metric-value'>{df.shape[0]}</div><div class='metric-label'>Rows</div></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='metric-card'><div class='metric-value'>{df.shape[1]}</div><div class='metric-label'>Columns</div></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='metric-card'><div class='metric-value'>{int(df.duplicated().sum())}</div><div class='metric-label'>Duplicates</div></div>", unsafe_allow_html=True)

    # Column Overview
    st.markdown("<div class='section-header'><h2>🗂 Column Overview</h2></div>", unsafe_allow_html=True)
    st.dataframe(df.dtypes.reset_index().rename(columns={"index": "Column", 0: "Type"}), use_container_width=True)

    # Health Score
    score, label, breakdown = compute_health_score(df)
    st.markdown("<div class='section-header'><h2>📈 Dataset Health Score</h2></div>", unsafe_allow_html=True)

    css_class = label.lower()
    st.markdown(f"<h1 class='{css_class}'>{score}/100 — {label}</h1>", unsafe_allow_html=True)
    st.progress(int(score) / 100)

    with st.expander("📊 Score Breakdown"):
        for k, v in breakdown.items():
            st.write(f"**{k.replace('_', ' ').title()}:** -{v}")

    # Recommendations
    st.markdown("<div class='section-header'><h2>🧠 Recommendations</h2></div>", unsafe_allow_html=True)
    recs = generate_recommendations(df)
    for r in recs:
        if "DROPPING" in r:
            st.error(f"🔴 {r}")
        elif "convert" in r.lower():
            st.warning(f"🟡 {r}")
        else:
            st.info(f"🔵 {r}")

    # Correlation Table
    st.markdown("<div class='section-header'><h2>🔗 Correlation Table</h2></div>", unsafe_allow_html=True)
    numeric_df = df.select_dtypes(include='number')
    if not numeric_df.empty:
        st.dataframe(numeric_df.corr().round(2), use_container_width=True)

    # Distributions
    st.markdown("<div class='section-header'><h2>📊 Distributions</h2></div>", unsafe_allow_html=True)
    cols = st.columns(2)
    for i, col in enumerate(numeric_df.columns):
        with cols[i % 2]:
            fig, ax = plt.subplots(figsize=(5, 3))
            numeric_df[col].dropna().hist(bins=30, ax=ax, color='#4da6ff', edgecolor='white')
            ax.set_title(f"{col}", fontsize=11)
            ax.set_facecolor('#1e2130')
            fig.patch.set_facecolor('#1e2130')
            ax.tick_params(colors='white')
            ax.title.set_color('white')
            ax.xaxis.label.set_color('white')
            ax.yaxis.label.set_color('white')
            st.pyplot(fig, use_container_width=False)
            plt.close()

    # Feature Importance
    st.markdown("<div class='section-header'><h2>🎯 Feature Importance</h2></div>", unsafe_allow_html=True)
    st.info("💡 Select a numeric or low-cardinality column as target (e.g. Survived, Price, Category)")
    target = st.selectbox("Select target column", options=df.columns)

    if st.button("Run Feature Importance", type="primary"):
        with st.spinner("Training model..."):
            importance_df = generate_feature_importance(df, target)
        if importance_df is not None:
            st.session_state['importance_df'] = importance_df
            st.session_state['importance_target'] = target
        else:
            st.warning(f"Could not compute feature importance for: **{target}**")

    if 'importance_df' in st.session_state:
        importance_df = st.session_state['importance_df']
        imp_target = st.session_state['importance_target']
        st.dataframe(importance_df, use_container_width=True)
        fig, ax = plt.subplots(figsize=(6, 3))
        ax.barh(importance_df["Feature"][:10][::-1],
                importance_df["Importance"][:10][::-1],
                color='#4da6ff')
        ax.set_title(f"Feature Importance → {imp_target}", color='white')
        ax.set_xlabel("Importance Score", color='white')
        ax.set_facecolor('#1e2130')
        fig.patch.set_facecolor('#1e2130')
        ax.tick_params(colors='white')
        st.pyplot(fig, use_container_width=False)
        plt.close()

        # SHAP chart
        if os.path.exists("shap_summary.png"):
            st.markdown("#### 🔍 SHAP Explainability")
            st.image("shap_summary.png", width=600)
            st.caption("Mean |SHAP Value| — how much each feature influences the prediction on average")

    # Download Report
    st.markdown("<div class='section-header'><h2>⬇️ Download Report</h2></div>", unsafe_allow_html=True)

    from report import generate_html_report

    summary = analyze(df)
    dl_target = st.session_state.get('importance_target', None)
    generate_html_report(summary, recs, score, label, breakdown, df, target=dl_target)

    if os.path.exists("report.html"):
        with open("report.html", "r", encoding="utf-8") as f:
            html_content = f.read()
        st.download_button(
            label="📥 Download HTML Report",
            data=html_content,
            file_name="autoeda_report.html",
            mime="text/html",
            type="primary"
        )

else:
    st.markdown("""
    <div style='text-align:center; padding: 80px 0;'>
        <h2 style='color:#4da6ff;'>👈 Upload a CSV file to get started</h2>
        <p style='color:#aaaaaa;'>Supports any CSV dataset up to 200MB</p>
    </div>
    """, unsafe_allow_html=True)