"""Create PNG charts from the cleaned road accident dataset."""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

ROOT = Path(__file__).resolve().parent
CLEAN = ROOT / "cleaned_roads_dataset.csv"
OUTPUT = ROOT / "analysis_output" / "charts"

sns.set_theme(style="whitegrid", palette="Set2")

def save_bar(series, title, xlabel, filename, horizontal=False, limit=None):
    values = series.dropna().value_counts()
    if limit:
        values = values.head(limit)
    fig, ax = plt.subplots(figsize=(10, 5))
    if horizontal:
        values.sort_values().plot(kind="barh", ax=ax)
        ax.set_xlabel("Accident records")
        ax.set_ylabel(xlabel)
    else:
        values.plot(kind="bar", ax=ax)
        ax.set_xlabel(xlabel)
        ax.set_ylabel("Accident records")
        ax.tick_params(axis="x", rotation=30)
    ax.set_title(title)
    fig.tight_layout()
    fig.savefig(OUTPUT / filename, dpi=160)
    plt.close(fig)

def main():
    if not CLEAN.exists():
        raise FileNotFoundError("Run data_cleaning.py first to create cleaned_roads_dataset.csv")
    df = pd.read_csv(CLEAN, low_memory=False)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    save_bar(df["city"], "Top 10 Cities by Accident Records", "City", "accidents_by_city.png", horizontal=True, limit=10)
    for col, title, name in [("accident_severity", "Accidents by Severity", "accidents_by_severity.png"), ("weather", "Accidents by Weather", "accidents_by_weather.png"), ("road_type", "Accidents by Road Type", "accidents_by_road_type.png"), ("day_of_week", "Accidents by Day of Week", "accidents_by_day.png"), ("cause", "Accidents by Cause", "accidents_by_cause.png")]:
        if col in df:
            save_bar(df[col], title, col.replace("_", " ").title(), name, horizontal=True)
    if "hour" in df:
        hours = pd.to_numeric(df["hour"], errors="coerce").dropna().astype(int).value_counts().reindex(range(24), fill_value=0)
        fig, ax = plt.subplots(figsize=(10, 5))
        hours.plot(kind="line", marker="o", ax=ax)
        ax.set(title="Accidents by Hour", xlabel="Hour of day", ylabel="Accident records", xticks=range(24))
        fig.tight_layout()
        fig.savefig(OUTPUT / "accidents_by_hour.png", dpi=160)
        plt.close(fig)
    if {"risk_score", "casualties"}.issubset(df.columns):
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.scatterplot(data=df, x="risk_score", y="casualties", hue="accident_severity" if "accident_severity" in df else None, alpha=.55, ax=ax)
        ax.set_title("Risk Score Compared with Casualties")
        fig.tight_layout()
        fig.savefig(OUTPUT / "risk_vs_casualties.png", dpi=160)
        plt.close(fig)
    print(f"Charts saved in {OUTPUT}")

if __name__ == "__main__":
    main()
