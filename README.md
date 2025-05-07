# Promo Event Analysis Pipeline

This repository provides a complete end-to-end Python pipeline to transform raw weekly Nielsen (or EPOS) sell-out data into detailed promotional event analytics. It:

* **Identifies promo weeks** based on volume share and discount depth rules
* **Calculates baseline price** (80th percentile non-promo price) and **baseline volume**
* **Computes uplift** of sales during valid promo weeks
* **Clusters consecutive promo weeks** into distinct events (`Event_ID`) using date gaps
* **Measures event metrics**: duration (in weeks), median depth (% discount), uplift significance
* **Buckets events** by depth intervals and duration categories for BI reporting

---

## 📂 Repository Structure

```text
promo-event-analysis/
├── data/                    # Example or synthetic CSV for demo
│   └── sample_data.csv      # Minimal dataset matching expected schema
├── notebooks/               # Jupyter notebooks demonstrating each step
│   └── sell_out.ipynb       # End-to-end demo wiring together your core functions
├── src/                     # Reusable modules implementing each pipeline stage
│   ├── data_loading.py      # 1. Load CSV/Excel, clean column names, parse dates
│   ├── baseline_price.py    # 2. Compute baseline price (quantile of non-promo price)
│   ├── baseline_volume.py   # 3. Compute baseline volume (mean non-promo units)
│   ├── promo_events.py      # 4. Flag promo weeks, filter anomalies, cluster Event_IDs
│   ├── promo_bins.py        # 5. Compute depth & duration buckets for events
│   └── cli.py               # CLI wrapper to run full pipeline from terminal
└── README.md                # This document (with instructions & overview)
```

## 📝 Expected Input Schema

The pipeline requires a tabular file (Excel or CSV) with at least:

| Column                                                         | Type    | Description                   |
| -------------------------------------------------------------- | ------- | ----------------------------- |
| `Markets`                                                      | string  | Retailer/channel identifier   |
| `END DATE`                                                     | date    | Week ending date (YYYY-MM-DD) |
| `BRAND`, `PACK TYPE`, `ACTUAL PACK SIZE`                       | string  | SKU identifiers               |
| `NON-PROMO PRICE`, `PROMO PRICE`                               | numeric | Regular vs. promo price       |
| `Sales Units`, `Sales Units Any Promo`, `Sales Units No Promo` | numeric | Volume metrics                |

*(Additional columns are optional for extended analysis.)*

## ▶️ Running the Pipeline

### 1️⃣ As a script via CLI

```bash
python -m src.cli \
  --input data/sample_data.csv \
  --sample_data_cleaned.xlsx \
  --sample_data_events.xlsx
```

This will produce:

* `sample_data_cleaned.xlsx`: full week‑level dataset with flags, uplift, baseline columns
* `sample_data_events.xlsx`: promo events with duration, depth, buckets, and counts

### 2️⃣ Within a notebook

1. Open `notebook/sell_out.ipynb` in Jupyter
2. Set `INPUT_PATH` and `OUTPUT_DIR` variables at the top
3. Run cells to see intermediate outputs 

## 🧩 Key Pipeline Steps

1. **Data Loading & Cleaning** – standardize column names, parse dates
2. **Baseline Calculation** – 80th percentile non‑promo price; mean non‑promo volume
3. **Promo Week Flagging** – identify weeks with >50% promo volume and ≥5% discount
4. **Anomaly Filtering** – remove low-volume weeks despite deep cuts
5. **Uplift Computation** – promo units minus baseline volume
6. **Event Clustering** – date‑gap method to assign `Event_ID`
7. **Metric Aggregation** – median discount depth, event duration, significance check
8. **Bucketing** – categorize by depth intervals (5% bands) and duration labels

## 🔍 Customization

* **Quantile parameter** for baseline price can be adjusted in `baseline.py`
* **Thresholds** for promo flags (volume share, discount %) in `promo_flags.py`
* **Gap days** for new events and uplift significance multiply in `event_detection.py`

## 💡 Business Significance
* Promotional volume can represent 20–80 % of annual volume in FMCG, yet poorly targeted tactics erode margin. This pipeline turns raw Nielsen (or EPOS) **sell‑out** data into actionable metrics—flagging promo weeks, clustering them into coherent events, and quantifying true sales uplift after baseline correction. By analysing uplift **directly from sell‑out**, teams can **benchmark competitors on the exact same shelf conditions** and capture real promo elasticity at the *end‑aisle* (where execution is often chaotic and non‑linear). The event‑level depth and duration buckets reveal which discounts drive volume versus which simply subsidise sales, while the high granularity and audit accuracy of Nielsen data ensure the insights are trustworthy and ready for trade‑spend optimisation and promo‑calendar design.

---

