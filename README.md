# 🧊 Arctic Sea Ice Extent Dashboard

**Course:** Exploratory Data Analysis  
**Instructor:** Ali Hassan Sherazi  
**Dataset:** `1780679221796_arctic_ice_extent.csv` (1979–2023, annual Arctic sea ice extent)

---

## 📁 Project Structure

```
dashboard_project/
├── data/
│   └── 1780679221796_arctic_ice_extent.csv   ← DO NOT RENAME
├── notebooks/
│   └── analysis.ipynb                         ← EDA notebook (optional)
├── app.py          ← Main Streamlit dashboard
├── charts.py       ← All chart/visualization functions
├── filters.py      ← Data loading, cleaning, filtering logic
├── requirements.txt
└── README.md
```

---

## 🚀 How to Run

### 1. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 2. Launch the dashboard

```bash
streamlit run app.py
```

The dashboard will open automatically at `http://localhost:8501`

---

## 📊 Charts Included

| # | Chart Type    | Purpose                                    |
|---|---------------|--------------------------------------------|
| 1 | Line Chart    | Annual trend with 5-year rolling average   |
| 2 | Area Chart    | Filled cumulative view with mean line       |
| 3 | Bar Chart     | Average ice extent per decade              |
| 4 | Histogram     | Frequency distribution of extent values    |
| 5 | Scatter Plot  | Year vs. extent with trendline             |
| 6 | Box Plot      | Spread and outliers by era                 |
| 7 | Pie Chart     | Proportion above vs. below historical mean |
| 8 | Heatmap       | Decade-wise stats (mean, min, max, std)    |
| 9 | Count Plot    | Records per decade                         |
|10 | Violin Plot   | Distribution density by era                |
| ★ | Bonus: YoY    | Year-over-year change bar chart            |

---

## 🎛️ Filters (all linked to every chart)

| Filter Type         | Description                                |
|---------------------|--------------------------------------------|
| Year Range Slider   | Restrict data to a selected year range     |
| Extent Range Slider | Filter by numerical extent values          |
| Decade Dropdown     | Multi-select one or more decades           |
| Era Multi-Select    | Filter by 1980s / 1990s / 2000s / 2010s+  |
| Text Search         | Search by year keyword                     |
| Reset Button        | Clear all filters to default               |

---

## 💡 Key Insights

- **Dramatic decline:** Arctic sea ice extent has dropped from ~7.5 million km² in the 1980s to under 4.5 million km² in recent years.
- **Record low:** 2012 saw the smallest extent on record at **3.387 million km²**.
- **Acceleration:** The rate of loss has increased since the 2000s, visible in the trendline slope of approximately **−0.06 million km² per year**.
- **Era shift:** Box plots clearly show a statistically significant downward shift between the 1980s era and the 2010s+ era.
- **Variability:** Despite the overall trend, year-to-year variability remains high, as shown by the violin and YoY charts.

---

## 🛠️ Tech Stack

| Tool        | Role                            |
|-------------|---------------------------------|
| Python 3.x  | Core language                   |
| Pandas      | Data loading, cleaning, filters |
| NumPy       | Numerical operations            |
| Matplotlib  | Core chart rendering            |
| Seaborn     | Statistical visualizations      |
| Streamlit   | Interactive dashboard frontend  |
