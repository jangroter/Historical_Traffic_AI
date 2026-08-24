from pyopensky.trino import Trino
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math

from get_data.download_data import download_data
from get_data.filter_data import filter_data

from tools.populationcost import kwikqdrdist

def distance_to_schiphol(row):
    qdr, dist = kwikqdrdist(52.3068953,4.760783,row['latitude'],row['longitude'])
    return dist / 1000

def altitude_to_density(altitude_ft):
    """Approximate air density (ISA) for a given altitude in feet."""
    altitude_m = altitude_ft * 0.3048
    if altitude_m > 11000:
        altitude_m = 11000  # Cap at tropopause for simplicity
    T0 = 288.15  # Sea level standard temperature (K)
    L = 0.0065   # Temperature lapse rate (K/m)
    p0 = 101325  # Sea level standard pressure (Pa)
    R = 287.058  # Gas constant for air (J/kg·K)
    g = 9.80665  # Gravity (m/s²)
    
    T = T0 - L * altitude_m
    p = p0 * (T / T0) ** (g / (R * L))
    rho = p / (R * T)
    return rho

def gs_to_cas(gs_kts, altitude_ft):
    """Convert Ground Speed (knots) to approximate CAS (knots)."""
    rho = altitude_to_density(altitude_ft)
    rho0 = 1.225  # Sea level air density
    correction_factor = math.sqrt(rho / rho0)
    cas = gs_kts * correction_factor
    return round(cas)

def generate_bluesky_scn(df):
    df['time'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values('time')
    start_time = df['time'].min()
    cre_lines = []

    for _, row in df.iterrows():
        delta = row['time'] - start_time
        total_seconds = delta.total_seconds()
        hh = int(total_seconds // 3600)
        mm = int((total_seconds % 3600) // 60)
        ss = int(total_seconds % 60)
        ms = int((delta.microseconds + (delta.seconds % 1) * 1e6) / 10000)
        time_str = f"{hh:02d}:{mm:02d}:{ss:02d}.{ms:02d}"

        fl = f"FL{int(round(row['altitude'] / 100))}"

        # GS → CAS
        cas = gs_to_cas(row['groundspeed'], row['altitude'])

        line = (
            f"{time_str}>CRE {row['icao24']}, A320 ,{row['latitude']:.4f},{row['longitude']:.4f},"
            f"{int(row['track'])},{fl},{cas}"
        )
        cre_lines.append(line)
    
    return cre_lines

# Initialize parameters
distance_from_eham = 300 #km

airport_icao = 'EHAM'
start = '2023-11-06 06:00:00'
stop = '2023-11-06 23:00:00'
trino = Trino()

download = False
file_name = 'data/SCN-sample.csv'

if download:
    history = download_data(start, stop, save=True)
    traffic = filter_data(history)
else:
    traffic = filter_data(file_name=file_name)

traf_data = traffic.data
# import code
# code.interact(local=locals())
traf_data['distance_schiphol'] = traf_data.apply(distance_to_schiphol, axis=1)
traf_data = traf_data[traf_data['distance_schiphol'] <= distance_from_eham]
traf_data = traf_data[traf_data['distance_schiphol'] >= distance_from_eham*0.9]
traf_data = traf_data.sort_values(by=['icao24', 'timestamp'])
traf_data = traf_data.drop_duplicates(subset='icao24', keep='first')

scenario = generate_bluesky_scn(traf_data)
with open("schiphol_arrivals.scn", "w") as f:
    f.writelines(line + "\n" for line in scenario)

import code
code.interact(local=locals())