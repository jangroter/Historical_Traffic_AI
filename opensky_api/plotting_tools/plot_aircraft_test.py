import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import cartopy.crs as ccrs
import cartopy.feature as cfeature

from datetime import datetime

def plot_trajectory(traffic_data, c_feature='altitude', label='altitude(m)', colormap = 'viridis', scale=None, log_cut_off=0.001):
    fig, ax = plt.subplots(figsize=(6, 5), subplot_kw={'projection': ccrs.PlateCarree()})
    ax.set_extent([1, 9, 48, 55], crs=ccrs.PlateCarree())
    ax.add_feature(cfeature.LAND)
    ax.add_feature(cfeature.OCEAN)
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS, linestyle=':')

    # Normalize noise data for color mapping
    if scale is None:
        norm = mcolors.Normalize(vmin=traffic_data[c_feature].min(), vmax=traffic_data[c_feature].max())
    elif scale == 'log':
        norm = mcolors.LogNorm(vmin=traffic_data[c_feature].min()+log_cut_off, vmax=traffic_data[c_feature].max())
    else:
        print(f'not implemented {scale}, doing standard Normalize')
        norm = mcolors.Normalize(vmin=traffic_data[c_feature].min(), vmax=traffic_data[c_feature].max())
    
    cmap = plt.get_cmap(colormap)
    cmap.set_bad('k')

    points = ax.scatter(
            traffic_data.longitude, traffic_data.latitude,
            c=traffic_data[c_feature], cmap=cmap, norm=norm,
            transform=ccrs.PlateCarree(), s=2
        )

    cbar = fig.colorbar(points, ax=ax, orientation='vertical', label=label)
    plt.show()


# df = pd.read_csv('data/flights_sample_1_hour.csv')
# df = df.sort_values('time')
# # df[df['geoaltitude']>12000] = 12000

# # Set up the map with Cartopy
# fig, ax = plt.subplots(figsize=(6, 5), subplot_kw={'projection': ccrs.PlateCarree()})
# ax.set_extent([1, 9, 48, 55], crs=ccrs.PlateCarree())
# ax.add_feature(cfeature.LAND)
# ax.add_feature(cfeature.OCEAN)
# ax.add_feature(cfeature.COASTLINE)
# ax.add_feature(cfeature.BORDERS, linestyle=':')

# # Normalize altitude data for color mapping
# norm = mcolors.Normalize(vmin=df['geoaltitude'].min(), vmax=df['geoaltitude'].max())
# cmap = plt.get_cmap('viridis')

# # Plot each flight as a separate line based on 'callsign'
# for callsign, flight_data in df.groupby('icao24'):
#     # Plot each flight's path with color based on 'geoaltitude'
#     points = ax.scatter(
#         flight_data['lon'], flight_data['lat'],
#         c=flight_data['geoaltitude'], cmap=cmap, norm=norm,
#         transform=ccrs.PlateCarree(), label=callsign, s=5
#     )
#     # Draw line between points to show flight path
#     ax.plot(
#         flight_data['lon'], flight_data['lat'],
#         transform=ccrs.PlateCarree(), color='gray', alpha=0.5
#     )

# # Add a color bar for altitude
# cbar = fig.colorbar(points, ax=ax, orientation='vertical', label='Altitude (m)')
# cbar.set_label('geoaltitude (m)')

# # Show plot
# plt.title("Flight Paths with Altitude Visualization")
# plt.show() 

# fig, ax = plt.subplots(figsize=(6, 5), subplot_kw={'projection': ccrs.PlateCarree()})
# ax.set_extent([1, 9, 48, 55], crs=ccrs.PlateCarree())
# ax.add_feature(cfeature.LAND)
# ax.add_feature(cfeature.OCEAN)
# ax.add_feature(cfeature.COASTLINE)
# ax.add_feature(cfeature.BORDERS, linestyle=':')

# # Normalize noise data for color mapping
# norm = mcolors.LogNorm(vmin=traffic.data.altitude.min()+0.001, vmax=traffic.data.altitude.max())
# cmap = plt.get_cmap('viridis')
# cmap.set_bad('k')

# points = ax.scatter(
#         traffic.data.longitude, traffic.data.latitude,
#         c=traffic.data.altitude, cmap=cmap, norm=norm,
#         transform=ccrs.PlateCarree(), s=2
#     )

# cbar = fig.colorbar(points, ax=ax, orientation='vertical', label='Population Exposure (-)')
# plt.show()
