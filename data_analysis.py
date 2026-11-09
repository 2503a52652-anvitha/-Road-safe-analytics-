"""Summarize road accident patterns and write dashboard tables."""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent
CLEAN = ROOT / "cleaned_roads_dataset.csv"
OUTPUT = ROOT / "analysis_output"


def main():
    if not CLEAN.exists():
        raise FileNotFoundError("Run data_cleaning.py first to create cleaned_roads_dataset.csv")

    df = pd.read_csv(CLEAN, parse_dates=["date"], low_memory=False)
    required = ["accident_id", "city", "date", "hour", "day_of_week", "road_type", "weather", "accident_severity", "casualties", "risk_score"]
    missing = [column for column in required if column not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    OUTPUT.mkdir(parents=True, exist_ok=True)
    df["city"] = df["city"].fillna("Unknown")
    print("ROAD ACCIDENT DATA ANALYSIS")
    print(f"Dataset records: {len(df):,}")
    print(f"Unique accidents: {df['accident_id'].nunique():,}")
    print(f"Total casualties: {df['casualties'].sum():,.0f}")
    print(f"Average casualties per record: {df['casualties'].mean():.2f}")
    print(f"Average risk score: {df['risk_score'].mean():.3f}")
    valid_dates = df["date"].dropna()
    if not valid_dates.empty:
        print(f"Date range: {valid_dates.min():%Y-%m-%d} to {valid_dates.max():%Y-%m-%d}")

    for column in ["state", "city", "accident_severity", "cause", "weather", "road_type", "traffic_density", "day_of_week"]:
        if column in df:
            print(f"\nAccidents by {column}:\n{df[column].fillna('Unknown').value_counts().to_string()}")

    hour_counts = pd.to_numeric(df["hour"], errors="coerce").dropna().astype(int).value_counts().sort_index()
    print(f"\nAccidents by hour:\n{hour_counts.to_string()}")
    severity_by_road = pd.crosstab(
        df["road_type"].fillna("Unknown"),
        df["accident_severity"].fillna("Unknown"),
        normalize="index",
    ).mul(100).round(1)
    print(f"\nSeverity by road type (row percentages):\n{severity_by_road.to_string()}")

    city_summary = df.groupby("city").agg(
        total_accidents=("accident_id", "nunique"),
        total_casualties=("casualties", "sum"),
        average_risk_score=("risk_score", "mean"),
    ).sort_values("total_accidents", ascending=False)
    city_summary["average_risk_score"] = city_summary["average_risk_score"].round(3)
    city_summary.to_csv(OUTPUT / "city_analysis.csv")

    for column, filename in [
        ("accident_severity", "severity_analysis.csv"),
        ("hour", "hour_analysis.csv"),
        ("weather", "weather_analysis.csv"),
        ("cause", "cause_analysis.csv"),
        ("road_type", "road_type_analysis.csv"),
    ]:
        if column in df:
            summary = df.groupby(column, dropna=False).agg(
                total_accidents=("accident_id", "nunique"),
                total_casualties=("casualties", "sum"),
                average_risk_score=("risk_score", "mean"),
            ).sort_values("total_accidents", ascending=False)
            summary.to_csv(OUTPUT / filename)

    print(f"\nSummary tables saved in {OUTPUT}")


if __name__ == "__main__":
    main()
