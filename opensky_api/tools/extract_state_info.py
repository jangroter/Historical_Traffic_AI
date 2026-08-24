import pandas as pd

def extract_state_info(traffic, summary = None):
    if summary is None:
        summary = traffic.summary(['icao24','callsign']).eval()
    
    grouped = traffic.data.groupby(['icao24', 'callsign'])

    # For each group, extract the first and last rows
    states = grouped.agg(
        timestamp_init=('timestamp', 'first'),
        latitude_init=('latitude', 'first'),
        longitude_init=('longitude', 'first'),
        altitude_init=('altitude', 'first'),

        timestamp_term=('timestamp', 'last'),
        latitude_term=('latitude', 'last'),
        longitude_term=('longitude', 'last'),
        track_term = ('track', 'last'),
        altitude_term=('altitude', 'last')
    ).reset_index()

    summary = pd.merge(summary, states, on=['icao24','callsign'], how='left')

    return summary