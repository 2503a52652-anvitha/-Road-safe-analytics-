"""Clean the Indian road accident dataset for analysis and Power BI."""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "indian_roads_dataset.csv"
OUTPUT = ROOT / "cleaned_roads_dataset.csv"

def main():
    if not SOURCE.exists():
        raise FileNotFoundError(f"Dataset not found: {SOURCE}")
    df = pd.read_csv(SOURCE)
    print(f"Loaded {len(df):,} rows and {len(df.columns)} columns")
    print("Missing values before cleaning:\n", df.isna().sum().to_string())

    if "accident_id" in df.columns:
        duplicate_count = int(df.duplicated(subset=["accident_id"]).sum())
        if duplicate_count:
            df = df.drop_duplicates(subset=["accident_id"], keep="first")
        print(f"Removed {duplicate_count:,} duplicate accident IDs")

    # The source's festival field is almost entirely blank and is omitted from analysis.
    df = df.drop(columns=["festival"], errors="ignore")
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
    if "time" in df.columns:
        parsed_time = pd.to_datetime(df["time"].astype("string"), format="%H:%M", errors="coerce")
        df["accident_hour"] = parsed_time.dt.hour
        df["accident_minute"] = parsed_time.dt.minute
    for column in ["hour", "casualties", "vehicles_involved", "risk_score", "latitude", "longitude"]:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")

    df.to_csv(OUTPUT, index=False, date_format="%Y-%m-%d")
    print(f"Saved cleaned data ({len(df):,} rows) to {OUTPUT}")
    print("Missing values after cleaning:\n", df.isna().sum().to_string())

if __name__ == "__main__":
    main()
