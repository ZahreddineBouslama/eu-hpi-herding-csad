import pandas as pd
import numpy as np
import statsmodels.api as sm
import os

# Ensure output folders exist
os.makedirs("outputs/tables", exist_ok=True)

print("Loading CSAD time series...")
csad = pd.read_csv("data/processed/csad_timeseries.csv")

# Standardize column names
csad.columns = [c.lower() for c in csad.columns]

# ----------------------------
# Helper: run baseline regression with HAC standard errors
# CSAD_t = a + b1*|Rm| + b2*Rm^2 + e
# Herding evidence: b2 < 0
# ----------------------------
def run_model(df: pd.DataFrame, label: str):
    X = df[["abs_rm", "rm2"]].copy()
    X = sm.add_constant(X)
    y = df["csad"]

    # Quarterly data -> HAC with maxlags=4 is a common, defensible choice
    model = sm.OLS(y, X).fit(cov_type="HAC", cov_kwds={"maxlags": 4})

    # Build a neat summary table
    out = pd.DataFrame({
        "model": label,
        "term": model.params.index,
        "coef": model.params.values,
        "se_hac": model.bse.values,
        "t": model.tvalues.values,
        "p": model.pvalues.values
    })

    # Add fit stats (repeat on all rows for convenience)
    out["n"] = int(model.nobs)
    out["r2"] = model.rsquared
    out["adj_r2"] = model.rsquared_adj

    return model, out


# ----------------------------
# 1) Baseline model (full sample)
# ----------------------------
m_base, t_base = run_model(csad, "baseline_full")

# ----------------------------
# 2) Asymmetry: up vs down markets
# ----------------------------
csad_up = csad[csad["rm"] > 0].copy()
csad_down = csad[csad["rm"] < 0].copy()

m_up, t_up = run_model(csad_up, "up_markets")
m_down, t_down = run_model(csad_down, "down_markets")

# ----------------------------
# 3) Extreme markets (top 10% of |Rm|)
# ----------------------------
thr = csad["abs_rm"].quantile(0.90)
csad_ext = csad[csad["abs_rm"] >= thr].copy()

m_ext, t_ext = run_model(csad_ext, "extreme_top10pct_abs_rm")

# ----------------------------
# 4) Combine & save regression table
# ----------------------------
table = pd.concat([t_base, t_up, t_down, t_ext], ignore_index=True)
table.to_csv("outputs/tables/csad_regressions_hac.csv", index=False)

print("\nSaved outputs/tables/csad_regressions_hac.csv")

# Print baseline summary to terminal (useful for quick interpretation)
print("\n=== BASELINE (FULL SAMPLE) ===")
print(m_base.summary())

print("\nKey herding test: coefficient on rm2 should be NEGATIVE for herding evidence.")