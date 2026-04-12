import argparse
import pandas as pd
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from analyzer import analyze
from recommendations import generate_recommendations
from health import compute_health_score
from report import generate_html_report

def main():
    parser = argparse.ArgumentParser(
        description="AutoEDA — Automated Dataset Analysis Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  autoeda data.csv
  autoeda data.csv --target Survived
  autoeda data.csv --target Price --output my_report.html
        """
    )
    parser.add_argument("file", help="Path to CSV file")
    parser.add_argument("--target", help="Target column for feature importance", default=None)
    parser.add_argument("--output", help="Output report filename", default="report.html")

    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"Error: File '{args.file}' not found.")
        sys.exit(1)

    print(f"\n📊 AutoEDA — Analyzing {args.file}...\n")

    df = pd.read_csv(args.file)
    print(f"✅ Loaded: {df.shape[0]} rows, {df.shape[1]} columns")

    summary = analyze(df)
    recs = generate_recommendations(df)
    health_score, label, breakdown = compute_health_score(df)

    print(f"\n📈 Health Score: {health_score}/100 ({label})")

    print("\n🧠 Recommendations:")
    for r in recs:
        print(f"  - {r}")

    print("\n📊 Score Breakdown:")
    for k, v in breakdown.items():
        print(f"  {k}: -{v}")

    generate_html_report(summary, recs, health_score, label, breakdown, df, target=args.target)
    print(f"\n✅ Report saved as {args.output}")
    print(f"   Open {args.output} in your browser to view the full report.\n")

if __name__ == "__main__":
    main()