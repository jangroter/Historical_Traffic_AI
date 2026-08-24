from pyopensky.trino import Trino
from datetime import datetime, timedelta
import pandas as pd
import math

from get_data.download_data import download_data
from get_data.filter_data import filter_data
from tools.populationcost import kwikqdrdist


def distance_to_schiphol(row):
    qdr, dist = kwikqdrdist(52.3068953, 4.760783, row['latitude'], row['longitude'])
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
    return cas


def generate_bluesky_scn(df, global_start_time):
    df['time'] = pd.to_datetime(df['timestamp'], utc=True)
    global_start_time = pd.to_datetime(global_start_time, utc=True)
    df = df.sort_values('time')
    cre_lines = []

    for _, row in df.iterrows():
        delta = row['time'] - global_start_time
        total_seconds = delta.total_seconds()
        hh = int(total_seconds // 3600)
        mm = int((total_seconds % 3600) // 60)
        ss = int(total_seconds % 60)
        ms = int((delta.microseconds + (delta.seconds % 1) * 1e6) / 10000)
        time_str = f"{hh:02d}:{mm:02d}:{ss:02d}.{ms:02d}"

        fl = f"FL{int(round(row['altitude'] / 100))}"
        
        cas = gs_to_cas(row['groundspeed'], row['altitude'])

        if not math.isnan(cas):
            cas = round(cas)
            line = (
                f"{time_str}>CRE {row['icao24']}, A320 ,{row['latitude']:.4f},{row['longitude']:.4f},"
                f"{int(row['track'])},{fl},{cas}"
            )
            cre_lines.append(line)

    return cre_lines


def process_interval(start, stop, distance_from_eham=300, file_out="schiphol_arrivals.scn", global_start_time = None, time_interval = 1):
    trino = Trino()
    scenario_lines = []

    # ensure output file is empty before appending
    open(file_out, "w").close()
    
    start_dt = pd.to_datetime(start, utc=True)
    stop_dt = pd.to_datetime(stop, utc=True)

    if global_start_time == None:
        global_start_time = start_dt
    else:
        global_start_time = global_start_time

    current = start_dt
    while current < stop_dt:
        next_day = min(current + timedelta(days=time_interval), stop_dt)

        print(f"Processing {current} to {next_day}")


        history = download_data(current.strftime("%Y-%m-%d %H:%M:%S"),
                                next_day.strftime("%Y-%m-%d %H:%M:%S"),
                                save=False)
        
        if len(history)>0:
            traffic = filter_data(history)

            traf_data = traffic.data
            traf_data['distance_schiphol'] = traf_data.apply(distance_to_schiphol, axis=1)
            traf_data = traf_data[
                (traf_data['distance_schiphol'] <= distance_from_eham) &
                (traf_data['distance_schiphol'] >= distance_from_eham * 0.9)
            ]
            traf_data = traf_data.sort_values(by=['icao24', 'timestamp'])
            traf_data = traf_data.drop_duplicates(subset='icao24', keep='first')

            scenario = generate_bluesky_scn(traf_data, global_start_time)

            # append batch to file
            with open(file_out, "a") as f:
                f.writelines(line + "\n" for line in scenario)

        current = next_day

    print(f"Scenario file written to {file_out}")


# Example usage
if __name__ == "__main__":
    process_interval(
        start="2024-03-01 00:00:00",
        stop="2024-03-31 23:59:59",
        distance_from_eham=300,
        file_out="schiphol_arrivals_march_2024.scn",
        global_start_time="2024-03-01 00:00:00",
        time_interval = 0.5
    )