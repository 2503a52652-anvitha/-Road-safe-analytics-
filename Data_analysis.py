from pathlib import Path

import pandas as pd

# Load the dataset from the folder containing this script.
PROJECT_DIR = Path(__file__).resolve().parent
DATA_PATH = PROJECT_DIR / "indian_roads_dataset.csv"
OUTPUT_DIR = PROJECT_DIR / "analysis_output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

if not DATA_PATH.exists():
    raise FileNotFoundError(
        f"Could not find {DATA_PATH.name}. Put the CSV beside this script."
    )

df = pd.read_csv(DATA_PATH)

# Check that the analysis fields exist.
required_columns = [
    "accident_id", "city", "state", "date", "hour", "day_of_week",
    "road_type", "weather", "traffic_density", "cause",
    "accident_severity", "casualties", "vehicles_involved", "risk_score",
]
missing_columns = [col for col in required_columns if col not in df.columns]
if missing_columns:
    raise ValueError(f"Missing required columns: {missing_columns}")

# Convert values to useful types and handle invalid entries.
for col in ["hour", "casualties", "vehicles_involved", "risk_score"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df["date"] = pd.to_datetime(df["date"], errors="coerce")
df["city"] = df["city"].fillna("Unknown")
df["state"] = df["state"].fillna("Unknown")

def print_counts(title, column):
    print(f"\n{title}")
    print(df[column].fillna("Unknown").value_counts().to_string())

# Overall summary
print("=" * 55)
print("ROAD ACCIDENT DATA ANALYSIS")
print("=" * 55)
print(f"Dataset records: {len(df):,}")
print(f"Unique accidents: {df['accident_id'].nunique():,}")
print(f"Total casualties: {df['casualties'].sum():,.0f}")
print(f"Average casualties per record: {df['casualties'].mean():.2f}")
print(f"Average risk score: {df['risk_score'].mean():.3f}")

valid_dates = df["date"].dropna()
if not valid_dates.empty:
    print(f"Date range: {valid_dates.min():%Y-%m-%d} to {valid_dates.max():%Y-%m-%d}")

# Category summaries
print_counts("Accidents by state", "state")
print_counts("Top 10 cities by accident records", "city")
print_counts("Accidents by severity", "accident_severity")
print_counts("Accidents by cause", "cause")
print_counts("Accidents by weather", "weather")
print_counts("Accidents by road type", "road_type")
print_counts("Accidents by traffic density", "traffic_density")
print_counts("Accidents by day of week", "day_of_week")

# Accident counts by hour, in chronological order
print("\nAccidents by hour")
hour_counts = df["hour"].dropna().astype(int).value_counts().sort_index()
print(hour_counts.to_string())

# Compare severity across road types
print("\nSeverity by road type (row percentages)")
severity_by_road = pd.crosstab(
    df["road_type"].fillna("Unknown"),
    df["accident_severity"].fillna("Unknown"),
    normalize="index",
).mul(100).round(1)
print(severity_by_road.to_string())

# City-level summary
city_summary = (
    df.groupby("city")
    .agg(
        total_accidents=("accident_id", "nunique"),
        total_casualties=("casualties", "sum"),
        average_risk_score=("risk_score", "mean"),
    )
    .sort_values("total_accidents", ascending=False)
)
city_summary["average_risk_score"] = city_summary["average_risk_score"].round(3)

summary_path = OUTPUT_DIR / "city_analysis.csv"
city_summary.to_csv(summary_path)

# Save additional tables for use in the report or Power BI.
severity_summary = (
    df["accident_severity"]
    .fillna("Unknown")
    .value_counts()
    .rename_axis("accident_severity")
    .reset_index(name="accident_records")
)
severity_summary.to_csv(OUTPUT_DIR / "severity_analysis.csv", index=False)

hour_summary = (
    hour_counts.rename_axis("hour")
    .reset_index(name="accident_records")
)
hour_summary.to_csv(OUTPUT_DIR / "hour_analysis.csv", index=False)

print(f"\nAnalysis complete. Results saved in: {OUTPUT_DIR}")