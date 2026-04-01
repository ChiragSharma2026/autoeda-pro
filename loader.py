import pandas as pd
import sys
from analyzer import analyze
from recommendations import generate_recommendations
from health import compute_health_score
from report import generate_html_report

def load_csv(path):
    df = pd.read_csv(path)
    print(f"Loaded: {df.shape[0]} rows, {df.shape[1]} columns")
    return df

if __name__ == "__main__":
    df = load_csv(sys.argv[1])
    summary = analyze(df)

    print("\n--- Dataset Summary ---")
    for key, value in summary.items():
        print(f"{key}: {value}")

    recs = generate_recommendations(df)

    print("\n--- Recommendations ---")
    for r in recs:
        print("-", r)

    health_score, label, breakdown = compute_health_score(df)

    print("\n--- Dataset Health Score ---")
    print(f"Score: {health_score}/100 ({label})")

    print("\n--- Score Breakdown ---")
    for k, v in breakdown.items():
        print(f"{k}: -{v}")

    generate_html_report(summary, recs, health_score, label, breakdown, df)
    print("\nReport saved as report.html")