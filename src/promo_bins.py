import pandas as pd

def compute_depth_and_duration_bins(
    valid: pd.DataFrame,
    group_cols = ['Markets', 'YEAR', 'Brand_Pack_PackType', 'Event_ID']
) -> pd.DataFrame:
    """
    5. Promo Depth and Duration Bins
    - Uses promo_depth_pct already on df/valid
    - Computes event-level median depth, depth buckets
    - Computes duration, duration buckets
    """
    # median depth per event
    depth_df = (
        valid
          .groupby(group_cols)['promo_depth_pct']
          .median()
          .reset_index(name='event_median_depth')
    )

    # depth buckets
    bins = [0.05,0.10,0.15,0.20,0.25,0.30,0.35,0.40,0.45,
            0.50,0.55,0.60,0.65,0.70,0.75,0.80,1.10]
    labels = ['5–9.99%','10–14.99%','15–19.99%','20–24.99%','25–29.99%',
              '30–34.99%','35–39.99%','40–44.99%','45–49.99%','50–54.99%',
              '55–59.99%','60–64.99%','65–69.99%','70–74.99%','75–79.99%','80%+']
    depth_df['depth_bucket'] = pd.cut(
        depth_df['event_median_depth'], bins=bins, labels=labels, right=False
    )

    # duration per event
    dur_df = (
        valid
          .groupby(group_cols)['Event_ID']
          .size()
          .reset_index(name='Event Duration (weeks)')
    )

    # duration & depth aggregate stats
    stats = (
        valid
          .groupby(group_cols)
          .agg(
              Event_Duration=('Event_ID','size'),
              Max_Depth=('promo_depth_pct','max')
          )
          .reset_index()
    )
    stats['Duration Bucket'] = pd.cut(
        stats['Event_Duration'], bins=[0,3,6,float('inf')],
        labels=['Short','Medium','Long'], right=True
    )
    stats['Depth Bucket'] = pd.cut(
        stats['Max_Depth'], bins=[-1,0.10,0.20,1.10],
        labels=['Shallow','Medium','Deep'], right=False
    )

    # merge everything back
    out = valid.merge(depth_df, on=group_cols, how='left')
    out = out.merge(dur_df,   on=group_cols, how='left')
    out = out.merge(stats[[*group_cols, 'Duration Bucket','Depth Bucket']], on=group_cols, how='left')
    return out
