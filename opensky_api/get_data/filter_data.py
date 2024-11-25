import pandas as pd
import numpy as np
import openap
import seaborn as sns
from traffic.core import Traffic, Flight
from traffic.data import aircraft
import matplotlib.pyplot as plt

df = pd.read_csv("data/flights_sample_1_hour.csv")
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

f = t["484165","484162","484163","484164",'484c54','484c24','484c50','484558', '484f6d']
# import code
# code.interact(local=locals())
# f = t[0:15]
df = t.data
df = df.sort_values('timestamp')

feature_to_plot = 'altitude'

# sns.lineplot(data=df, x = 'timestamp', y = feature_to_plot, hue = 'icao24')
# plt.show()
