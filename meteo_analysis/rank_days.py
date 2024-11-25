import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('data/average_wind_23_24.csv')

# Convert valid_time to date
df['date'] = pd.to_datetime(df['valid_time']).dt.date

# Group by date and isobaricInhPa to get daily averages for each pressure level
daily_avg_per_pressure = df.groupby(['date', 'isobaricInhPa'])['avg_total_wind_speed'].mean().reset_index()

# Group by date only to get daily averages across all pressure levels
daily_avg_all_pressures = df.groupby('date')['avg_total_wind_speed'].mean().reset_index()
daily_avg_all_pressures['isobaricInhPa'] = 'all'  # Label for overall average

# Concatenate the two DataFrames
result = pd.concat([daily_avg_per_pressure, daily_avg_all_pressures], ignore_index=True)

# Rename columns for clarity if desired
result = result.rename(columns={'avg_total_wind_speed': 'daily_avg_wind_speed'})

# Set custom order for isobaricInhPa levels
result['isobaricInhPa'] = pd.Categorical(result['isobaricInhPa'], categories=['all', 1000.0, 800.0, 400.0], ordered=True)

# Sort by daily average wind speed for rows where isobaricInhPa is 'all'
dates = result[result['isobaricInhPa']=='all'].sort_values(by=['daily_avg_wind_speed'])
result['date'] = pd.Categorical(result['date'], categories=dates['date'], ordered=True)
result_sorted = result.sort_values(by='date')

# Factorize unique dates and create a mapping
result_sorted['unique_date_number'] = pd.factorize(result_sorted['date'])[0] + 1  # +1 to start numbering from 1

result_sorted.to_csv('data/days_ranked_lowest_wind_23_24.csv', index=False)

sns.lineplot(data = result_sorted, x = 'unique_date_number', y = 'daily_avg_wind_speed', hue = 'isobaricInhPa')
plt.show()
