from config import EUROSTAT_HPI_URL
import io
import gzip
import requests
import pandas as pd

URL = URL = EUROSTAT_HPI_URL

def download_hpi():
    print("Downloading Eurostat HPI data...")
    r = requests.get(URL, timeout=60)
    r.raise_for_status()

    content = r.content

    # Eurostat often compresses responses
    try:
        content = gzip.decompress(content)
    except OSError:
        pass

    df = pd.read_csv(io.BytesIO(content))

    # Standardize column names
    df.columns = [c.lower() for c in df.columns]

    df = df.rename(columns={
        "time_period": "time",
        "obs_value": "hpi",
        "geo": "geo"
    })

    df = df[["geo", "time", "hpi"]].dropna()

    df.to_csv("data/processed/hpi_raw.csv", index=False)
    print("Saved data/processed/hpi_raw.csv")

if __name__ == "__main__":
    download_hpi()
