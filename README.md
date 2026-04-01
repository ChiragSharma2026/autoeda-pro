# 📊 AutoEDA — Automated Dataset Analysis & Quality Scoring

AutoEDA is a lightweight tool that automatically analyzes datasets, evaluates data quality, and generates a clean HTML report with actionable insights.

---

## 🚀 Features

* 📦 Load and analyze CSV datasets instantly
* 📊 Dataset summary (rows, columns, duplicates, data types)
* ⚠️ Automatic issue detection:

  * Missing values
  * ID-like columns
  * Incorrect data types (e.g., dates as strings)
* 🧠 Smart recommendations for data cleaning
* 📈 Dataset Health Score (0–100) with breakdown
* 📝 Export-ready HTML report with visualization

---

## 🧠 Example Output

* Health Score: **89.41 / 100 (Good)**
* Identified issues:

  * ID columns detected
  * Date columns not parsed
  * Missing values in dataset

---

## 📸 Report Preview

![Report Preview](report-preview.png)

---

## ⚙️ Installation

```bash
git clone https://github.com/ChiragSharma2026/autoeda-pro.git
cd autoeda-pro
pip install pandas matplotlib
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
│── analyzer.py          # Dataset analysis
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

* Correlation heatmaps
* Advanced feature importance
* CLI packaging
* Web dashboard

---

## 👨‍💻 Author

Chirag Sharma
BTech CSE | Data Analytics & ML Enthusiast
