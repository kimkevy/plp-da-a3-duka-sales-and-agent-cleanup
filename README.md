# Duka Sales Exploration & Mobile-Money Agent Data Cleanup

This repository delivers two comprehensive data analytics engagements:
1. **Engagement 1: Duka Electronics Sales Exploration (H1 2026)** — A multi-dimensional sales analysis across five Kenyan branches (Nairobi, Mombasa, Nakuru, Kisumu, Eldoret), product categories, ordering channels, and calendar dimensions, complete with an Excel executive model.
2. **Engagement 2: Mobile-Money Agent Network Data Cleanup** — A complete data quality audit, cleaning pipeline, referential integrity merge, and reporting framework addressing synthetic real-world data quality anomalies across six data quality dimensions.

---

## How to Regenerate Data & Run the Notebooks

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
2. **Regenerate raw datasets**:
   ```bash
   python generate_data.py
   ```
   This script runs both deterministic generators:
   - **Duka Electronics (`seed 2026`)**: Generates 1,000 sales transactions across H1 2026 saved to `duka_sales.csv`.
   - **Agent Network (`seed 44`)**: Generates 20 registered agents (`agents.csv`) and 612 raw transaction logs (`agent_transactions.csv`) with injected anomalies.
   *(Note: The raw CSVs are excluded from version control via `.gitignore` and are regenerated on demand).*

3. **Execute Notebooks**:
   Open and execute both notebooks from top to bottom:
   - `duka_sales_exploration.ipynb`
   - `agent_cleanup.ipynb`

All required deliverables are saved automatically to `outputs/` and `excel/`.

---

## Duka Electronics: Executive Summary

- Duka Electronics generated KES 110,255,000 in revenue across 1,000 orders during January to June 2026.
- Nakuru led the branches with KES 24,326,000 in revenue and 207 orders.
- Laptops led product revenue at KES 52,815,000, while Smartwatches and Headphones each led units sold with 664 units.
- January was the strongest month at KES 20,238,000, compared with June at KES 16,777,000, a 20.6% difference.
- There were 82 Premium Online orders from Nairobi and Mombasa, worth KES 14,890,000 in total.

The exact values above are regenerated and displayed by the Duka notebook from seed 2026; the notebook is the authoritative report if regenerated data is used.

---

## Agent Network Cleanup: Before & After Metrics

The agent generator creates 612 transaction rows. Deduplication removes 12 rows, leaving 600 unique transactions. The cleaning pipeline standardises transaction types, converts amounts and dates, imputes invalid amounts with the valid-value median, flags IQR outliers, left-merges the agent county, and retains unknown agents with a missing county for governance review.

| Metric | Before Cleaning (Raw) | After Cleaning (Clean) | Notes / Treatment |
| :--- | :---: | :---: | :--- |
| **Transaction Rows** | **612** | **600** | 12 duplicate `txn_id` rows removed (Uniqueness). |
| **Unique Transaction IDs** | 600 | 600 | 100% unique primary keys in clean output. |
| **Valid `txn_type` Values** | 5 variations | 2 standardized | Standardized strictly to `Deposit` & `Withdrawal`. |
| **Missing / N/A Amounts** | 20 | 0 | Coerced to numeric; imputed with median; flagged in `amount_imputed`. |
| **Non-ISO Date Formats** | 5 | 0 | Converted `/` to `-` and formatted as ISO `YYYY-MM-DD`. |
| **Statistical Outliers (IQR)** | - | 5 flagged | KES 250,000 transactions flagged in `is_outlier` and retained. |
| **Agent Merge (Referential)** | 20 agents | 20 agents | Left-merged with `agents.csv`; 8 transactions reference unregistered agent `AG099` (retained with `county = NaN`). |

---

## Repository Deliverables

- `generate_data.py` — Unchanged synthetic generators for both engagements (`seed 2026` and `seed 44`).
- `cleaning_pipeline.py` — Modular cleaning function `clean_agent_data(txns, agents)` returning `(clean_df, log)` with automated rule-based logic.
- `duka_sales_exploration.ipynb` — Full H1 2026 sales exploration notebook with documented 5-minute inspection, derived fields, Tasks 3–7 with Markdown answers beneath the code, and spreadsheet verification.
- `agent_cleanup.ipynb` — Audit analysis, pipeline execution, post-merge validation, county summary, weekly pivot table, and six-dimension Data Quality Report.
- `excel/duka_branch_summary.xlsx` — Multi-tab Excel workbook containing `SalesData`, `Regions`, `BranchSummary` (with Excel `SUMIFS` formulas and `XLOOKUP`), and `PivotTable` (matching Pandas totals).
- `outputs/premium_online_coast_capital.csv` — Filtered high-value e-commerce dataset (Premium price band, Online channel, Nairobi and Mombasa branches) exported with `index=False`.
- `outputs/agent_transactions_clean.csv` — Fully cleaned and enriched agent transactions extract exported with `index=False`.
- `requirements.txt` — Environment dependencies (`pandas`, `numpy`, `openpyxl`).

---

## Data Privacy & Governance Notice

Under the **Kenya Data Protection Act (KDPA) 2019**, any future integration of customer/agent personal data (such as MSISDNs, names, or national identification numbers) must adhere to data minimization, purpose limitation, storage limitation, role-based access control (RBAC), and encryption standards both at rest and in transit.
