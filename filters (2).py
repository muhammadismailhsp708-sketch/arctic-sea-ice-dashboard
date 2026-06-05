import pandas as pd
import numpy as np

def load_data(filepath="arctic_ice_extent[1].csv"):
    """Load and clean the Arctic Sea Ice dataset."""
    df = pd.read_csv(filepath)
    # Clean column names and values
    df.columns = df.columns.str.strip()
    df['extent'] = df['extent'].astype(str).str.strip().astype(float)
    df['year'] = df['year'].astype(int)

    # Derived features
    df['decade'] = (df['year'] // 10) * 10
    df['decade_label'] = df['decade'].astype(str) + 's'
    df['rolling_avg'] = df['extent'].rolling(window=5, min_periods=1).mean().round(3)
    df['yoy_change'] = df['extent'].diff().round(3)
    df['yoy_pct_change'] = df['extent'].pct_change().mul(100).round(2)
    df['anomaly'] = (df['extent'] - df['extent'].mean()).round(3)
    df['era'] = pd.cut(df['year'],
                       bins=[1978, 1989, 1999, 2009, 2023],
                       labels=['1980s', '1990s', '2000s', '2010s+'])
    df['trend'] = df['yoy_change'].apply(
        lambda x: 'Increase' if x > 0 else ('Decrease' if x < 0 else 'No Change')
    )
    return df


def apply_filters(df, year_range, era_filter, extent_range, search_year):
    """Apply all sidebar filters and return filtered DataFrame."""
    filtered = df.copy()

    # Year range filter
    filtered = filtered[
        (filtered['year'] >= year_range[0]) & (filtered['year'] <= year_range[1])
    ]

    # Era multi-select filter
    if era_filter and len(era_filter) > 0:
        filtered = filtered[filtered['era'].isin(era_filter)]

    # Extent numerical range filter
    filtered = filtered[
        (filtered['extent'] >= extent_range[0]) & (filtered['extent'] <= extent_range[1])
    ]

    # Search / text filter (year keyword)
    if search_year and search_year.strip() != "":
        try:
            yr = int(search_year.strip())
            filtered = filtered[filtered['year'] == yr]
        except ValueError:
            pass  # invalid input, skip filter

    return filtered


def get_kpis(df, filtered):
    """Compute KPI summary statistics."""
    return {
        "total_records": len(filtered),
        "avg_extent": round(filtered['extent'].mean(), 3),
        "max_extent": filtered['extent'].max(),
        "max_year": int(filtered.loc[filtered['extent'].idxmax(), 'year']) if len(filtered) > 0 else "—",
        "min_extent": filtered['extent'].min(),
        "min_year": int(filtered.loc[filtered['extent'].idxmin(), 'year']) if len(filtered) > 0 else "—",
        "overall_trend": round(filtered['yoy_change'].mean(), 3) if len(filtered) > 1 else 0,
    }
