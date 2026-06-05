"""
app.py — Main Streamlit Dashboard Application
Arctic Sea Ice Extent Dashboard
Course: Exploratory Data Analysis | Instructor: Ali Hassan Sherazi
"""

import streamlit as st
import pandas as pd

from filters import load_data, apply_filters, compute_kpis
from charts import (
    chart_line, chart_area, chart_bar, chart_histogram,
    chart_scatter, chart_box, chart_pie, chart_heatmap,
    chart_count, chart_violin, chart_yoy,
)

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Arctic Sea Ice Dashboard",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Dark base */
    .stApp { background-color: #0E1117; }

    /* KPI cards */
    .kpi-card {
        background: #1C1E26;
        border: 1px solid #2A2D3A;
        border-radius: 12px;
        padding: 16px 20px;
        text-align: center;
    }
    .kpi-label  { color: #8E9AAF; font-size: 12px; text-transform: uppercase; letter-spacing: 1px; }
    .kpi-value  { color: #FAFAFA; font-size: 26px; font-weight: 700; margin: 4px 0; }
    .kpi-sub    { color: #1E90FF; font-size: 12px; }

    /* Section headers */
    .section-header {
        border-left: 4px solid #1E90FF;
        padding-left: 12px;
        margin: 24px 0 12px 0;
        font-size: 18px;
        font-weight: 600;
        color: #FAFAFA;
    }

    /* Sidebar */
    [data-testid="stSidebar"] { background-color: #13151C; }

    /* Divider */
    hr { border-color: #2A2D3A; }
</style>
""", unsafe_allow_html=True)


# ── Load data ──────────────────────────────────────────────────────────────────
@st.cache_data
def get_data():
    return load_data()

full_df = get_data()

# ── Sidebar — Filters ──────────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/0/00/Flag_of_Antarctica.svg/320px-Flag_of_Antarctica.svg.png",
             width=80)
    st.title("🧊 Filters")
    st.markdown("---")

    # 1. Date / Year Range Filter
    st.subheader("📅 Year Range")
    year_min, year_max = int(full_df["year"].min()), int(full_df["year"].max())
    year_range = st.slider("Select year range", year_min, year_max,
                           (year_min, year_max), step=1)

    # 2. Numerical Range Slider
    st.subheader("📊 Extent Range (million km²)")
    ext_min = float(full_df["extent"].min())
    ext_max = float(full_df["extent"].max())
    extent_range = st.slider("Select extent range",
                             ext_min, ext_max,
                             (ext_min, ext_max), step=0.01)

    # 3. Category Filter — Decade dropdown
    st.subheader("🗂️ Decade Filter")
    all_decades = sorted(full_df["decade"].unique().tolist())
    selected_decades = st.multiselect("Select decade(s)", all_decades, default=[])

    # 4. Multi-Select Filter — Era
    st.subheader("⏳ Era Filter")
    all_eras = full_df["era"].dropna().unique().tolist()
    selected_eras = st.multiselect("Select era(s)", all_eras, default=[])

    # 5. Search / Text Filter
    st.subheader("🔍 Search Year")
    search_year = st.text_input("Type a year (or partial, e.g. '199')", value="")

    st.markdown("---")

    # 6. Reset / Clear Filters
    if st.button("🔄 Reset All Filters", use_container_width=True):
        st.rerun()

    st.markdown("---")
    st.caption("Data: NSIDC Arctic Sea Ice Extent 1979–2023")


# ── Apply filters ──────────────────────────────────────────────────────────────
df = apply_filters(
    full_df,
    year_range=year_range,
    selected_decades=selected_decades,
    selected_eras=selected_eras,
    extent_range=extent_range,
    search_year=search_year,
)

kpis = compute_kpis(df, full_df)

# ── Dashboard Header ───────────────────────────────────────────────────────────
st.markdown("""
<h1 style='color:#1E90FF; margin-bottom:0;'>🧊 Arctic Sea Ice Extent Dashboard</h1>
<p style='color:#8E9AAF; margin-top:4px;'>
    Analyzing annual Arctic sea ice extent data from 1979 to 2023.
    Use the sidebar filters to explore trends, distributions, and patterns.
</p>
""", unsafe_allow_html=True)
st.markdown("---")

# ── KPI Cards ──────────────────────────────────────────────────────────────────
if df.empty:
    st.error("⚠️ No data matches the current filters. Please adjust your filters.")
    st.stop()

c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    st.markdown(f"""<div class='kpi-card'>
        <div class='kpi-label'>Total Records</div>
        <div class='kpi-value'>{kpis['total_records']}</div>
        <div class='kpi-sub'>Years of data</div>
    </div>""", unsafe_allow_html=True)

with c2:
    st.markdown(f"""<div class='kpi-card'>
        <div class='kpi-label'>Avg Extent</div>
        <div class='kpi-value'>{kpis['avg_extent']:.2f}</div>
        <div class='kpi-sub'>million km²</div>
    </div>""", unsafe_allow_html=True)

with c3:
    st.markdown(f"""<div class='kpi-card'>
        <div class='kpi-label'>Record Low 📉</div>
        <div class='kpi-value'>{kpis['min_extent']:.2f}</div>
        <div class='kpi-sub'>in {kpis['min_year']}</div>
    </div>""", unsafe_allow_html=True)

with c4:
    st.markdown(f"""<div class='kpi-card'>
        <div class='kpi-label'>Record High 📈</div>
        <div class='kpi-value'>{kpis['max_extent']:.2f}</div>
        <div class='kpi-sub'>in {kpis['max_year']}</div>
    </div>""", unsafe_allow_html=True)

with c5:
    trend_label = "📉 Declining" if kpis['trend_slope'] < 0 else "📈 Rising"
    st.markdown(f"""<div class='kpi-card'>
        <div class='kpi-label'>Trend</div>
        <div class='kpi-value'>{kpis['trend_slope']:.3f}</div>
        <div class='kpi-sub'>{trend_label} per year</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Section 1: Trend Charts ────────────────────────────────────────────────────
st.markdown("<div class='section-header'>📈 Trend Analysis</div>", unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    st.pyplot(chart_line(df))
with col2:
    st.pyplot(chart_area(df))

# ── Section 2: Distribution Charts ────────────────────────────────────────────
st.markdown("<div class='section-header'>📊 Distribution & Spread</div>", unsafe_allow_html=True)
col3, col4, col5 = st.columns(3)
with col3:
    st.pyplot(chart_histogram(df))
with col4:
    st.pyplot(chart_box(df))
with col5:
    st.pyplot(chart_pie(df))

# ── Section 3: Categorical Charts ─────────────────────────────────────────────
st.markdown("<div class='section-header'>🗂️ Categorical Comparisons</div>", unsafe_allow_html=True)
col6, col7 = st.columns(2)
with col6:
    st.pyplot(chart_bar(df))
with col7:
    st.pyplot(chart_count(df))

# ── Section 4: Relationship & Advanced ────────────────────────────────────────
st.markdown("<div class='section-header'>🔬 Relationships & Advanced Analysis</div>", unsafe_allow_html=True)
col8, col9 = st.columns(2)
with col8:
    st.pyplot(chart_scatter(df))
with col9:
    st.pyplot(chart_violin(df))

# ── Section 5: Heatmap ─────────────────────────────────────────────────────────
st.markdown("<div class='section-header'>🌡️ Heatmap — Stats by Decade</div>", unsafe_allow_html=True)
st.pyplot(chart_heatmap(df))

# ── Section 6: Bonus ──────────────────────────────────────────────────────────
st.markdown("<div class='section-header'>🎁 Bonus: Year-over-Year Change</div>", unsafe_allow_html=True)
st.pyplot(chart_yoy(df))

# ── Raw Data Table ─────────────────────────────────────────────────────────────
st.markdown("<div class='section-header'>📋 Filtered Data Table</div>", unsafe_allow_html=True)
with st.expander("Show / Hide Data Table"):
    st.dataframe(
        df[["year", "extent", "decade", "era", "yoy_change", "pct_change", "anomaly"]].style
          .background_gradient(subset=["extent"], cmap="Blues")
          .format({"extent": "{:.3f}", "yoy_change": "{:+.3f}",
                   "pct_change": "{:+.1f}%", "anomaly": "{:+.3f}"}),
        use_container_width=True,
    )

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:#8E9AAF; font-size:12px;'>"
    "Arctic Sea Ice Extent Dashboard · EDA Course · Instructor: Ali Hassan Sherazi"
    "</p>",
    unsafe_allow_html=True,
)
