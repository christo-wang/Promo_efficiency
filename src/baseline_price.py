import pandas as pd

def calculate_baseline_price(
    df: pd.DataFrame,
    group_cols = ['Markets', 'YEAR', 'Brand_Pack_PackType'],
    price_col  = 'NON-PROMO PRICE',
    quantile   = 0.8
) -> pd.DataFrame:
    """
    2. Baseline Price Calculating
    - Computes the q-th quantile of non-promo price per group, here i used 80% above as an example
    """
    baseline = (
        df
          .groupby(group_cols)[price_col]
          .quantile(quantile)
          .reset_index(name='Baseline Price')
    )
    return df.merge(baseline, on=group_cols, how='left')
