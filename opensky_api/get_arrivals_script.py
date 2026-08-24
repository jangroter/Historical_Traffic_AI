from pyopensky.trino import Trino
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt
from time import sleep
import seaborn as sns

load_data = True
save_data = False

folder = "figures/hourly_arrivals"
data = "july_2024"

# Create a dictionary of filenames and labels
data = {
    'January': f"{folder}/jan_2024.csv",
    'March': f"{folder}/march_2024.csv",
    'July': f"{folder}/july_2024.csv"
}

if not load_data:
    # Initialize parameters
    airport_icao = 'EHAM'
    start_date = datetime(2024, 7, 1)
    end_date = datetime(2024, 8, 1)  # exclusive
    trino = Trino()

    # Storage for flight data
    all_flights = []

    # Fetch data in daily batches
    current = start_date
    while current < end_date:
        next_day = current + timedelta(days=10)
        try:
            df = trino.flightlist(
                start=current,
                stop=next_day,
                arrival_airport=airport_icao
            )
            if df is not None and not df.empty:
                all_flights.append(df)
        except Exception as e:
            print(f"Error fetching data for {current.date()}: {e}")
        current = next_day


    # Combine all daily dataframes into one
    flights_df = pd.concat(all_flights, ignore_index=True)

    # Convert arrival time to datetime and round to the hour
    flights_df['arrival_hour'] = pd.to_datetime(flights_df['lastseen']).dt.floor('h')

    # Count arrivals per hour
    arrival_counts = flights_df['arrival_hour'].value_counts().sort_index()
    if save_data:
        arrival_counts.to_csv(f"{folder}/{data}.csv", index=False)

if load_data:
    if type(data) == str:
        arrival_counts = pd.read_csv(f"{folder}/{data}.csv")

    elif type(data) == dict:
        # Read and tag each file
        dfs = []
        for month, file in data.items():
            df = pd.read_csv(file)
            df['Month'] = month  # add label column
            dfs.append(df)

        # Combine into one big DataFrame
        arrival_counts = pd.concat(dfs, ignore_index=True)

# Plotting the histogram
plt.figure(figsize=(10, 4))
bins = max(arrival_counts['count'])
# sns.histplot(arrival_counts, x="count", bins=bins,hue='month')
sns.kdeplot(arrival_counts, x="count",hue='Month', bw_adjust=0.7)
# Title and labels
# plt.title('Hourly Arrivals at Schiphol (EHAM)')
plt.xlabel('Hourly Rate')
plt.ylabel('Frequency')
plt.yticks([])
plt.xlim([0, 80])

# Remove top and right spines
sns.despine(top=True, right=True)

# Remove grid
plt.grid(False)

# Adjust layout
plt.tight_layout()

# Show plot
plt.show()

# Create a dictionary of filenames and labels
files = {
    'January': f"{folder}/jan_2024.csv",
    'February': f"{folder}/march_2024.csv",
    'March': f"{folder}/july_2024.csv"
}

# Read and tag each file
dfs = []
for month, file in files.items():
    df = pd.read_csv(file)
    df['Month'] = month  # add label column
    dfs.append(df)

# Combine into one big DataFrame
data = pd.concat(dfs, ignore_index=True)