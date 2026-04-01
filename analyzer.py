def analyze(df):
    summary = {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "missing_values": df.isnull().sum().to_dict(),
        "dtypes": df.dtypes.astype(str).to_dict(),
        "duplicates": int(df.duplicated().sum()),
        "correlations": df.select_dtypes(include='number').corr().round(2).to_dict()
    }
    return summary