from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]

DATA_PATH = ROOT / "data" / "processed" / "csad_timeseries.csv"
FIGURES_DIR = ROOT / "figures"

FIGURES_DIR.mkdir(exist_ok=True)

df = pd.read_csv(DATA_PATH)

# Figure 1
plt.figure(figsize=(10,5))
plt.plot(df["time"], df["csad"])
plt.xticks(rotation=45)
plt.xlabel("Quarter")
plt.ylabel("CSAD")
plt.title("Quarterly CSAD in European Housing Markets")
plt.tight_layout()

plt.savefig(FIGURES_DIR / "csad_timeseries.png", dpi=300)
plt.close()

# Figure 2
plt.figure(figsize=(7,5))
plt.scatter(df["rm"], df["csad"])

plt.xlabel("Aggregate Market Return")
plt.ylabel("CSAD")
plt.title("Aggregate Market Returns and Cross-Sectional Dispersion")

plt.tight_layout()

plt.savefig(FIGURES_DIR / "csad_scatter.png", dpi=300)
plt.close()

print("Done.")