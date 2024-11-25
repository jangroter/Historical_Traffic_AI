import pandas as pd
import numpy as np
import openap
import seaborn as sns
from traffic.core import Traffic, Flight
from traffic.data import aircraft
import matplotlib.pyplot as plt

from tools.statebased import detect

pd.set_option('future.no_silent_downcasting', True)

class BlueSky_Traffic:
    def __init__(self, index, lat, lon, gs, alt, vs, trk):
        self.id = index
        self.ntraf = len(lat)
        self.lat = lat
        self.lon = lon
        self.gs = gs
        self.alt = alt
        self.vs = vs
        self.trk = trk


df = pd.read_csv("data/flights_sample_24_hours.csv")
ac = pd.DataFrame(aircraft.data)[["icao24", "typecode"]]
df = df.merge(ac)

df = df.rename(
    columns={
        "time": "timestamp",
        "lat": "latitude",
        "lon": "longitude",
        "heading": "track",
    }
).drop(columns=["geoaltitude"])

df = df.assign(
    altitude=df.baroaltitude / openap.aero.ft,
    vertical_rate=df.vertrate / openap.aero.ft * 60,
    groundspeed=df.velocity / openap.aero.kts,
)

df[["onground", "alert", "spi"]] = df[["onground", "alert", "spi"]].astype(bool)
df[["timestamp", "hour"]] = df[["timestamp", "hour"]].astype("datetime64[ns, UTC]")
df[["callsign", "squawk"]] = df[["callsign", "squawk"]].astype(object)

t = (Traffic(df)
        # smooth vertical glitches
        .filter('aggressive')
        # resample at 1s
        .resample('10s')
        .eval(1)
)

# t = t["484165","484162","484163","484164",'484c54','484c24','484c50','484558', '484f6d']
df = t.data
df = df.sort_values('timestamp')

id_list = []

lat_array = np.array([])
lon_array = np.array([])
gs_array = np.array([])
alt_array = np.array([])
vs_array = np.array([])
trk_array = np.array([])

dcpa_array = np.array([])
tcpa_array = np.array([])
dist_array = np.array([])
dalt_array = np.array([])

for t in df['timestamp'].unique():
    print(t)
    df_t = df[df['timestamp']==t]
    # df_t = df_t[df_t['baroaltitude']>3000]
    
    index = df_t['icao24'].to_list()
    lat = df_t['latitude'].to_numpy()
    lon = df_t['longitude'].to_numpy()
    gs = df_t['velocity'].to_numpy()
    alt = df_t['baroaltitude'].to_numpy()
    vs = df_t['vertrate'].to_numpy()
    trk = df_t['track'].to_numpy()

    if len(index) == 0:
        continue

    ac = BlueSky_Traffic(index,lat,lon,gs,alt,vs,trk)

    dcpa, dist, dalt, swconfl, tcpa = detect(ac, ac, 5000, 300, 1000)

    id_list.append([ac.id[i] for i, j in zip(*np.where(swconfl))])
    
    lat_array = np.append(lat_array, np.array([ac.lat[i] for i, j in zip(*np.where(swconfl))]))
    lon_array = np.append(lon_array, np.array([ac.lon[i] for i, j in zip(*np.where(swconfl))]))
    gs_array = np.append(gs_array, np.array([ac.gs[i] for i, j in zip(*np.where(swconfl))]))
    alt_array = np.append(alt_array, np.array([ac.alt[i] for i, j in zip(*np.where(swconfl))]))
    vs_array = np.append(vs_array, np.array([ac.vs[i] for i, j in zip(*np.where(swconfl))]))
    trk_array = np.append(trk_array, np.array([ac.trk[i] for i, j in zip(*np.where(swconfl))]))
        
    dcpa_array = np.append(dcpa_array, dcpa[swconfl])
    tcpa_array = np.append(tcpa_array, tcpa[swconfl])
    dist_array = np.append(dist_array, dist[swconfl])
    dalt_array = np.append(dalt_array, dalt[swconfl])

id_list = [item for sublist in id_list for item in sublist]

conf_df = pd.DataFrame({
    'id': id_list,
    'lat': lat_array,
    'lon': lon_array,
    'gs': gs_array,
    'alt': alt_array,
    'vs': vs_array,
    'trk': trk_array,
    'dcpa':dcpa_array,
    'tcpa':tcpa_array,
    'dist':dist_array,
    'dalt':dalt_array
})

conf_df.to_csv('data/conflicts_sample_24_hours.csv')