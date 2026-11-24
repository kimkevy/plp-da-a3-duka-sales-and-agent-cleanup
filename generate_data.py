import numpy as np
import pandas as pd

# Generator 1: Duka Electronics (seed 2026)
rng_duka = np.random.default_rng(2026)
n_duka = 1000
products_duka = {
    "Laptop": 105000,
    "Phone": 40000,
    "Tablet": 28000,
    "Headphones": 8500,
    "Smartwatch": 18000,
}
duka_sales = pd.DataFrame({
    "order_id": range(1001, 1001 + n_duka),
    "order_date": pd.date_range("2026-01-01", "2026-06-30", periods=n_duka),
    "branch": rng_duka.choice(["Nairobi", "Mombasa", "Nakuru", "Kisumu", "Eldoret"], n_duka),
    "product": rng_duka.choice(list(products_duka.keys()), n_duka),
    "quantity": rng_duka.integers(1, 6, n_duka),
    "channel": rng_duka.choice(["In-store", "Online", "Phone order"], n_duka, p=[0.55, 0.35, 0.10]),
})
duka_sales["unit_price"] = duka_sales["product"].map(products_duka)
duka_sales.to_csv("duka_sales.csv", index=False)

# Generator 2: Agent Network (seed 44)
rng = np.random.default_rng(44)
n = 600
agents = pd.DataFrame({
    "agent_id": [f"AG{i:03d}" for i in range(1, 21)],
    "county": rng.choice(["Nairobi", "Kiambu", "Nakuru", "Mombasa", "Kisumu"], 20),
    "onboarded": pd.date_range("2024-01-01", periods=20, freq="MS").strftime("%Y-%m-%d"),
})
txns = pd.DataFrame({
    "txn_id": [f"TX{i:05d}" for i in range(1, n + 1)],
    "agent_id": rng.choice(agents["agent_id"], n),
    "txn_type": rng.choice(["Deposit", "withdrawal", "DEPOSIT ", "Withdrawal", "deposit"], n),
    "amount": rng.lognormal(7.5, 0.8, n).round(0).astype(str),
    "txn_date": (pd.to_datetime("2026-03-01") + pd.to_timedelta(rng.integers(0, 60, n), unit="D")).strftime("%Y-%m-%d"),
})
idx = rng.choice(n, 30, replace=False)
txns.loc[idx[:15], "amount"] = np.nan
txns.loc[idx[15:20], "amount"] = "N/A"
txns.loc[idx[20:25], "amount"] = "250000"
txns.loc[idx[25:], "txn_date"] = txns.loc[idx[25:], "txn_date"].str.replace("-", "/")
txns = pd.concat([txns, txns.sample(12, random_state=1)], ignore_index=True)
txns.loc[rng.choice(len(txns), 8, replace=False), "agent_id"] = "AG099"

agents.to_csv("agents.csv", index=False)
txns.to_csv("agent_transactions.csv", index=False)

