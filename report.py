import matplotlib.pyplot as plt

def generate_html_report(summary, recommendations, score, label, breakdown, df):

    # Missing values chart
    missing = df.isnull().sum()
    missing = missing[missing > 0]

    if not missing.empty:
        missing.plot(kind='bar')
        plt.title("Missing Values per Column")
        plt.tight_layout()
        plt.savefig("missing.png")
        plt.close()

    # Distribution charts for numeric columns
    numeric_cols = df.select_dtypes(include='number').columns
    for col in numeric_cols:
        plt.figure()
        df[col].dropna().hist(bins=30, color='steelblue', edgecolor='white')
        plt.title(f"Distribution: {col}")
        plt.xlabel(col)
        plt.ylabel("Frequency")
        plt.tight_layout()
        plt.savefig(f"dist_{col}.png")
        plt.close()

    html = f"""
    <html>
    <head>
        <title>AutoEDA Report</title>
        <style>
            body {{ font-family: Arial; margin: 40px; }}
            h1 {{ color: #2c3e50; }}
            h2 {{ color: #34495e; }}
            h3 {{ color: #555; }}
            table {{ border-collapse: collapse; width: 80%; margin-bottom: 20px; }}
            th, td {{ border: 1px solid #ccc; padding: 8px; text-align: left; }}
            th {{ background-color: #f2f2f2; }}
            .box {{ padding: 15px; border-radius: 8px; margin-bottom: 20px; }}
            .good {{ background-color: #d4edda; }}
            .moderate {{ background-color: #fff3cd; }}
            .poor {{ background-color: #f8d7da; }}
        </style>
    </head>
    <body>

    <h1>📊 AutoEDA Report</h1>
    <p>Automated Dataset Analysis & Quality Assessment</p>

    <h2>Dataset Summary</h2>
    <div class="box">
        <p><b>Rows:</b> {summary['rows']}</p>
        <p><b>Columns:</b> {summary['columns']}</p>
        <p><b>Duplicates:</b> {summary['duplicates']}</p>
    </div>
    """

    # Column table
    html += "<h2>Column Overview</h2><table>"
    html += "<tr><th>Column</th><th>Type</th></tr>"
    for col, dtype in summary['dtypes'].items():
        html += f"<tr><td>{col}</td><td>{dtype}</td></tr>"
    html += "</table>"

    # Health score
    html += f"""
    <h2>Health Score</h2>
    <div class="box {label.lower()}">
        <h2 style="font-size:32px;">{score}/100</h2>
        <p><b>Status:</b> {label}</p>
    </div>
    """

    # Score breakdown
    html += "<h2>Score Breakdown</h2><ul>"
    for k, v in breakdown.items():
        html += f"<li>{k}: -{v}</li>"
    html += "</ul>"

    # Recommendations
    html += "<h2>Recommendations</h2><ul>"
    for r in recommendations:
        if "DROPPING" in r:
            html += f"<li style='color:red;'>{r}</li>"
        elif "convert" in r.lower():
            html += f"<li style='color:orange;'>{r}</li>"
        else:
            html += f"<li>{r}</li>"
    html += "</ul>"

    # Next steps
    html += "<h2>Next Steps</h2><ul>"
    if breakdown["object_dtype_penalty"] > 0:
        html += "<li>Convert categorical/object columns for better analysis</li>"
    if breakdown["high_cardinality_penalty"] > 0:
        html += "<li>Remove or encode ID-like columns</li>"
    if breakdown["missing_penalty"] > 0:
        html += "<li>Handle missing values (imputation or removal)</li>"
    html += "</ul>"

    # Missing values
    significant_missing = missing[missing > df.shape[0] * 0.01]
    if not significant_missing.empty:
        html += "<h2>Missing Values Chart</h2>"
        html += "<img src='missing.png' width='600'>"
    else:
        html += "<h2>Missing Values</h2><p style='color:green;'>✅ No significant missing values detected.</p>"

    # Correlation table
    corr = summary.get("correlations", {})
    if corr:
        numeric_cols_list = list(corr.keys())
        html += "<h2>Correlation Table (Numeric Columns)</h2>"
        html += "<table><tr><th>Column</th>"
        for col in numeric_cols_list:
            html += f"<th>{col}</th>"
        html += "</tr>"
        for row_col in numeric_cols_list:
            html += f"<tr><td><b>{row_col}</b></td>"
            for col in numeric_cols_list:
                val = corr[col].get(row_col, "")
                try:
                    fval = float(val)
                    if abs(fval) > 0.7 and fval != 1.0:
                        html += f"<td style='background:#f8d7da;'>{fval}</td>"
                    else:
                        html += f"<td>{fval}</td>"
                except:
                    html += f"<td>{val}</td>"
            html += "</tr>"
        html += "</table>"

    # Distribution charts
    html += "<h2>📊 Distributions (Numeric Columns)</h2>"
    for col in numeric_cols:
        html += f"<h3>{col}</h3>"
        html += f"<img src='dist_{col}.png' width='500'><br><br>"

    html += """
    </body>
    </html>
    """

    with open("report.html", "w", encoding="utf-8") as f:
        f.write(html)