import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.colors as mcolors
import cartopy.crs as ccrs
import cartopy.feature as cfeature

from datetime import datetime

df = pd.read_csv('data/flights_sample_1_hour.csv')
df = df.sort_values('time')

feature_to_plot = 'geoaltitude'

sns.lineplot(data=df, x = 'time', y = feature_to_plot, hue = 'icao24')
plt.show()