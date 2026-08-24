from get_data.download_data import download_data
from get_data.filter_data import filter_data
from analysis_scripts.population_exposure_analysis import overlay_population_data
from analysis_scripts.path_distance_analysis import overlay_pathlength_data
from analysis_scripts.conflict_detection import get_conflict_data, update_conflict_summary
from tools.extract_state_info import extract_state_info
from tools.estimate_runway import estimate_runway

from traffic.core import Traffic

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import cartopy.crs as ccrs
import cartopy.feature as cfeature

import seaborn as sns
import pandas as pd

start = '2023-11-06 06:00:00'
stop = '2023-11-06 23:00:00'
download = False
file_name = 'data/2023-11-06 06:00:00_2023-11-06 23:00:00_EHAM.csv'
file_name = 'data/test_output.csv'

runway_loss_cut_off = 250000
exclude_runways = []#['22','04']

if download:
    history = download_data(start, stop)
    traffic = filter_data(history)
else:
    traffic = filter_data(file_name=file_name)

summary = extract_state_info(traffic)
summary = estimate_runway(traffic, summary)
traffic_data = pd.merge(traffic.data,summary, on=['icao24','callsign'], how='inner')
traffic = Traffic(traffic_data[(traffic_data['runway_loss']<runway_loss_cut_off) & (~traffic_data['runway'].isin(exclude_runways))])
summary = summary[(summary['runway_loss']<runway_loss_cut_off) & (~summary['runway'].isin(exclude_runways))]


traffic, summary = overlay_population_data(traffic, summary)
traffic, summary = overlay_pathlength_data(traffic, summary)
traffic, summary, conf_df = get_conflict_data(traffic, summary)

# Get initial state into summary (lat, lon, t_start)
# Get terminal state into summary (rwy / faf, t_end)
import code
code.interact(local=locals())
def func(flight):
    return(flight.aligned_on_ils("EHAM").all())
t_ils = traffic.pipe(func).eval()
result = t_ils.data.loc[t_ils.data['runway'] != t_ils.data['ILS'], 'icao24']

import code
code.interact(local=locals())