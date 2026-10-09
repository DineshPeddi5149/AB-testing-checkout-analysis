"""
Generate a small, slightly messy A/B test dataset (checkout page redesign).

control   = current checkout page
treatment = redesigned checkout page

Run:  python generate_dataset.py   ->  raw_ab_test.csv
"""
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
N = 10_000

# ---- clean "true" data -------------------------------------------------------
df = pd.DataFrame({
    "user_id": np.arange(1001, 1001 + N),
    "group": rng.choice(["control", "treatment"], N),
    "date": pd.Timestamp("2026-09-01") + pd.to_timedelta(rng.integers(0, 14, N), unit="D"),
    "device": rng.choice(["mobile", "desktop", "tablet"], N, p=[0.55, 0.37, 0.08]),
    "user_type": rng.choice(["new", "returning"], N, p=[0.65, 0.35]),
})
df["time_on_page"] = (rng.gamma(2.5, 60, N)).round(1)  # seconds

# conversion probability: base 10%, +2pp for treatment, returning users convert more
p = 0.10 + 0.02 * (df["group"] == "treatment") + 0.04 * (df["user_type"] == "returning")
df["converted"] = rng.binomial(1, p)
df["revenue"] = np.where(df["converted"] == 1, rng.lognormal(4.0, 0.5, N), 0).round(2)
df["date"] = df["date"].dt.strftime("%Y-%m-%d")

# ---- inject data quality issues ----------------------------------------------
def pick(frac):
    return rng.choice(N, int(N * frac), replace=False)

i = pick(0.05); df.loc[i, "group"] = df.loc[i, "group"].str.upper()          # 'CONTROL'
i = pick(0.03); df.loc[i, "group"] = " " + df.loc[i, "group"] + " "          # ' treatment '
i = pick(0.04); df.loc[i, "device"] = df.loc[i, "device"].str.capitalize()   # 'Mobile'
df.loc[pick(0.03), "device"] = np.nan                                        # missing device
df.loc[pick(0.03), "time_on_page"] = np.nan                                  # missing time
i = pick(0.002); df.loc[i, "time_on_page"] = -df.loc[i, "time_on_page"]      # impossible negatives
i = pick(0.002); df.loc[i, "time_on_page"] = rng.uniform(5_000, 20_000, len(i)).round(1)  # bots
buyers = df.index[df["converted"] == 1]
j = rng.choice(buyers, 10, replace=False)
df.loc[j, "revenue"] = rng.uniform(1_500, 4_000, 10).round(2)                # a few huge orders

df = pd.concat([df, df.sample(frac=0.02, random_state=1)], ignore_index=True)  # duplicate rows
df = df.sample(frac=1, random_state=1).reset_index(drop=True)

df.to_csv("raw_ab_test.csv", index=False)
print(f"saved raw_ab_test.csv with {len(df):,} rows")
