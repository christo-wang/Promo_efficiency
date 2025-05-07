import pandas as pd

def calculate_baseline_volume(
    df: pd.DataFrame,
    group_cols = ['Markets', 'YEAR', 'Brand_Pack_PackType'],
    vol_col    = 'Sales Units No Promo'
) -> pd.DataFrame:
    """
    3. Baseline Volume Calculating
    - Ensures vol_col is numeric
    - Computes mean non-promo units per group
    """
    df[vol_col] = pd.to_numeric(df[vol_col], errors='coerce')
    baseline = (
        df
          .groupby(group_cols)[vol_col]
          .mean()
          .reset_index(name='Baseline Volume')
    )
    return df.merge(baseline, on=group_cols, how='left')
