def compute_health_score(df):
    score = 100
    total_rows = df.shape[0]
    total_cols = df.shape[1]

    breakdown = {}

    # -----------------------------
    # Missing values penalty (column-wise)
    # -----------------------------
    missing_penalty = 0

    for col in df.columns:
        col_missing_ratio = df[col].isnull().mean()

        if col_missing_ratio > 0:
            weight = 1

            # Reduce importance for ID-like columns
            if "id" not in col.lower():
                weight = 1.5

            missing_penalty += col_missing_ratio * 20 * weight

    score -= missing_penalty
    breakdown["missing_penalty"] = round(missing_penalty, 2)

    # -----------------------------
    # Duplicate rows penalty
    # -----------------------------
    duplicates = df.duplicated().sum()
    duplicate_ratio = duplicates / total_rows
    duplicate_penalty = duplicate_ratio * 20

    score -= duplicate_penalty
    breakdown["duplicate_penalty"] = round(duplicate_penalty, 2)

    # -----------------------------
    # High cardinality penalty (ID-like columns)
    # -----------------------------
    high_card_cols = sum(df[col].nunique() == total_rows for col in df.columns)
    high_card_penalty = (high_card_cols / total_cols) * 40

    score -= high_card_penalty
    breakdown["high_cardinality_penalty"] = round(high_card_penalty, 2)

    # -----------------------------
    # Object dtype penalty (unprocessed data)
    # -----------------------------
    object_cols = sum(df[col].dtype == 'object' for col in df.columns)
    object_penalty = (object_cols / total_cols) * 10

    score -= object_penalty
    breakdown["object_dtype_penalty"] = round(object_penalty, 2)

    # -----------------------------
    # Final score clamp
    # -----------------------------
    score = max(0, round(score, 2))

    # -----------------------------
    # Label interpretation
    # -----------------------------
    if score >= 85:
        label = "Good"
    elif score >= 60:
        label = "Moderate"
    else:
        label = "Poor"

    return score, label, breakdown