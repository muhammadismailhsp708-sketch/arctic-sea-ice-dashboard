# 🧊 Arctic Sea Ice Extent — Data Visualization Dashboard

**Course:** Exploratory Data Analysis  
**Instructor:** Ali Hassan Sherazi  
**Submission Date:** 05-June-2026  

---

## 📌 Project Overview

This dashboard analyzes the annual Arctic Sea Ice Extent from **1979 to 2023** using the `arctic_ice_extent.csv` dataset. It presents 10 professional chart types with fully interactive filters, KPI cards, and a clean Streamlit interface.

---

## 🚀 How to Run

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Launch the Dashboard
```bash
streamlit run app.py
```

The dashboard will open automatically at `http://localhost:8501`

---

## 📁 Project Structure

```
dashboard_project/
├── data/
│   └── arctic_ice_extent.csv       ← Dataset (exact filename, do NOT rename)
├── notebooks/
│   └── analysis.ipynb              ← EDA notebook
├── app.py                          ← Main Streamlit dashboard
├── charts.py                       ← All 10 chart functions
├── filters.py                      ← Data loading, cleaning, filter logic
├── requirements.txt                ← Python dependencies
└── README.md                       ← This file
```

---

## 📊 Charts Included

| # | Chart Type   | Insight                                      |
|---|-------------|----------------------------------------------|
| 1 | Line Chart   | Ice extent trend with 5-year rolling average |
| 2 | Area Chart   | Cumulative visual of declining ice coverage  |
| 3 | Bar Chart    | Average extent by decade                     |
| 4 | Histogram    | Frequency distribution of extent values      |
| 5 | Scatter Plot | Year vs extent with polynomial trend line    |
| 6 | Box Plot     | Spread & outliers per climate era            |
| 7 | Pie Chart    | Proportion of years above/below average      |
| 8 | Heatmap      | Feature correlation matrix                   |
| 9 | Count Plot   | Year-over-year trend direction counts        |
|10 | Violin Plot  | Extent probability density by era            |

---

## 🔍 Filter Controls

- 📅 **Year Range Slider** — Filter data by time range
- 🗂️ **Era Multi-Select** — 1980s, 1990s, 2000s, 2010s+
- 📊 **Extent Numerical Slider** — Filter by sea ice extent value
- 📈 **Trend Multi-Select** — Increase / Decrease / No Change years
- 🔎 **Year Search Box** — Jump to a specific year
- 🔄 **Reset Filters** — Restore all defaults

All filters update all charts simultaneously.

---

## 💡 Key Insights

- Arctic sea ice has declined by approximately **2.5 million km²** from 1979 to 2023.
- The record minimum was recorded in **2012** at just **3.387 million km²**.
- A clear accelerating downward trend is visible from the **2000s onward**.
- About **65%** of years (post-2000) recorded below-average ice extent.
- Year-over-year changes show high volatility but a consistent negative mean trend.

---

## 📦 Dataset

- **File:** `data/arctic_ice_extent.csv`  
- **Columns:** `year` (int), `extent` (float — million km²)  
- **Source:** NSIDC (National Snow and Ice Data Center)
