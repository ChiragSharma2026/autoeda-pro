# 📊 AutoEDA — Automated Dataset Analysis & Quality Scoring

AutoEDA is a lightweight tool that automatically analyzes datasets, evaluates data quality, and generates a clean HTML report with actionable insights.

---

## 🚀 Features

* 📦 Load and analyze CSV datasets instantly
* 📊 Dataset summary (rows, columns, duplicates, data types)
* ⚠️ Automatic issue detection:
  * Missing values (with significance threshold)
  * ID-like columns
  * Incorrect data types (e.g., dates as strings, numeric-looking objects)
* 🧠 Smart recommendations for data cleaning
* 📈 Dataset Health Score (0–100) with penalty breakdown
* 🔗 Correlation table for numeric columns (highlights strong correlations)
* 📝 Export-ready HTML report

---

## 🧠 Example Output

* Health Score: **97.74 / 100 (Good)**
* Identified issues:
  * ID columns detected
  * Date columns not parsed
  * Minor missing values in Postal Code (0.11%)

---

## 📸 Report Preview

![Report Preview](report-preview.png)

---

## ⚙️ Installation
```bash
git clone https://github.com/ChiragSharma2026/autoeda-pro.git
cd autoeda-pro
pip install pandas matplotlib scikit-learn
```

---

## ▶️ Usage
```bash
python loader.py your_dataset.csv
```

👉 This generates:

* `report.html` (open in browser)

---

## 📁 Project Structure
```
autoeda-pro/
│── loader.py            # Main entry point
│── analyzer.py          # Dataset analysis + correlations
│── recommendations.py   # Suggestions engine
│── health.py            # Scoring system
│── report.py            # HTML report generator
```

---

## 🎯 Why this project?

Most EDA tools give statistics.

AutoEDA focuses on:
👉 **actionable insights + dataset quality scoring**

---

## 🚧 Future Improvements

* Distribution charts per column
* CLI packaging (`pip install autoeda-pro`)
* Feature importance (target column detection)
* Web dashboard

---

## 👨‍💻 Author

**Chirag Sharma**
BTech CSE | Data Analytics & ML Enthusiast
