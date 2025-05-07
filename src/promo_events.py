import pandas as pd
import numpy as np

def flag_and_identify_promos(
    df: pd.DataFrame,
    group_cols = ['Markets', 'YEAR', 'Brand_Pack_PackType']
) -> pd.DataFrame:
    """
    4. Flagging Promo Weeks & Identifying Promo Events
    - Flags volume & price deviations
    - Filters anomalies and computes uplift
    - Clusters valid promo weeks into Event_IDs
    """
    # volume & price flags
    df['Promo Vol Check'] = (df['Sales Units Any Promo'] > 0.5 * df['Sales Units']).map({True:'Y', False:'N'})
    df['Promo 5% Deviation Check'] = (df['PROMO PRICE'] < 0.95 * df['NON-PROMO PRICE']).map({True:'Y', False:'N'})
    df['Promo Week Check'] = (
        (df['Promo Vol Check']=='Y') &
        (df['Promo 5% Deviation Check']=='Y')
    ).map({True:'Y', False:'N'})

    # anomalies & uplift
    df['Erase Anomaly'] = (
        (df['Baseline Volume'] > df['Sales Units']) &
        (df['Baseline Price'] < df['PROMO PRICE'])
    ).map({True:'Y', False:'N'})
    df['Uplift'] = df.apply(
        lambda r: r['Sales Units'] - r['Baseline Volume']
                  if (r['Promo Week Check']=='Y') and (r['Erase Anomaly']=='N')
                  else np.nan,
        axis=1
    )

    # build valid table
    valid = df[(df['Promo Week Check']=='Y') & (df['Erase Anomaly']=='N')].copy()
    valid.sort_values(group_cols + ['END DATE'], inplace=True)

    # event clustering
    valid['Date_Gap'] = valid.groupby(group_cols)['END DATE'].diff().dt.days.fillna(0)
    valid['New_Event'] = (valid['Date_Gap'] > 7).astype(int)
    valid['Event_ID'] = valid.groupby(group_cols)['New_Event'].cumsum()

    # require uplift significance
    valid['Valid Event Uplift'] = (
        (valid['Uplift'].notna()) &
        (valid['Uplift'] > 0.2 * valid['Baseline Volume'])
    ).map({True:'Y', False:'N'})
    return valid[valid['Valid Event Uplift']=='Y']
