import streamlit as st
import pandas as pd
import numpy as np

from filters import load_data, apply_filters, get_kpis
from charts import (
    line_chart, area_chart, bar_chart, histogram,
    scatter_plot, box_plot, pie_chart, heatmap,
    count_plot, violin_plot
)

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Arctic Sea Ice Dashboard",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #F0F4F8; }
    .block-container { padding-top: 1.5rem; }
    .kpi-card {
        background: white;
        border-radius: 10px;
        padding: 16px 20px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border-top: 4px solid #1565C0;
    }
    .kpi-value { font-size: 28px; font-weight: 700; color: #1565C0; }
    .kpi-label { font-size: 12px; color: #607D8B; margin-top: 4px; }
    .section-header {
        font-size: 16px; font-weight: 700;
        color: #1A237E; margin-top: 1rem;
        border-bottom: 2px solid #1565C0;
        padding-bottom: 4px;
    }
</style>
""", unsafe_allow_html=True)

# ── Load Data ─────────────────────────────────────────────────────────────────
df = load_data("arctic_ice_extent[1].csv")

# ── SIDEBAR FILTERS ───────────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/4/41/Arctic_Sea_ice_loss_animation.gif/240px-Arctic_Sea_ice_loss_animation.gif",
             use_container_width=True, caption="Arctic Sea Ice")
    st.markdown("## 🔍 Dashboard Filters")
    st.markdown("---")

    # 1. Year range filter (Date/Time Range)
    min_yr, max_yr = int(df['year'].min()), int(df['year'].max())
    year_range = st.slider("📅 Year Range", min_yr, max_yr, (min_yr, max_yr))

    # 2. Era multi-select filter
    all_eras = df['era'].dropna().unique().tolist()
    era_filter = st.multiselect("🗂️ Filter by Era", options=all_eras, default=all_eras)

    # 3. Extent numerical range slider
    min_ext = float(df['extent'].min())
    max_ext = float(df['extent'].max())
    extent_range = st.slider("📊 Extent Range (million km²)",
                             min_ext, max_ext, (min_ext, max_ext), step=0.1)

    # 4. Trend multi-select
    all_trends = df['trend'].dropna().unique().tolist()
    trend_filter = st.multiselect("📈 Year-over-Year Trend", options=all_trends, default=all_trends)

    # 5. Search / Text filter
    search_year = st.text_input("🔎 Search by Year (e.g. 2012)", value="")

    # 6. Reset button
    if st.button("🔄 Reset All Filters"):
        st.rerun()

    st.markdown("---")
    st.caption("Data: NSIDC Arctic Sea Ice Extent\n1979–2023 | Annual September Minimum")

# ── Apply Filters ─────────────────────────────────────────────────────────────
filtered = apply_filters(df, year_range, era_filter, extent_range, search_year)

# Apply trend filter
if trend_filter:
    filtered = filtered[filtered['trend'].isin(trend_filter)]

# ── HEADER ────────────────────────────────────────────────────────────────────
st.markdown("""
<h1 style='color:#1A237E; margin-bottom:0;'>🧊 Arctic Sea Ice Extent Dashboard</h1>
<p style='color:#607D8B; font-size:15px; margin-top:4px;'>
Exploratory Data Analysis of annual Arctic sea ice extent (million km²) from 1979 to 2023.
Track the alarming decline in polar ice coverage due to climate change.
</p>
""", unsafe_allow_html=True)
st.markdown("---")

# ── KPI CARDS ─────────────────────────────────────────────────────────────────
kpis = get_kpis(df, filtered)
c1, c2, c3, c4, c5, c6 = st.columns(6)

with c1:
    st.markdown(f"""<div class="kpi-card">
        <div class="kpi-value">{kpis['total_records']}</div>
        <div class="kpi-label">📋 Total Records</div></div>""", unsafe_allow_html=True)
with c2:
    st.markdown(f"""<div class="kpi-card">
        <div class="kpi-value">{kpis['avg_extent']}</div>
        <div class="kpi-label">📊 Avg Extent (km²M)</div></div>""", unsafe_allow_html=True)
with c3:
    st.markdown(f"""<div class="kpi-card" style="border-top-color:#42A5F5;">
        <div class="kpi-value" style="color:#42A5F5;">{kpis['max_extent']}</div>
        <div class="kpi-label">🔼 Max Extent ({kpis['max_year']})</div></div>""", unsafe_allow_html=True)
with c4:
    st.markdown(f"""<div class="kpi-card" style="border-top-color:#EF5350;">
        <div class="kpi-value" style="color:#EF5350;">{kpis['min_extent']}</div>
        <div class="kpi-label">🔽 Min Extent ({kpis['min_year']})</div></div>""", unsafe_allow_html=True)
with c5:
    trend_color = "#EF5350" if kpis['overall_trend'] < 0 else "#42A5F5"
    trend_icon = "📉" if kpis['overall_trend'] < 0 else "📈"
    st.markdown(f"""<div class="kpi-card" style="border-top-color:{trend_color};">
        <div class="kpi-value" style="color:{trend_color};">{kpis['overall_trend']}</div>
        <div class="kpi-label">{trend_icon} Avg YoY Change</div></div>""", unsafe_allow_html=True)
with c6:
    total_decline = round(filtered['extent'].iloc[-1] - filtered['extent'].iloc[0], 3) if len(filtered) > 1 else 0
    st.markdown(f"""<div class="kpi-card" style="border-top-color:#FF7043;">
        <div class="kpi-value" style="color:#FF7043;">{total_decline}</div>
        <div class="kpi-label">🌡️ Total Change (km²M)</div></div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── SECTION 1: TREND CHARTS ───────────────────────────────────────────────────
st.markdown('<div class="section-header">📈 Trend Analysis</div>', unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    if len(filtered) > 0:
        st.pyplot(line_chart(filtered))
    else:
        st.warning("No data for selected filters.")
with col2:
    if len(filtered) > 0:
        st.pyplot(area_chart(filtered))

# ── SECTION 2: DISTRIBUTION CHARTS ───────────────────────────────────────────
st.markdown('<div class="section-header">📊 Distribution & Spread</div>', unsafe_allow_html=True)
col3, col4, col5 = st.columns(3)
with col3:
    if len(filtered) > 1:
        st.pyplot(histogram(filtered))
with col4:
    if len(filtered) > 1:
        st.pyplot(box_plot(filtered))
with col5:
    if len(filtered) > 1:
        st.pyplot(violin_plot(filtered))

# ── SECTION 3: CATEGORY & COMPARISON CHARTS ──────────────────────────────────
st.markdown('<div class="section-header">📋 Category & Comparison</div>', unsafe_allow_html=True)
col6, col7, col8 = st.columns(3)
with col6:
    if len(filtered) > 0:
        st.pyplot(bar_chart(filtered))
with col7:
    if len(filtered) > 0:
        st.pyplot(pie_chart(filtered))
with col8:
    if len(filtered) > 1:
        st.pyplot(count_plot(filtered))

# ── SECTION 4: RELATIONSHIP CHARTS ───────────────────────────────────────────
st.markdown('<div class="section-header">🔗 Relationships & Correlations</div>', unsafe_allow_html=True)
col9, col10 = st.columns(2)
with col9:
    if len(filtered) > 2:
        st.pyplot(scatter_plot(filtered))
with col10:
    if len(filtered) > 2:
        st.pyplot(heatmap(filtered))

# ── DATA TABLE ────────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">🗃️ Filtered Data Table</div>', unsafe_allow_html=True)
st.dataframe(
    filtered[['year', 'extent', 'rolling_avg', 'yoy_change', 'yoy_pct_change', 'anomaly', 'era', 'trend']]
    .rename(columns={
        'year': 'Year', 'extent': 'Extent (km²M)', 'rolling_avg': '5-yr Rolling Avg',
        'yoy_change': 'YoY Change', 'yoy_pct_change': 'YoY % Change',
        'anomaly': 'Anomaly', 'era': 'Era', 'trend': 'Trend'
    }),
    use_container_width=True,
    height=280
)

st.caption("📌 Dashboard by: [Your Name] | Course: Exploratory Data Analysis | Instructor: Ali Hassan Sherazi")
