import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import cartopy.crs as ccrs
import cartopy.feature as cfeature

df = pd.read_csv('data/conflicts_sample_24_hours.csv')

df.loc[df.tcpa>600, "tcpa"]=600
df.loc[df.tcpa<0, "tcpa"]=0

fig, ax = plt.subplots(figsize=(6, 5), subplot_kw={'projection': ccrs.PlateCarree()})
ax.set_extent([1, 9, 48, 55], crs=ccrs.PlateCarree())
ax.add_feature(cfeature.LAND)
ax.add_feature(cfeature.OCEAN)
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.BORDERS, linestyle=':')

# Normalize altitude data for color mapping
norm = mcolors.Normalize(vmin=df.tcpa.min(), vmax=df.tcpa.max())
cmap = plt.get_cmap('viridis')

points = ax.scatter(
        df.lon, df.lat,
        c=df.tcpa, cmap=cmap, norm=norm,
        transform=ccrs.PlateCarree(), s=3
    )

cbar = fig.colorbar(points, ax=ax, orientation='vertical', label='Tcpa (s)')
plt.show()