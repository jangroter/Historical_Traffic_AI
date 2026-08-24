import pandas as pd
from tools.populationcost import Noisepollution

def overlay_population_data(traffic, summary = None):
    noise = Noisepollution()
    if summary is None:
        summary = traffic.summary(['icao24','callsign']).eval()
    f2m = 0.3048

    traffic = traffic.assign(population_exposure = lambda df: df.apply(
        lambda row: noise.get_noise(row['latitude'], row['longitude'], row['altitude']*f2m),
            axis=1
        )
    )
    
    population_exposure = traffic.data.groupby(['icao24','callsign'])['population_exposure'].sum().reset_index()
    summary = pd.merge(summary, population_exposure, on=['icao24','callsign'], how='left')
    summary.rename(columns={'population_exposure': 'total_exposure'}, inplace=True)

    return traffic, summary
        
        