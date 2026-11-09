"""Summarize road accident patterns and save CSV tables for the dashboard."""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent
CLEAN = ROOT / "cleaned_roads_dataset.csv"
OUTPUT = ROOT / "analysis_output"

def main():
    if not CLEAN.exists():
        raise FileNotFoundError("Run data_cleaning.py first to create cleaned_roads_dataset.csv")
    df = pd.read_csv(CLEAN, parse_dates=["date"], low_memory=False)
    OUTPUT.mkdir(exist_ok=True)
    print("ROAD ACCIDENT DATA ANALYSIS")
    print(f"Accident records: {len(df):,}")
    print(f"Total casualties: {df['casualties'].sum():,.0f}")
    if "risk_score" in df:
        print(f"Average risk score: {df['risk_score'].mean():.3f}")
    for col in ["city", "accident_severity", "weather", "cause", "road_type", "day_of_week"]:
        if col in df:
            print(f"\nRecords by {col}:\n{df[col].fillna('Unknown').value_counts().to_string()}")
    if "city" in df:
        city = df.assign(city=df["city"].fillna("Unknown")).groupby("city").agg(
            total_accidents=("accident_id", "nunique"),
            total_casualties=("casualties", "sum"),
            average_risk_score=("risk_score", "mean"),
        ).sort_values("total_accidents", ascending=False)
        city.to_csv(OUTPUT / "city_analysis.csv")
    for col, filename in [("accident_severity", "severity_analysis.csv"), ("hour", "hour_analysis.csv"), ("weather", "weather_analysis.csv"), ("cause", "cause_analysis.csv"), ("road_type", "road_type_analysis.csv")]:
        if col in df:
            df.groupby(col, dropna=False).agg(
                total_accidents=("accident_id", "nunique"),
                total_casualties=("casualties", "sum"),
                average_risk_score=("risk_score", "mean"),
            ).sort_values("total_accidents", ascending=False).to_csv(OUTPUT / filename)
    print(f"\nSummary tables saved in {OUTPUT}")

if __name__ == "__main__":
    main()
