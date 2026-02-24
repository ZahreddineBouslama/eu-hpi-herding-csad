import pandas as pd
import numpy as np

# ----------------------------
# 1. Helper: convert to quarterly PeriodIndex
# ----------------------------
def to_period_q(series: pd.Series) -> pd.PeriodIndex:
    return pd.PeriodIndex(series.astype(str).str.replace(" ", ""), freq="Q")


# ----------------------------
# 2. Load data
# ----------------------------
print("Loading HPI data...")
df = pd.read_csv("data/processed/hpi_raw.csv")

df.columns = [c.lower() for c in df.columns]
df = df[["geo", "time", "hpi"]].copy()

# ----------------------------
# 3. Clean
# ----------------------------
df["time"] = to_period_q(df["time"])
df["hpi"] = pd.to_numeric(df["hpi"], errors="coerce")
df = df.dropna(subset=["hpi"])
df = df.sort_values(["geo", "time"])

print("Countries:", df["geo"].nunique())
print("Time range:", df["time"].min(), "to", df["time"].max())

# ----------------------------
# 4. Compute log returns
# ----------------------------
df["ret"] = df.groupby("geo")["hpi"].transform(lambda x: np.log(x).diff())
df = df.dropna(subset=["ret"])

# ----------------------------
# 5. Compute market return (equal-weighted)
# ----------------------------
market = (
    df.groupby("time", as_index=False)["ret"]
    .mean()
    .rename(columns={"ret": "rm"})
)

# Merge market return back to full panel
df = df.merge(market, on="time", how="left")

# ----------------------------
# 6. Compute CSAD
# ----------------------------
df["abs_dev"] = (df["ret"] - df["rm"]).abs()

csad = (
    df.groupby("time", as_index=False)
    .agg(
        csad=("abs_dev", "mean"),
        rm=("rm", "first")   # keep market return
    )
)

csad["abs_rm"] = csad["rm"].abs()
csad["rm2"] = csad["rm"] ** 2

# ----------------------------
# 7. Save
# ----------------------------
csad.to_csv("data/processed/csad_timeseries.csv", index=False)

print("\nSaved data/processed/csad_timeseries.csv")
print("\nFirst rows:")
print(csad.head())

print("\nFinal time range:",
      csad["time"].min(), "to", csad["time"].max())
print("Number of quarters:", len(csad))