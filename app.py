"""
Arctic Sea Ice Extent Dashboard
================================
Course  : Exploratory Data Analysis
Instructor: Ali Hassan Sherazi
Dataset : arctic_ice_extent.csv  (exact file name retained)
Framework: Streamlit
"""

import os
import streamlit as st
import pandas as pd

from filters import load_data, apply_filters
from charts import (
    chart_pie, chart_histogram, chart_line, chart_bar,
    chart_scatter, chart_box, chart_heatmap, chart_area,
    chart_count, chart_violin, chart_pair
)

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="🌊 Arctic Ice Dashboard",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #f4f8fc; }
    .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }
    .kpi-card {
        background: white;
        border-radius: 12px;
        padding: 18px 24px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(26,111,168,0.10);
        border-left: 5px solid #1a6fa8;
    }
    .kpi-value { font-size: 2rem; font-weight: 700; color: #1a6fa8; }
    .kpi-label { font-size: 0.85rem; color: #666; margin-top: 4px; }
    .section-header {
        font-size: 1.15rem; font-weight: 700; color: #1a6fa8;
        border-bottom: 2px solid #1a6fa8; padding-bottom: 4px;
        margin-bottom: 16px; margin-top: 8px;
    }
</style>
""", unsafe_allow_html=True)

# ── Load Data ─────────────────────────────────────────────────────────────────
DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "arctic_ice_extent.csv")

@st.cache_data
def get_data():
    return load_data(DATA_PATH)

df_full = get_data()

# ── SIDEBAR — Filters ─────────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/1/18/Simple_snowflake.svg/120px-Simple_snowflake.svg.png", width=60)
    st.title("🔍 Dashboard Filters")
    st.markdown("---")

    # 1. Year Range (Date/Time analogue)
    st.subheader("📅 Year Range")
    year_min, year_max = int(df_full["year"].min()), int(df_full["year"].max())
    year_range = st.slider("Select Year Range", year_min, year_max, (year_min, year_max))

    st.markdown("---")

    # 2. Category filter (dropdown)
    st.subheader("🏷️ Extent Category")
    all_cats = df_full["extent_category"].unique().tolist()
    selected_cats = st.multiselect("Select Categories", all_cats, default=all_cats)

    st.markdown("---")

    # 3. Numerical Range Slider
    st.subheader("📊 Extent Range (million km²)")
    ext_min = float(df_full["extent"].min())
    ext_max = float(df_full["extent"].max())
    extent_range = st.slider("Extent Range", ext_min, ext_max,
                              (ext_min, ext_max), step=0.1)

    st.markdown("---")

    # 4. Multi-Select (Era)
    st.subheader("🕰️ Era")
    all_eras = ["Pre-1990", "1990s", "2000s", "2010s+"]
    available_eras = [e for e in all_eras if e in df_full["era"].unique()]
    selected_eras = st.multiselect("Select Eras", available_eras, default=available_eras)

    st.markdown("---")

    # 5. Search / Text Filter
    st.subheader("🔎 Search")
    search_text = st.text_input("Filter by year / era / decade", placeholder="e.g. 2000 or 1990s")

    st.markdown("---")

    # 6. Reset Button
    if st.button("🔄 Reset All Filters", use_container_width=True):
        st.rerun()

    st.markdown("---")
    st.caption("📁 Dataset: arctic_ice_extent.csv\n\n🎓 EDA Project — Ali Hassan Sherazi")

# ── Apply Filters ─────────────────────────────────────────────────────────────
df = apply_filters(
    df_full,
    year_range=year_range,
    selected_eras=selected_eras,
    extent_range=extent_range,
    selected_categories=selected_cats,
    search_text=search_text
)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<h1 style='text-align:center; color:#1a6fa8; margin-bottom:4px;'>
🧊 Arctic Sea Ice Extent Dashboard
</h1>
<p style='text-align:center; color:#555; font-size:1rem; margin-bottom:24px;'>
Exploratory Data Analysis of Arctic Sea Ice from 1979 to 2023 | Course: EDA | Instructor: Ali Hassan Sherazi
</p>
""", unsafe_allow_html=True)

# ── KPI Cards ─────────────────────────────────────────────────────────────────
if df.empty:
    st.warning("⚠️ No data matches the current filters. Please adjust the filters.")
    st.stop()

k1, k2, k3, k4, k5 = st.columns(5)
with k1:
    st.markdown(f"""<div class="kpi-card">
        <div class="kpi-value">{len(df)}</div>
        <div class="kpi-label">Total Records</div>
    </div>""", unsafe_allow_html=True)
with k2:
    st.markdown(f"""<div class="kpi-card">
        <div class="kpi-value">{df['extent'].mean():.2f}</div>
        <div class="kpi-label">Avg Extent (M km²)</div>
    </div>""", unsafe_allow_html=True)
with k3:
    max_row = df.loc[df["extent"].idxmax()]
    st.markdown(f"""<div class="kpi-card">
        <div class="kpi-value">{max_row['extent']:.2f}</div>
        <div class="kpi-label">Highest ({int(max_row['year'])})</div>
    </div>""", unsafe_allow_html=True)
with k4:
    min_row = df.loc[df["extent"].idxmin()]
    st.markdown(f"""<div class="kpi-card">
        <div class="kpi-value">{min_row['extent']:.2f}</div>
        <div class="kpi-label">Lowest ({int(min_row['year'])})</div>
    </div>""", unsafe_allow_html=True)
with k5:
    trend = df["extent"].iloc[-1] - df["extent"].iloc[0] if len(df) > 1 else 0
    arrow = "📉" if trend < 0 else "📈"
    st.markdown(f"""<div class="kpi-card">
        <div class="kpi-value">{trend:+.2f}</div>
        <div class="kpi-label">Overall Change {arrow}</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Section 1: Trends ─────────────────────────────────────────────────────────
st.markdown('<div class="section-header">📈 Temporal Trends</div>', unsafe_allow_html=True)
col1, col2 = st.columns([2, 1])
with col1:
    st.markdown("**Line Chart — Extent Over Time**")
    st.pyplot(chart_line(df), use_container_width=True)
with col2:
    st.markdown("**Pie Chart — Category Distribution**")
    st.pyplot(chart_pie(df), use_container_width=True)

st.markdown("---")

# ── Section 2: Distributions ──────────────────────────────────────────────────
st.markdown('<div class="section-header">📊 Distributions</div>', unsafe_allow_html=True)
col3, col4 = st.columns(2)
with col3:
    st.markdown("**Histogram — Extent Frequency**")
    st.pyplot(chart_histogram(df), use_container_width=True)
with col4:
    st.markdown("**Area Chart — Cumulative Trend**")
    st.pyplot(chart_area(df), use_container_width=True)

st.markdown("---")

# ── Section 3: Comparisons ────────────────────────────────────────────────────
st.markdown('<div class="section-header">📋 Comparisons by Era & Decade</div>', unsafe_allow_html=True)
col5, col6 = st.columns(2)
with col5:
    st.markdown("**Bar Chart — Average by Decade**")
    st.pyplot(chart_bar(df), use_container_width=True)
with col6:
    st.markdown("**Count Plot — Observations per Era**")
    st.pyplot(chart_count(df), use_container_width=True)

st.markdown("---")

# ── Section 4: Statistical Analysis ──────────────────────────────────────────
st.markdown('<div class="section-header">🔬 Statistical Analysis</div>', unsafe_allow_html=True)
col7, col8 = st.columns(2)
with col7:
    st.markdown("**Box Plot — Spread by Era**")
    st.pyplot(chart_box(df), use_container_width=True)
with col8:
    st.markdown("**Violin Plot — Distribution Density by Era**")
    st.pyplot(chart_violin(df), use_container_width=True)

st.markdown("---")

# ── Section 5: Correlations ───────────────────────────────────────────────────
st.markdown('<div class="section-header">🔗 Correlations & Relationships</div>', unsafe_allow_html=True)
col9, col10 = st.columns(2)
with col9:
    st.markdown("**Scatter Plot — Year vs Extent (Trend Line)**")
    st.pyplot(chart_scatter(df), use_container_width=True)
with col10:
    st.markdown("**Heatmap — Feature Correlation Matrix**")
    st.pyplot(chart_heatmap(df), use_container_width=True)

st.markdown("---")

# ── Section 6: Bonus ──────────────────────────────────────────────────────────
with st.expander("🎁 Bonus: Pair Plot (Click to Expand)", expanded=False):
    st.markdown("**Pair Plot — All Key Features**")
    if len(df) >= 5:
        st.pyplot(chart_pair(df), use_container_width=True)
    else:
        st.info("Not enough data points for Pair Plot with current filters.")

st.markdown("---")

# ── Section 7: Raw Data Table ─────────────────────────────────────────────────
with st.expander("📄 View Filtered Data Table", expanded=False):
    st.dataframe(df.reset_index(drop=True), use_container_width=True)
    st.caption(f"Showing {len(df)} records after filters applied.")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<hr>
<p style='text-align:center; color:#999; font-size:0.8rem;'>
🧊 Arctic Sea Ice Dashboard &nbsp;|&nbsp; Dataset: arctic_ice_extent.csv &nbsp;|&nbsp;
Built with Streamlit, Pandas, Matplotlib & Seaborn &nbsp;|&nbsp; EDA Course
</p>
""", unsafe_allow_html=True)
