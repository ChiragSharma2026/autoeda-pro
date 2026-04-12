import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import shap

def generate_feature_importance(df, target_col):
    """
    Computes feature importance using RandomForest and SHAP values.
    Returns: importance_df or None
    """
    if target_col not in df.columns:
        print(f"Target column '{target_col}' not found.")
        return None

    df = df.dropna(subset=[target_col])
    X = df.drop(columns=[target_col])
    y = df[target_col]
    X = X.select_dtypes(include='number')

    if X.empty:
        print("No numeric feature columns available.")
        return None

    # Drop ID-like columns
    id_like_cols = [col for col in X.columns if X[col].nunique() == len(X)]
    X = X.drop(columns=id_like_cols)

    if X.empty:
        print("No usable feature columns after removing ID-like columns.")
        return None

    # Reject high cardinality object targets
    if y.dtype == 'object' and y.nunique() > 20:
        print(f"Target '{target_col}' has too many unique categories.")
        return None

    is_classification = y.dtype == 'object' or y.nunique() < 20

    if is_classification:
        le = LabelEncoder()
        y = le.fit_transform(y.astype(str))
        model = RandomForestClassifier(n_estimators=50, random_state=42)
    else:
        model = RandomForestRegressor(n_estimators=50, random_state=42)

    model.fit(X, y)

    # RandomForest importance
    importance_df = pd.DataFrame({
        "Feature": X.columns,
        "Importance": model.feature_importances_
    }).sort_values("Importance", ascending=False)

    # RandomForest chart
    plt.figure(figsize=(8, 4))
    plt.barh(importance_df["Feature"][:10][::-1],
             importance_df["Importance"][:10][::-1],
             color='steelblue')
    plt.title(f"Feature Importance → Target: {target_col}")
    plt.xlabel("Importance Score")
    plt.tight_layout()
    plt.savefig("feature_importance.png")
    plt.close()

    # SHAP values
    try:
        explainer = shap.TreeExplainer(model)
        shap_values_raw = explainer.shap_values(X)

        import numpy as np

        # Handle different shap_values shapes
        if isinstance(shap_values_raw, list):
            sv = np.array(shap_values_raw[1])
        else:
            sv = np.array(shap_values_raw)

        # If 3D (samples, features, classes), take class 1
        if sv.ndim == 3:
            sv = sv[:, :, 1]

        mean_shap = np.abs(sv).mean(axis=0)

        shap_importance = pd.DataFrame({
            'Feature': X.columns,
            'SHAP Importance': mean_shap
        }).sort_values('SHAP Importance', ascending=True)

        plt.figure(figsize=(8, 4))
        plt.barh(shap_importance['Feature'],
                 shap_importance['SHAP Importance'],
                 color='#ff6b6b')
        plt.xlabel('Mean |SHAP Value|')
        plt.title(f"SHAP Feature Impact → Target: {target_col}")
        plt.tight_layout()
        plt.savefig("shap_summary.png", bbox_inches='tight')
        plt.close()
        print("SHAP chart saved.")

    except Exception as e:
        print(f"SHAP computation failed: {e}")

    return importance_df