import pandas as pd
import sys
import openap
from traffic.core import Traffic, Flight
from traffic.data import aircraft
pd.set_option('future.no_silent_downcasting', True)

def filter_data(data = None, file_name = None, sample_rate = '10s'):
    if data == None:
        try:
            data = pd.read_csv(file_name)
        except FileNotFoundError:
            print('If no data is provided, an exisiting path to the data as .csv should be given')
            sys.exit(1)
    ac = pd.DataFrame(aircraft.data)[["icao24", "typecode"]]
    data = data.merge(ac)

    data = data.rename(
        columns={
            "time": "timestamp",
            "lat": "latitude",
            "lon": "longitude",
            "heading": "track",
        }
    ).drop(columns=["geoaltitude"])

    data = data.assign(
        altitude=data.baroaltitude / openap.aero.ft,
        vertical_rate=data.vertrate / openap.aero.ft * 60,
        groundspeed=data.velocity / openap.aero.kts,
    )

    data[["onground", "alert", "spi"]] = data[["onground", "alert", "spi"]].astype(bool)
    data[["timestamp", "hour"]] = data[["timestamp", "hour"]].astype("datetime64[ns, UTC]")
    data[["callsign", "squawk"]] = data[["callsign", "squawk"]].astype(object)
    
    traffic = (Traffic(data)
        # smooth vertical glitches
        .filter('aggressive')
        # resample at 10s
        .resample(sample_rate)
        .eval(1)
    )   

    traffic.data = traffic.data.reset_index()
    traffic = traffic.drop(traffic.data.index[traffic.data.altitude.isna()].tolist())
    traffic.data = traffic.data.set_index('index')
    
    return traffic