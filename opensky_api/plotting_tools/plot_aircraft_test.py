import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import cartopy.crs as ccrs
import cartopy.feature as cfeature

from datetime import datetime

df = pd.read_csv('data/flights_sample_1_hour.csv')
df = df.sort_values('time')
# df[df['geoaltitude']>12000] = 12000

# Set up the map with Cartopy
fig, ax = plt.subplots(figsize=(6, 5), subplot_kw={'projection': ccrs.PlateCarree()})
ax.set_extent([1, 9, 48, 55], crs=ccrs.PlateCarree())
ax.add_feature(cfeature.LAND)
ax.add_feature(cfeature.OCEAN)
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.BORDERS, linestyle=':')

# Normalize altitude data for color mapping
norm = mcolors.Normalize(vmin=df['geoaltitude'].min(), vmax=df['geoaltitude'].max())
cmap = plt.get_cmap('viridis')

# Plot each flight as a separate line based on 'callsign'
for callsign, flight_data in df.groupby('icao24'):
    # Plot each flight's path with color based on 'geoaltitude'
    points = ax.scatter(
        flight_data['lon'], flight_data['lat'],
        c=flight_data['geoaltitude'], cmap=cmap, norm=norm,
        transform=ccrs.PlateCarree(), label=callsign, s=5
    )
    # Draw line between points to show flight path
    ax.plot(
        flight_data['lon'], flight_data['lat'],
        transform=ccrs.PlateCarree(), color='gray', alpha=0.5
    )

# Add a color bar for altitude
cbar = fig.colorbar(points, ax=ax, orientation='vertical', label='Altitude (m)')
cbar.set_label('geoaltitude (m)')

# Show plot
plt.title("Flight Paths with Altitude Visualization")
plt.show() 