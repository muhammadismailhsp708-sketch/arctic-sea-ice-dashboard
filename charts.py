import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import numpy as np
import pandas as pd

# ── Consistent color palette ──────────────────────────────────────────────────
PALETTE = "Blues_r"
ACCENT  = "#1565C0"
ACCENT2 = "#EF5350"
BG      = "#F0F4F8"
GRID    = "#CFD8DC"

def _style(ax, title, xlabel="", ylabel=""):
    ax.set_title(title, fontsize=13, fontweight='bold', pad=10, color="#1A237E")
    ax.set_xlabel(xlabel, fontsize=10, color="#37474F")
    ax.set_ylabel(ylabel, fontsize=10, color="#37474F")
    ax.tick_params(colors="#37474F", labelsize=9)
    ax.grid(True, linestyle='--', linewidth=0.5, color=GRID, alpha=0.7)
    ax.set_facecolor(BG)
    for spine in ax.spines.values():
        spine.set_edgecolor(GRID)


def line_chart(df):
    """Line chart: Sea ice extent trend over years."""
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(df['year'], df['extent'], color=ACCENT, linewidth=2, marker='o', markersize=4, label='Extent')
    ax.plot(df['year'], df['rolling_avg'], color=ACCENT2, linewidth=1.5, linestyle='--', label='5-yr Rolling Avg')
    _style(ax, "Arctic Sea Ice Extent Over Time", "Year", "Extent (million km²)")
    ax.legend(fontsize=9)
    fig.tight_layout()
    return fig


def area_chart(df):
    """Area chart: Cumulative ice extent trend."""
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.fill_between(df['year'], df['extent'], alpha=0.4, color=ACCENT, label='Extent')
    ax.plot(df['year'], df['extent'], color=ACCENT, linewidth=1.5)
    _style(ax, "Area Chart: Ice Extent Over Time", "Year", "Extent (million km²)")
    ax.legend(fontsize=9)
    fig.tight_layout()
    return fig


def bar_chart(df):
    """Bar chart: Average extent by decade."""
    decade_avg = df.groupby('decade_label')['extent'].mean().reset_index()
    fig, ax = plt.subplots(figsize=(7, 4))
    colors = sns.color_palette(PALETTE, len(decade_avg))
    bars = ax.bar(decade_avg['decade_label'], decade_avg['extent'], color=colors, edgecolor='white', width=0.6)
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
                f"{bar.get_height():.2f}", ha='center', va='bottom', fontsize=8, color="#37474F")
    _style(ax, "Average Ice Extent by Decade", "Decade", "Avg Extent (million km²)")
    fig.tight_layout()
    return fig


def histogram(df):
    """Histogram: Frequency distribution of extent values."""
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.hist(df['extent'], bins=12, color=ACCENT, edgecolor='white', alpha=0.85)
    ax.axvline(df['extent'].mean(), color=ACCENT2, linestyle='--', linewidth=1.5, label=f"Mean: {df['extent'].mean():.2f}")
    _style(ax, "Distribution of Ice Extent Values", "Extent (million km²)", "Frequency")
    ax.legend(fontsize=9)
    fig.tight_layout()
    return fig


def scatter_plot(df):
    """Scatter plot: Year vs Extent with trend line."""
    fig, ax = plt.subplots(figsize=(7, 4))
    sc = ax.scatter(df['year'], df['extent'], c=df['extent'], cmap='Blues_r', s=60, edgecolors='white', linewidth=0.5, zorder=3)
    # Trend line
    z = np.polyfit(df['year'], df['extent'], 1)
    p = np.poly1d(z)
    ax.plot(df['year'], p(df['year']), color=ACCENT2, linestyle='--', linewidth=1.5, label='Trend Line')
    plt.colorbar(sc, ax=ax, label='Extent')
    _style(ax, "Year vs Ice Extent (Scatter)", "Year", "Extent (million km²)")
    ax.legend(fontsize=9)
    fig.tight_layout()
    return fig


def box_plot(df):
    """Box plot: Extent distribution per era."""
    fig, ax = plt.subplots(figsize=(7, 4))
    eras = df['era'].dropna().unique().tolist()
    data_by_era = [df[df['era'] == e]['extent'].values for e in eras]
    bp = ax.boxplot(data_by_era, labels=eras, patch_artist=True, notch=False,
                    medianprops=dict(color=ACCENT2, linewidth=2))
    colors = sns.color_palette(PALETTE, len(eras))
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
    _style(ax, "Ice Extent Distribution by Era", "Era", "Extent (million km²)")
    fig.tight_layout()
    return fig


def pie_chart(df):
    """Pie chart: Proportion of years above/below mean extent."""
    mean_val = df['extent'].mean()
    above = (df['extent'] >= mean_val).sum()
    below = (df['extent'] < mean_val).sum()
    fig, ax = plt.subplots(figsize=(5, 5))
    wedges, texts, autotexts = ax.pie(
        [above, below],
        labels=['Above Average', 'Below Average'],
        autopct='%1.1f%%',
        colors=[ACCENT, ACCENT2],
        startangle=90,
        wedgeprops=dict(edgecolor='white', linewidth=2)
    )
    for t in autotexts:
        t.set_fontsize(10)
    ax.set_title("Years Above vs Below Average Extent", fontsize=13, fontweight='bold', color="#1A237E", pad=12)
    fig.tight_layout()
    return fig


def heatmap(df):
    """Heatmap: Correlation matrix of all numerical features."""
    num_cols = ['year', 'extent', 'rolling_avg', 'yoy_change', 'yoy_pct_change', 'anomaly']
    corr = df[num_cols].corr()
    fig, ax = plt.subplots(figsize=(7, 5))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap='Blues', ax=ax,
                linewidths=0.5, linecolor='white', annot_kws={"size": 9})
    ax.set_title("Correlation Heatmap of Features", fontsize=13, fontweight='bold', color="#1A237E", pad=10)
    fig.tight_layout()
    return fig


def count_plot(df):
    """Count plot: Number of years per trend direction (Increase/Decrease)."""
    fig, ax = plt.subplots(figsize=(6, 4))
    order = ['Increase', 'Decrease', 'No Change']
    order = [o for o in order if o in df['trend'].values]
    palette = {'Increase': '#42A5F5', 'Decrease': ACCENT2, 'No Change': '#B0BEC5'}
    sns.countplot(data=df, x='trend', ax=ax, order=order,
                  palette={k: palette[k] for k in order if k in palette})
    _style(ax, "Year-over-Year Trend Direction Count", "Trend Direction", "Number of Years")
    for p in ax.patches:
        ax.annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width()/2., p.get_height()),
                    ha='center', va='bottom', fontsize=10)
    fig.tight_layout()
    return fig


def violin_plot(df):
    """Violin plot: Extent distribution per era."""
    fig, ax = plt.subplots(figsize=(7, 4))
    df_clean = df.dropna(subset=['era'])
    sns.violinplot(data=df_clean, x='era', y='extent', ax=ax,
                   palette=PALETTE, inner='box', linewidth=1.2)
    _style(ax, "Violin Plot: Extent Distribution by Era", "Era", "Extent (million km²)")
    fig.tight_layout()
    return fig
