from pathlib import Path

import pandas as pd

csv_path = Path(__file__).with_name("indian_roads_dataset.csv")
output_path = Path(__file__).with_name("cleaned_roads_dataset.csv")

df = pd.read_csv(csv_path)

print("First 5 rows:")
print(df.head())

print("\nMissing values per column:")
print(df.isna().sum())

# Parse dates and times; invalid values become missing instead of stopping the script.
df["date"] = pd.to_datetime(df["date"], errors="coerce")
parsed_time = pd.to_datetime(
    df["time"].astype(str),
    format="%H:%M",
    errors="coerce",
)

# Extract time parts only if parsing succeeded.
df["accident_hour"] = parsed_time.dt.hour
df["accident_minute"] = parsed_time.dt.minute

# Keep the existing hour field; compare it with the parsed time if useful.
if "hour" in df.columns:
    mismatch_count = (
        df["hour"].notna()
        & df["accident_hour"].notna()
        & (df["hour"] != df["accident_hour"])
    ).sum()
    print(f"\nRows where existing hour differs from time: {mismatch_count}")

print("\nData types after cleaning:")
df.info()

df.to_csv(output_path, index=False)
print(f"\nCleaned dataset saved to: {output_path}")
df = pd.read_csv(csv_path)
df = df.drop(columns=["festival"], errors="ignore")