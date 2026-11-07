# RoadSafe Analytics

A student project exploring patterns in the supplied Indian road accident dataset. The repository includes the raw dataset, reproducible cleaning and analysis scripts, chart generation, an interactive hotspot map, and the Power BI report.

## Dashboard

Open `RoadSafe_Analytics_Dashboard.pbix` in Power BI Desktop. The report includes KPI cards, filters (slicers), and charts for accident patterns, including city, severity, time, road conditions, and risk. Use the slicers to filter the report. If Power BI asks for the CSV location, select `indian_roads_dataset.csv` in this folder.

## Run the Python workflow

Requires Python 3.10 or later. From this folder run:

```powershell
python -m pip install -r requirements.txt
python data_cleaning.py
python data_analysis.py
python data_visualisation.py
```

`data_cleaning.py` reads `indian_roads_dataset.csv`, drops the mostly empty `festival` field, parses dates and times, derives hour and minute columns, and writes `cleaned_roads_dataset.csv`. `data_analysis.py` writes grouped CSV summaries to `analysis_output/`. `data_visualisation.py` saves PNG charts to `analysis_output/charts/`.

## Files

- `indian_roads_dataset.csv`: provided source data
- `cleaned_roads_dataset.csv`: generated cleaned data (created by the cleaning script)
- `data_cleaning.py`, `data_analysis.py`, `data_visualisation.py`: project scripts
- `RoadSafe_Analytics_Dashboard.pbix`: Power BI report
- `accident_hotspots_map.html`: interactive accident location map

The dataset contains observational records; charts describe patterns in the supplied data and do not establish causes.
