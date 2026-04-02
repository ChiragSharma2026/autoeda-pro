import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

def generate_feature_importance(df, target_col):
    """
    Given a dataframe and a target column name,
    trains a quick RandomForest and returns feature importances.
    """
    if target_col not in df.columns:
        print(f"Target column '{target_col}' not found in dataset.")
        return None

    # Drop rows where target is missing
    df = df.dropna(subset=[target_col])

    # Separate features and target
    X = df.drop(columns=[target_col])
    y = df[target_col]

    # Keep only numeric columns for now
    X = X.select_dtypes(include='number')
    id_like_cols = [col for col in X.columns if X[col].nunique() == len(X)]
    X = X.drop(columns=id_like_cols)

    if X.empty:
        print("No usable feature columns after removing ID-like columns.")
        return None

    if X.empty:
        print("No numeric feature columns available for feature importance.")
        return None

    # Detect if classification or regression
    is_classification = y.dtype == 'object' or y.nunique() < 20

    if is_classification:
        le = LabelEncoder()
        y = le.fit_transform(y.astype(str))
        model = RandomForestClassifier(n_estimators=50, random_state=42)
    else:
        model = RandomForestRegressor(n_estimators=50, random_state=42)

    model.fit(X, y)

    # Build importance dataframe
    importance_df = pd.DataFrame({
        "Feature": X.columns,
        "Importance": model.feature_importances_
    }).sort_values("Importance", ascending=False)

    # Plot
    plt.figure(figsize=(8, 4))
    plt.barh(importance_df["Feature"][:10][::-1],
             importance_df["Importance"][:10][::-1],
             color='steelblue')
    plt.title(f"Feature Importance → Target: {target_col}")
    plt.xlabel("Importance Score")
    plt.tight_layout()
    plt.savefig("feature_importance.png")
    plt.close()

    return importance_df