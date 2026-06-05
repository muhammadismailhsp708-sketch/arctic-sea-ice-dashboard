"""
filters.py — Data loading, cleaning, and filtering functions
Arctic Sea Ice Extent Dashboard
"""

import pandas as pd
import numpy as np

DATA_PATH = "data/1780679221796_arctic_ice_extent.csv"

# ── Decade helper ──────────────────────────────────────────────────────────────
def get_decade(year):
    return f"{(year // 10) * 10}s"


def load_data() -> pd.DataFrame:
    """Load and clean the dataset; add derived columns."""
    df = pd.read_csv(DATA_PATH)

    # Basic cleaning
    df.columns = df.columns.str.strip().str.lower()
    df = df.dropna(subset=["year", "extent"])
    df["year"] = df["year"].astype(int)
    df["extent"] = df["extent"].astype(float)

    # Derived columns
    df["decade"] = df["year"].apply(get_decade)
    df["era"] = pd.cut(
        df["year"],
        bins=[1978, 1989, 1999, 2009, 2023],
        labels=["1980s", "1990s", "2000s", "2010s+"],
    )
    df["rolling_avg"] = df["extent"].rolling(window=5, center=True).mean()
    df["yoy_change"] = df["extent"].diff()
    df["pct_change"] = df["extent"].pct_change() * 100
    df["above_mean"] = df["extent"] >= df["extent"].mean()
    df["anomaly"] = df["extent"] - df["extent"].mean()

    return df


def apply_filters(
    df: pd.DataFrame,
    year_range: tuple,
    selected_decades: list,
    selected_eras: list,
    extent_range: tuple,
    search_year: str,
) -> pd.DataFrame:
    """Apply all sidebar filters and return filtered DataFrame."""
    mask = pd.Series([True] * len(df), index=df.index)

    # Year range
    mask &= (df["year"] >= year_range[0]) & (df["year"] <= year_range[1])

    # Extent range
    mask &= (df["extent"] >= extent_range[0]) & (df["extent"] <= extent_range[1])

    # Decade multi-select
    if selected_decades:
        mask &= df["decade"].isin(selected_decades)

    # Era multi-select
    if selected_eras:
        mask &= df["era"].astype(str).isin(selected_eras)

    # Text search on year
    if search_year.strip():
        mask &= df["year"].astype(str).str.contains(search_year.strip())

    return df[mask].reset_index(drop=True)


def compute_kpis(df: pd.DataFrame, full_df: pd.DataFrame) -> dict:
    """Return KPI dict for filtered DataFrame."""
    if df.empty:
        return {}
    return {
        "total_records": len(df),
        "avg_extent": df["extent"].mean(),
        "min_extent": df["extent"].min(),
        "min_year": df.loc[df["extent"].idxmin(), "year"],
        "max_extent": df["extent"].max(),
        "max_year": df.loc[df["extent"].idxmax(), "year"],
        "latest_year": df["year"].max(),
        "latest_extent": df.loc[df["year"].idxmax(), "extent"],
        "trend_slope": np.polyfit(df["year"], df["extent"], 1)[0],
        "global_mean": full_df["extent"].mean(),
    }
