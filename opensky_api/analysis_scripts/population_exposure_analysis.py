import pandas as pd
import numpy as np
import openap
import seaborn as sns
from traffic.core import Traffic, Flight
from traffic.data import aircraft
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import cartopy.crs as ccrs
import cartopy.feature as cfeature

from tools.populationcost import Noisepollution
from tools.statebased import detect

# pd.set_option('future.no_silent_downcasting', True)

# df = pd.read_csv("data/flights_sample_1_hour.csv")
# ac = pd.DataFrame(aircraft.data)[["icao24", "typecode"]]
# df = df.merge(ac)

# df = df.rename(
#     columns={
#         "time": "timestamp",
#         "lat": "latitude",
#         "lon": "longitude",
#         "heading": "track",
#     }
# ).drop(columns=["geoaltitude"])

# df = df.assign(
#     altitude=df.baroaltitude / openap.aero.ft,
#     vertical_rate=df.vertrate / openap.aero.ft * 60,
#     groundspeed=df.velocity / openap.aero.kts,
# )

# df[["onground", "alert", "spi"]] = df[["onground", "alert", "spi"]].astype(bool)
# df[["timestamp", "hour"]] = df[["timestamp", "hour"]].astype("datetime64[ns, UTC]")
# df[["callsign", "squawk"]] = df[["callsign", "squawk"]].astype(object)

# t = (Traffic(df)
#         # smooth vertical glitches
#         .filter('aggressive')
#         # resample at 1s
#         .resample('10s')
#         .eval(1)
# )

# s = t.summary(['icao24']).eval()
# noise = Noisepollution()

# f2m = 0.3048

# t = t.assign(population_exposure = lambda df: df.apply(
#     lambda row: noise.get_noise(row['latitude'], row['longitude'], row['altitude']*f2m),
#         axis=1
#     )
# )

# total_noise = t.data.groupby('icao24')['population_exposure'].sum().reset_index()
# s = pd.merge(s, total_noise, on='icao24', how='left')
# s.rename(columns={'population_exposure': 'total_noise'}, inplace=True)

# # import code
# # code.interact(local=locals())

# fig, ax = plt.subplots(figsize=(6, 5), subplot_kw={'projection': ccrs.PlateCarree()})
# ax.set_extent([1, 9, 48, 55], crs=ccrs.PlateCarree())
# ax.add_feature(cfeature.LAND)
# ax.add_feature(cfeature.OCEAN)
# ax.add_feature(cfeature.COASTLINE)
# ax.add_feature(cfeature.BORDERS, linestyle=':')

# # Normalize noise data for color mapping
# norm = mcolors.LogNorm(vmin=t.data.population_exposure.min()+0.001, vmax=t.data.population_exposure.max())
# cmap = plt.get_cmap('viridis')
# cmap.set_bad('k')

# points = ax.scatter(
#         t.data.longitude, t.data.latitude,
#         c=t.data.population_exposure, cmap=cmap, norm=norm,
#         transform=ccrs.PlateCarree(), s=2
#     )

# cbar = fig.colorbar(points, ax=ax, orientation='vertical', label='Population Exposure (-)')
# plt.show()

def overlay_population_data(traffic, summary = None):
    noise = Noisepollution()
    if summary == None:
        summary = traffic.summary(['icao24','callsign']).eval()
    f2m = 0.3048

    traffic = traffic.assign(population_exposure = lambda df: df.apply(
        lambda row: noise.get_noise(row['latitude'], row['longitude'], row['altitude']*f2m),
            axis=1
        )
    )
    
    population_exposure = traffic.data.groupby(['icao24','callsign'])['population_exposure'].sum().reset_index()
    import code
    code.interact(local=locals())
    summary = pd.merge(summary, population_exposure, on=['icao24','callsign'], how='left')
    summary.rename(columns={'population_exposure': 'total_exposure'}, inplace=True)

    return traffic, summary
        
        