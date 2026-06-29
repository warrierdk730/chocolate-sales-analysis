# 🍫 Chocolate Sales Analysis (2022–2024)

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.0+-150458?logo=pandas&logoColor=white)
![Seaborn](https://img.shields.io/badge/Seaborn-Visualization-4c72b0)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?logo=streamlit&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?logo=jupyter&logoColor=white)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen)

> **End-to-end exploratory data analysis of chocolate sales across 6 countries, 22 products, and 25 salespeople — uncovering revenue trends, product profitability, and salesperson selling strategies from 3,282 transactions over 2.5 years.**

---

## 📊 Live Dashboard

👉 **[Open the Streamlit Dashboard](https://warrierdk730-chocolate-sales.streamlit.app)**


---

## 📌 Project Overview

| Detail | Value |
|--------|-------|
| **Dataset** | Chocolate Sales — Kaggle |
| **Period** | January 2022 – August 2024 |
| **Records** | 3,282 transactions |
| **Countries** | 6 (Australia, Canada, India, New Zealand, UK, USA) |
| **Products** | 22 chocolate product lines |
| **Salespeople** | 25 |
| **Total Revenue** | $19.79M |
| **Total Boxes Shipped** | 540,437 |

---

## 🎯 Business Questions Answered

1. **Which salespeople generate the most revenue — and how?** (volume strategy vs premium strategy)
2. **Which products are the most profitable per box shipped?**
3. **How is revenue distributed across countries?**
4. **Is the business growing year-over-year?** (2022 → 2023 → 2024)
5. **Are there seasonal patterns in chocolate sales?**
6. **What are the actionable recommendations for the sales team?**

---

## 🔑 Key Findings

- 📈 **Revenue grew +7.4%** from 2022 ($6.18M) to 2023 ($6.64M), with 2024 tracking ahead of 2023
- 🌍 **Markets are well-balanced** — all 6 countries contribute 15.7%–17.3% each; no dangerous dependency on a single market
- 🏆 **Top salesperson:** Ches Bonnell at $1.02M total revenue
- 🍫 **Top revenue product:** Smooth Sliky Salty ($1.12M) — but **Almond Choco** leads on profitability at $43.31/box
- 📦 **Selling strategy matters more than volume** — correlation between boxes shipped and revenue is moderate; premium sellers outperform high-volume sellers in revenue per box
- ⚠️ **Caramel Stuffed Bars** and **70% Dark Bites** rank bottom on both total revenue and profitability — candidates for strategic review

---

## 📁 Project Structure

```
chocolate-sales-analysis/
│
├── Chocolate_Sales.csv              # Raw dataset
├── Chocolate_Sales_Analysis.ipynb   # Full analysis notebook (9 sections)
├── app.py                           # Streamlit dashboard
├── requirements.txt                 # Python dependencies
│
├── charts/                          # Auto-generated chart PNGs
│   ├── 01_eda_distributions.png
│   ├── 02_salesperson_revenue.png
│   ├── 03_product_analysis.png
│   ├── 04_geographic_analysis.png
│   ├── 05_salesperson_strategy.png
│   └── 06_yoy_trends.png
│
└── README.md
```

---

## 📓 Notebook Sections

| # | Section | Description |
|---|---------|-------------|
| 1 | Setup & Data Loading | Import libraries, load and preview dataset |
| 2 | Data Cleaning | Fix Amount format, parse dates, type conversion, outlier check |
| 3 | Exploratory Data Analysis | Distribution plots, summary statistics |
| 4 | Sales Performance | All 25 salespeople ranked by total revenue |
| 5 | Product Analysis | Revenue totals + revenue per box (profitability) |
| 6 | Geographic Analysis | Country revenue breakdown with pie and bar charts |
| 7 | Salesperson Strategy | Volume vs premium selling strategy quadrant map |
| 8 | Year-over-Year Trends | Monthly timeline, seasonal pattern, quarterly breakdown |
| 9 | Key Findings & Recommendations | Business summary, insights, and action items |

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| **Python 3.10+** | Core language |
| **Pandas** | Data loading, cleaning, groupby analysis |
| **NumPy** | Numerical operations |
| **Matplotlib** | Base chart rendering |
| **Seaborn** | Statistical visualizations |
| **Streamlit** | Interactive dashboard |
| **Jupyter Notebook** | Analysis environment |

---

## 🚀 How to Run

### 1. Clone the repository
```bash
git clone https://github.com/warrierdk730/chocolate-sales-analysis.git
cd chocolate-sales-analysis
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Jupyter notebook
```bash
jupyter notebook Chocolate_Sales_Analysis.ipynb
```

### 4. Launch the Streamlit dashboard
```bash
streamlit run app.py
```

---

## 📦 Requirements

```
pandas>=2.0
numpy>=1.24
matplotlib>=3.7
seaborn>=0.12
streamlit>=1.30
plotly>=5.18
```

---

## 💡 Skills Demonstrated

- ✅ Real-world **data cleaning** (currency strings, date parsing, type coercion)
- ✅ **Exploratory Data Analysis** with statistical interpretation
- ✅ **Business-focused analysis** — every chart answers a business question
- ✅ **Segmentation analysis** — salesperson strategy quadrant mapping
- ✅ **Time-series analysis** — YoY growth, seasonal patterns, quarterly trends
- ✅ **Data storytelling** — markdown insights after every visualization
- ✅ **Interactive dashboard** deployment with Streamlit

---

## 👤 Author

**Dileep Kumar Warrier**
- 📧 warrierdk.1985@gmail.com
- 💼 [LinkedIn](https://linkedin.com/in/your-profile)
- 🐙 [GitHub](https://github.com/warrierdk730)

---

## 📄 Dataset Source

[Chocolate Sales Dataset — Kaggle](https://www.kaggle.com/)  
*Data covers January 2022 to August 2024. 2024 figures represent a partial year (Jan–Aug only).*

---

*⭐ If you found this analysis useful, please star the repository!*
