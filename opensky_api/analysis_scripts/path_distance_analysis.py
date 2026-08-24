import pandas as pd

pd.set_option('future.no_silent_downcasting', True)

def overlay_pathlength_data(traffic, summary = None):
    if summary is None:
        summary = traffic.summary(['icao24','callsign']).eval()

    traffic = traffic.cumulative_distance().eval()

    nm = 1852

    traffic = traffic.assign(cumdist_m = lambda df: df.apply(
        lambda row: row['cumdist']*nm,
            axis=1
        )
    )

    total_distance = traffic.data.groupby(['icao24','callsign'])['cumdist_m'].max().reset_index()
    summary = pd.merge(summary, total_distance, on=['icao24','callsign'], how='left')

    return traffic, summary