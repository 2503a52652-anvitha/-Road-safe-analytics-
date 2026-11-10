from pathlib import Path

import pandas as pd

csv_path = Path(__file__).with_name('indian_roads_dataset.csv')
df = pd.read_csv(csv_path)
print(df.head())
print('Missing values per column:')
print(df.isnull().sum())
print('\nData types of each column:')
df.info()
df= df.drop('festival', axis=1)
print('Dropped the \'festival\' column due to many missing values.')
df['date'] = pd.to_datetime(df['date'])
df['time'] = pd.to_datetime(df['time'], format='%H:%M').dt.time
print('Converted \'date\' and \'time\' columns to datetime objects.')
df.info()
df['accident_hour'] = df['time'].map(lambda time_value: time_value.hour)
df['accident_minute'] = df['time'].map(lambda time_value: time_value.minute)
print("Extracted 'hour' and 'minute' into new columns: 'accident_hour' and 'accident_minute'.")
print(df[['time', 'accident_hour', 'accident_minute']].head())