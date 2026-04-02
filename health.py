def compute_health_score(df):
    """
    Computes a dataset health score from 0-100.
    Returns: (score, label, breakdown)
    """
    score = 100
    total_rows = df.shape[0]
    total_cols = df.shape[1]

    breakdown = {}


    missing_penalty = 0

    for col in df.columns:
        col_missing_ratio = df[col].isnull().mean()

        if col_missing_ratio > 0:
            if "id" in col.lower():
                weight = 0.5
            else:
                weight = 1.5

            missing_penalty += col_missing_ratio * 20 * weight

    score -= missing_penalty
    breakdown["missing_penalty"] = round(missing_penalty, 2)

    duplicates = df.duplicated().sum()
    duplicate_ratio = duplicates / total_rows
    duplicate_penalty = duplicate_ratio * 20

    score -= duplicate_penalty
    breakdown["duplicate_penalty"] = round(duplicate_penalty, 2)

    high_card_cols = sum(df[col].nunique() == total_rows for col in df.columns)
    high_card_penalty = (high_card_cols / total_cols) * 40

    score -= high_card_penalty
    breakdown["high_cardinality_penalty"] = round(high_card_penalty, 2)

    numeric_looking_objects = 0
    for col in df.columns:
        if df[col].dtype == 'object':
            try:
                df[col].dropna().astype(float)
                numeric_looking_objects += 1
            except (ValueError, TypeError):
                pass

    object_penalty = (numeric_looking_objects / total_cols) * 15
    score -= object_penalty
    breakdown["object_dtype_penalty"] = round(object_penalty, 2)

    score = max(0, round(score, 2))

    if score >= 85:
        label = "Good"
    elif score >= 60:
        label = "Moderate"
    else:
        label = "Poor"

    return score, label, breakdown
