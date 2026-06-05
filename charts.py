"""
charts.py — All chart / visualization functions
Arctic Sea Ice Extent Dashboard
Uses Matplotlib + Seaborn exclusively as required.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import numpy as np
import pandas as pd

# ── Consistent colour palette ──────────────────────────────────────────────────
PALETTE = {
    "primary":   "#1E90FF",   # dodger blue
    "secondary": "#00CED1",   # dark turquoise
    "accent":    "#FF6347",   # tomato
    "warn":      "#FFA500",   # orange
    "bg":        "#0E1117",   # dark background
    "card":      "#1C1E26",
    "text":      "#FAFAFA",
    "grid":      "#2A2D3A",
}

CMAP_COOL  = "Blues_r"
CMAP_DIV   = "RdYlBu"
SEABORN_PALETTE = ["#1E90FF", "#00CED1", "#FF6347", "#FFA500", "#9370DB", "#32CD32"]

def _style():
    """Apply a consistent dark theme."""
    plt.rcParams.update({
        "figure.facecolor":  PALETTE["bg"],
        "axes.facecolor":    PALETTE["card"],
        "axes.edgecolor":    PALETTE["grid"],
        "axes.labelcolor":   PALETTE["text"],
        "axes.titlecolor":   PALETTE["text"],
        "xtick.color":       PALETTE["text"],
        "ytick.color":       PALETTE["text"],
        "text.color":        PALETTE["text"],
        "grid.color":        PALETTE["grid"],
        "grid.linestyle":    "--",
        "grid.alpha":        0.5,
        "legend.facecolor":  PALETTE["card"],
        "legend.edgecolor":  PALETTE["grid"],
        "legend.labelcolor": PALETTE["text"],
        "font.family":       "DejaVu Sans",
        "font.size":         11,
    })

def _save(fig):
    """Return figure (Streamlit will call st.pyplot)."""
    plt.tight_layout()
    return fig


# ── 1. LINE CHART — Trend over time ──────────────────────────────────────────
def chart_line(df: pd.DataFrame):
    _style()
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(df["year"], df["extent"], color=PALETTE["primary"],
            linewidth=2.2, marker="o", markersize=4, label="Annual Extent")
    if "rolling_avg" in df.columns and df["rolling_avg"].notna().sum() > 2:
        ax.plot(df["year"], df["rolling_avg"], color=PALETTE["warn"],
                linewidth=2, linestyle="--", label="5-yr Rolling Avg")
    ax.fill_between(df["year"], df["extent"], alpha=0.15, color=PALETTE["primary"])
    ax.set_title("Arctic Sea Ice Extent Over Time", fontsize=14, fontweight="bold")
    ax.set_xlabel("Year");  ax.set_ylabel("Extent (million km²)")
    ax.legend();  ax.grid(True)
    return _save(fig)


# ── 2. AREA CHART — Cumulative / filled trend ────────────────────────────────
def chart_area(df: pd.DataFrame):
    _style()
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.fill_between(df["year"], df["extent"], alpha=0.45,
                    color=PALETTE["secondary"], label="Ice Extent")
    ax.plot(df["year"], df["extent"], color=PALETTE["secondary"], linewidth=1.8)
    global_mean = df["extent"].mean()
    ax.axhline(global_mean, color=PALETTE["accent"], linewidth=1.5,
               linestyle="--", label=f"Mean ({global_mean:.2f})")
    ax.set_title("Area Chart — Arctic Ice Extent (Cumulative View)", fontsize=14, fontweight="bold")
    ax.set_xlabel("Year");  ax.set_ylabel("Extent (million km²)")
    ax.legend();  ax.grid(True)
    return _save(fig)


# ── 3. BAR CHART — Decade averages ───────────────────────────────────────────
def chart_bar(df: pd.DataFrame):
    _style()
    decade_avg = df.groupby("decade")["extent"].mean().reset_index()
    fig, ax = plt.subplots(figsize=(8, 4))
    bars = ax.bar(decade_avg["decade"], decade_avg["extent"],
                  color=SEABORN_PALETTE[:len(decade_avg)], edgecolor=PALETTE["grid"], linewidth=0.8)
    for bar, val in zip(bars, decade_avg["extent"]):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
                f"{val:.2f}", ha="center", va="bottom", fontsize=10, color=PALETTE["text"])
    ax.set_title("Average Ice Extent by Decade", fontsize=14, fontweight="bold")
    ax.set_xlabel("Decade");  ax.set_ylabel("Avg Extent (million km²)")
    ax.grid(True, axis="y")
    return _save(fig)


# ── 4. HISTOGRAM — Frequency distribution ────────────────────────────────────
def chart_histogram(df: pd.DataFrame):
    _style()
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.hist(df["extent"], bins=12, color=PALETTE["primary"],
            edgecolor=PALETTE["bg"], linewidth=0.8, alpha=0.85)
    ax.axvline(df["extent"].mean(), color=PALETTE["accent"], linewidth=2,
               linestyle="--", label=f"Mean: {df['extent'].mean():.2f}")
    ax.axvline(df["extent"].median(), color=PALETTE["warn"], linewidth=2,
               linestyle=":", label=f"Median: {df['extent'].median():.2f}")
    ax.set_title("Histogram — Distribution of Ice Extent Values", fontsize=14, fontweight="bold")
    ax.set_xlabel("Extent (million km²)");  ax.set_ylabel("Frequency")
    ax.legend();  ax.grid(True, axis="y")
    return _save(fig)


# ── 5. SCATTER PLOT — Year vs Extent ─────────────────────────────────────────
def chart_scatter(df: pd.DataFrame):
    _style()
    fig, ax = plt.subplots(figsize=(8, 4))
    sc = ax.scatter(df["year"], df["extent"], c=df["extent"],
                    cmap=CMAP_DIV, s=70, edgecolors=PALETTE["grid"], linewidth=0.6, zorder=3)
    # Trendline
    if len(df) > 2:
        z = np.polyfit(df["year"], df["extent"], 1)
        p = np.poly1d(z)
        ax.plot(df["year"], p(df["year"]), color=PALETTE["accent"],
                linewidth=2, linestyle="--", label=f"Trend ({z[0]:+.3f}/yr)")
    plt.colorbar(sc, ax=ax, label="Extent (million km²)")
    ax.set_title("Scatter Plot — Year vs Ice Extent", fontsize=14, fontweight="bold")
    ax.set_xlabel("Year");  ax.set_ylabel("Extent (million km²)")
    ax.legend();  ax.grid(True)
    return _save(fig)


# ── 6. BOX PLOT — Spread by era ──────────────────────────────────────────────
def chart_box(df: pd.DataFrame):
    _style()
    fig, ax = plt.subplots(figsize=(8, 4))
    eras = df["era"].dropna().unique().tolist()
    data_by_era = [df.loc[df["era"] == e, "extent"].values for e in eras]
    bp = ax.boxplot(data_by_era, labels=eras, patch_artist=True,
                    medianprops=dict(color=PALETTE["accent"], linewidth=2))
    colors = SEABORN_PALETTE[:len(eras)]
    for patch, col in zip(bp["boxes"], colors):
        patch.set_facecolor(col); patch.set_alpha(0.7)
    ax.set_title("Box Plot — Ice Extent Spread by Era", fontsize=14, fontweight="bold")
    ax.set_xlabel("Era");  ax.set_ylabel("Extent (million km²)")
    ax.grid(True, axis="y")
    return _save(fig)


# ── 7. PIE CHART — Above/below mean ──────────────────────────────────────────
def chart_pie(df: pd.DataFrame):
    _style()
    counts = df["above_mean"].value_counts()
    labels = ["Above Mean" if k else "Below Mean" for k in counts.index]
    colors = [PALETTE["primary"], PALETTE["accent"]]
    fig, ax = plt.subplots(figsize=(6, 5))
    wedges, texts, autotexts = ax.pie(
        counts, labels=labels, colors=colors,
        autopct="%1.1f%%", startangle=140,
        wedgeprops=dict(edgecolor=PALETTE["bg"], linewidth=2),
    )
    for at in autotexts:
        at.set_color(PALETTE["text"]); at.set_fontweight("bold")
    ax.set_title("Proportion Above vs Below Historical Mean", fontsize=13, fontweight="bold")
    return _save(fig)


# ── 8. HEATMAP — Decade × Era correlation table ──────────────────────────────
def chart_heatmap(df: pd.DataFrame):
    _style()
    # Build a pivot: decade rows, numeric stats columns
    stats = df.groupby("decade")["extent"].agg(["mean", "min", "max", "std"]).round(3)
    if stats.empty or len(stats) < 2:
        fig, ax = plt.subplots(figsize=(6, 3))
        ax.text(0.5, 0.5, "Not enough data for heatmap",
                ha="center", va="center", color=PALETTE["text"])
        return _save(fig)
    fig, ax = plt.subplots(figsize=(8, max(3, len(stats) * 0.7 + 1)))
    sns.heatmap(stats, annot=True, fmt=".2f", cmap="Blues",
                linewidths=0.5, linecolor=PALETTE["bg"],
                ax=ax, cbar_kws={"label": "Extent (million km²)"})
    ax.set_title("Heatmap — Ice Extent Stats by Decade", fontsize=14, fontweight="bold")
    ax.set_xlabel("Statistic");  ax.set_ylabel("Decade")
    return _save(fig)


# ── 9. COUNT PLOT — Records per decade ───────────────────────────────────────
def chart_count(df: pd.DataFrame):
    _style()
    decade_counts = df["decade"].value_counts().sort_index()
    fig, ax = plt.subplots(figsize=(8, 4))
    bars = ax.bar(decade_counts.index, decade_counts.values,
                  color=SEABORN_PALETTE[:len(decade_counts)],
                  edgecolor=PALETTE["bg"], linewidth=0.8)
    for bar, val in zip(bars, decade_counts.values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                str(val), ha="center", va="bottom", fontsize=10, color=PALETTE["text"])
    ax.set_title("Count Plot — Records per Decade", fontsize=14, fontweight="bold")
    ax.set_xlabel("Decade");  ax.set_ylabel("Number of Years")
    ax.grid(True, axis="y")
    return _save(fig)


# ── 10. VIOLIN PLOT — Era distribution ───────────────────────────────────────
def chart_violin(df: pd.DataFrame):
    _style()
    df2 = df.dropna(subset=["era"])
    if df2.empty or df2["era"].nunique() < 2:
        fig, ax = plt.subplots(figsize=(6, 3))
        ax.text(0.5, 0.5, "Not enough era diversity for violin plot",
                ha="center", va="center", color=PALETTE["text"])
        return _save(fig)
    fig, ax = plt.subplots(figsize=(9, 4))
    sns.violinplot(data=df2, x="era", y="extent", palette=SEABORN_PALETTE,
                   inner="quartile", ax=ax)
    ax.set_title("Violin Plot — Ice Extent Distribution by Era", fontsize=14, fontweight="bold")
    ax.set_xlabel("Era");  ax.set_ylabel("Extent (million km²)")
    ax.grid(True, axis="y")
    return _save(fig)


# ── BONUS: YoY Change Bar ─────────────────────────────────────────────────────
def chart_yoy(df: pd.DataFrame):
    _style()
    df2 = df.dropna(subset=["yoy_change"])
    if df2.empty:
        fig, ax = plt.subplots(figsize=(6, 3))
        ax.text(0.5, 0.5, "Insufficient data for YoY chart",
                ha="center", va="center", color=PALETTE["text"])
        return _save(fig)
    colors = [PALETTE["accent"] if v < 0 else PALETTE["primary"] for v in df2["yoy_change"]]
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.bar(df2["year"], df2["yoy_change"], color=colors, edgecolor=PALETTE["bg"], linewidth=0.5)
    ax.axhline(0, color=PALETTE["text"], linewidth=1.2)
    pos_patch = mpatches.Patch(color=PALETTE["primary"], label="Increase")
    neg_patch = mpatches.Patch(color=PALETTE["accent"], label="Decrease")
    ax.legend(handles=[pos_patch, neg_patch])
    ax.set_title("Year-over-Year Change in Ice Extent (Bonus Chart)", fontsize=14, fontweight="bold")
    ax.set_xlabel("Year");  ax.set_ylabel("Change (million km²)")
    ax.grid(True, axis="y")
    return _save(fig)
