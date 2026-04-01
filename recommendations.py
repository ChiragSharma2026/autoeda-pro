def generate_recommendations(df):
    recommendations = []
    total_rows = df.shape[0]

    for col in df.columns:
        missing = df[col].isnull().sum()
        missing_pct = (missing / total_rows) * 100
        unique_count = df[col].nunique()

        if missing_pct > 0:
            recommendations.append(f"{col}: {missing_pct:.2f}% missing values")

        if missing_pct > 50:
            recommendations.append(f"{col}: {missing_pct:.1f}% missing → consider DROPPING")

        if unique_count == total_rows:
            recommendations.append(f"{col}: high cardinality → likely ID column")

        if df[col].dtype == 'object':
            try:
                df[col].astype(float)
                recommendations.append(f"{col}: stored as object but numeric → convert to numeric")
            except (ValueError, TypeError):
                pass

        if df[col].dtype == 'object':
            if "date" in col.lower():
                recommendations.append(f"{col}: appears to be date → convert to datetime")

    return recommendations