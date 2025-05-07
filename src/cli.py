import argparse
from pathlib import Path

import pandas as pd

from src.data_loading import load_data
from src.baseline_price import calculate_baseline_price
from src.baseline_volume import calculate_baseline_volume
from src.promo_events import flag_and_identify_promos
from src.promo_bins import compute_depth_and_duration_bins

def main():
    parser = argparse.ArgumentParser(description="Promo Event Analysis Pipeline")
    parser.add_argument(
        "--input", "-i",
        required=True,
        help="Path to raw sell-out data (CSV or XLSX)"
    )
    parser.add_argument(
        "--out-clean", "-c",
        default="sample_data_cleaned.xlsx",
        help="Where to write the cleaned week-level dataset"
    )
    parser.add_argument(
        "--out-events", "-e",
        default="sample_data_events.xlsx",
        help="Where to write the promo-events summary workbook"
    )
    args = parser.parse_args()

    # 1. Load data
    df = load_data(args.input, skiprows=0)

    # 2. Compute baseline price & volume
    df = calculate_baseline_price(df)
    df = calculate_baseline_volume(df)

    # 3. Flag promos and identify valid promo‐week events
    valid = flag_and_identify_promos(df)

    # 4. Compute promo_depth_pct on the main df so it's available in valid
    df['promo_depth_pct'] = 1.0 - (df['PROMO PRICE'] / df['Baseline Price'])

    # 5. Bucket depth & duration for each valid event
    events = compute_depth_and_duration_bins(valid)

    # Ensure output directories exist
    Path(args.out_clean).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out_events).parent.mkdir(parents=True, exist_ok=True)

    # 6. Save outputs
    df.to_excel(args.out_clean, index=False)
    events.to_excel(args.out_events, sheet_name="Weekly", index=False)

    print(f"Cleaned data written to {args.out_clean}")
    print(f"Event summary written to {args.out_events}")

if __name__ == "__main__":
    main()
