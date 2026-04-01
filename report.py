import matplotlib.pyplot as plt

def generate_html_report(summary, recommendations, score, label, breakdown, df):
    # -----------------------------
    # Generate missing values chart
    # -----------------------------
    missing = df.isnull().sum()
    missing = missing[missing > 0]

    if not missing.empty:
        missing.plot(kind='bar')
        plt.title("Missing Values per Column")
        plt.tight_layout()
        plt.savefig("missing.png")
        plt.close()

    # -----------------------------
    # Start HTML
    # -----------------------------
    html = f"""
    <html>
    <head>
        <title>AutoEDA Report</title>
        <style>
            body {{ font-family: Arial; margin: 40px; }}
            h1 {{ color: #2c3e50; }}
            h2 {{ color: #34495e; }}
            table {{ border-collapse: collapse; width: 60%; }}
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

    # -----------------------------
    # Column Table
    # -----------------------------
    html += "<h2>Column Overview</h2><table>"
    html += "<tr><th>Column</th><th>Type</th></tr>"

    for col, dtype in summary['dtypes'].items():
        html += f"<tr><td>{col}</td><td>{dtype}</td></tr>"

    html += "</table>"

    # -----------------------------
    # Health Score
    # -----------------------------
    html += f"""
    <h2>Health Score</h2>
    <div class="box {label.lower()}">
        <h2 style="font-size:32px;">{score}/100</h2>
        <p><b>Status:</b> {label}</p>
    </div>
    """

    # -----------------------------
    # Breakdown
    # -----------------------------
    html += "<h2>Score Breakdown</h2><ul>"
    for k, v in breakdown.items():
        html += f"<li>{k}: -{v}</li>"
    html += "</ul>"

    # -----------------------------
    # Recommendations
    # -----------------------------
    html += "<h2>Recommendations</h2><ul>"

    for r in recommendations:
        if "DROPPING" in r:
            html += f"<li style='color:red;'>{r}</li>"
        elif "convert" in r.lower():
            html += f"<li style='color:orange;'>{r}</li>"
        else:
            html += f"<li>{r}</li>"

    html += "</ul>"

    # -----------------------------
    # Next Steps (NEW)
    # -----------------------------
    html += "<h2>Next Steps</h2><ul>"

    if breakdown["object_dtype_penalty"] > 0:
        html += "<li>Convert categorical/object columns for better analysis</li>"

    if breakdown["high_cardinality_penalty"] > 0:
        html += "<li>Remove or encode ID-like columns</li>"

    if breakdown["missing_penalty"] > 0:
        html += "<li>Handle missing values (imputation or removal)</li>"

    html += "</ul>"

    # -----------------------------
    # Chart (NEW)
    # -----------------------------
    if not missing.empty:
        html += "<h2>Missing Values Chart</h2>"
        html += "<img src='missing.png' width='600'>"

    # -----------------------------
    # End HTML
    # -----------------------------
    html += """
    </body>
    </html>
    """

    with open("report.html", "w", encoding="utf-8") as f:
        f.write(html)