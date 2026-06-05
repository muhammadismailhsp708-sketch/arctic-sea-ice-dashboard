import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns

# ── Global Style ──────────────────────────────────────────────────────────────
PALETTE = "Blues_r"
PRIMARY   = "#1a6fa8"
SECONDARY = "#e05c2a"
BG        = "#f4f8fc"
ACCENT    = "#2ca02c"
sns.set_theme(style="whitegrid", palette="Blues_r")
plt.rcParams.update({
    "figure.facecolor": BG,
    "axes.facecolor":   BG,
    "axes.titlesize":   13,
    "axes.labelsize":   11,
    "xtick.labelsize":  9,
    "ytick.labelsize":  9,
})


def _save_tight(fig):
    fig.tight_layout()
    return fig


# 1. PIE CHART ─────────────────────────────────────────────────────────────────
def chart_pie(df: pd.DataFrame):
    counts = df["extent_category"].value_counts()
    fig, ax = plt.subplots(figsize=(5, 4))
    colors = [PRIMARY, SECONDARY]
    wedges, texts, autotexts = ax.pie(
        counts, labels=counts.index, autopct="%1.1f%%",
        colors=colors, startangle=140,
        wedgeprops={"edgecolor": "white", "linewidth": 1.5}
    )
    for at in autotexts:
        at.set_fontsize(10)
    ax.set_title("Distribution: Above vs Below Median Extent", fontweight="bold")
    return _save_tight(fig)


# 2. HISTOGRAM ─────────────────────────────────────────────────────────────────
def chart_histogram(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.hist(df["extent"], bins=10, color=PRIMARY, edgecolor="white", linewidth=0.8)
    ax.set_xlabel("Sea Ice Extent (million km²)")
    ax.set_ylabel("Frequency")
    ax.set_title("Frequency Distribution of Sea Ice Extent", fontweight="bold")
    ax.axvline(df["extent"].mean(), color=SECONDARY, linestyle="--", label=f"Mean: {df['extent'].mean():.2f}")
    ax.legend()
    return _save_tight(fig)


# 3. LINE CHART ────────────────────────────────────────────────────────────────
def chart_line(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(df["year"], df["extent"], color=PRIMARY, linewidth=2, marker="o", markersize=3, label="Annual Extent")
    ax.plot(df["year"], df["rolling_avg_5yr"], color=SECONDARY, linewidth=2, linestyle="--", label="5-yr Rolling Avg")
    ax.set_xlabel("Year")
    ax.set_ylabel("Sea Ice Extent (million km²)")
    ax.set_title("Arctic Sea Ice Extent Over Time", fontweight="bold")
    ax.legend()
    ax.xaxis.set_major_locator(mticker.MultipleLocator(5))
    return _save_tight(fig)


# 4. BAR CHART ─────────────────────────────────────────────────────────────────
def chart_bar(df: pd.DataFrame):
    decade_avg = df.groupby("decade")["extent"].mean().reset_index()
    fig, ax = plt.subplots(figsize=(7, 4))
    colors = sns.color_palette(PALETTE, len(decade_avg))
    bars = ax.bar(decade_avg["decade"], decade_avg["extent"], color=colors, edgecolor="white", linewidth=0.8)
    ax.set_xlabel("Decade")
    ax.set_ylabel("Average Extent (million km²)")
    ax.set_title("Average Sea Ice Extent by Decade", fontweight="bold")
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.04,
                f"{bar.get_height():.2f}", ha="center", va="bottom", fontsize=9)
    return _save_tight(fig)


# 5. SCATTER PLOT ──────────────────────────────────────────────────────────────
def chart_scatter(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(6, 4))
    sc = ax.scatter(df["year"], df["extent"], c=df["extent"], cmap="RdYlBu",
                    s=60, edgecolors="white", linewidth=0.5, zorder=3)
    plt.colorbar(sc, ax=ax, label="Extent (million km²)")
    # Trend line
    z = np.polyfit(df["year"], df["extent"], 1)
    p = np.poly1d(z)
    ax.plot(df["year"], p(df["year"]), color=SECONDARY, linestyle="--", linewidth=1.5, label="Trend")
    ax.set_xlabel("Year")
    ax.set_ylabel("Sea Ice Extent (million km²)")
    ax.set_title("Year vs Sea Ice Extent (with Trend)", fontweight="bold")
    ax.legend()
    return _save_tight(fig)


# 6. BOX PLOT ──────────────────────────────────────────────────────────────────
def chart_box(df: pd.DataFrame):
    era_order = ["Pre-1990", "1990s", "2000s", "2010s+"]
    era_order = [e for e in era_order if e in df["era"].unique()]
    fig, ax = plt.subplots(figsize=(7, 4))
    data_by_era = [df[df["era"] == e]["extent"].values for e in era_order]
    bp = ax.boxplot(data_by_era, labels=era_order, patch_artist=True,
                    boxprops=dict(facecolor=PRIMARY, alpha=0.7),
                    medianprops=dict(color=SECONDARY, linewidth=2),
                    whiskerprops=dict(color=PRIMARY),
                    capprops=dict(color=PRIMARY))
    ax.set_xlabel("Era")
    ax.set_ylabel("Sea Ice Extent (million km²)")
    ax.set_title("Sea Ice Extent Distribution by Era (Box Plot)", fontweight="bold")
    return _save_tight(fig)


# 7. HEATMAP ───────────────────────────────────────────────────────────────────
def chart_heatmap(df: pd.DataFrame):
    num_cols = ["year", "extent", "change_from_prev", "rolling_avg_5yr", "pct_change", "anomaly"]
    corr = df[num_cols].dropna().corr()
    fig, ax = plt.subplots(figsize=(7, 5))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", ax=ax,
                linewidths=0.5, square=True, annot_kws={"size": 9},
                vmin=-1, vmax=1)
    ax.set_title("Feature Correlation Heatmap", fontweight="bold")
    return _save_tight(fig)


# 8. AREA CHART ────────────────────────────────────────────────────────────────
def chart_area(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.fill_between(df["year"], df["extent"], alpha=0.4, color=PRIMARY, label="Extent")
    ax.plot(df["year"], df["extent"], color=PRIMARY, linewidth=1.5)
    ax.fill_between(df["year"], df["rolling_avg_5yr"], alpha=0.3, color=SECONDARY, label="5-yr Avg")
    ax.plot(df["year"], df["rolling_avg_5yr"], color=SECONDARY, linewidth=1.5, linestyle="--")
    ax.set_xlabel("Year")
    ax.set_ylabel("Sea Ice Extent (million km²)")
    ax.set_title("Cumulative Area Chart: Extent Over Time", fontweight="bold")
    ax.legend()
    ax.xaxis.set_major_locator(mticker.MultipleLocator(5))
    return _save_tight(fig)


# 9. COUNT PLOT ────────────────────────────────────────────────────────────────
def chart_count(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(7, 4))
    era_order = ["Pre-1990", "1990s", "2000s", "2010s+"]
    era_order = [e for e in era_order if e in df["era"].unique()]
    counts = df["era"].value_counts().reindex(era_order).fillna(0)
    colors = sns.color_palette(PALETTE, len(era_order))
    bars = ax.bar(counts.index, counts.values, color=colors, edgecolor="white", linewidth=0.8)
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                int(bar.get_height()), ha="center", va="bottom", fontsize=10)
    ax.set_xlabel("Era")
    ax.set_ylabel("Number of Years")
    ax.set_title("Count of Observations per Era", fontweight="bold")
    return _save_tight(fig)


# 10. VIOLIN PLOT ──────────────────────────────────────────────────────────────
def chart_violin(df: pd.DataFrame):
    era_order = ["Pre-1990", "1990s", "2000s", "2010s+"]
    era_order = [e for e in era_order if e in df["era"].unique()]
    fig, ax = plt.subplots(figsize=(7, 4))
    plot_df = df[df["era"].isin(era_order)].copy()
    sns.violinplot(data=plot_df, x="era", y="extent", order=era_order,
                   palette="Blues", inner="box", ax=ax)
    ax.set_xlabel("Era")
    ax.set_ylabel("Sea Ice Extent (million km²)")
    ax.set_title("Extent Distribution & Density by Era (Violin Plot)", fontweight="bold")
    return _save_tight(fig)


# BONUS: PAIR PLOT (returns figure separately) ────────────────────────────────
def chart_pair(df: pd.DataFrame):
    num_cols = ["year", "extent", "anomaly", "rolling_avg_5yr"]
    plot_df = df[num_cols + ["extent_category"]].dropna()
    g = sns.pairplot(plot_df, hue="extent_category", palette={
        "Above Median": PRIMARY, "Below Median": SECONDARY
    }, plot_kws={"alpha": 0.7, "s": 40}, diag_kind="kde")
    g.fig.suptitle("Pair Plot of Key Numerical Features", y=1.02, fontweight="bold")
    return g.fig
