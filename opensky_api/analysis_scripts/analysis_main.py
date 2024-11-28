from get_data.download_data import download_data
from get_data.filter_data import filter_data
from analysis_scripts.population_exposure_analysis import overlay_population_data
from analysis_scripts.path_distance_analysis import overlay_pathlength_data
from analysis_scripts.conflict_detection import get_conflict_data, update_conflict_summary

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import cartopy.crs as ccrs
import cartopy.feature as cfeature

start = '2023-11-06 06:00:00'
stop = '2023-11-06 23:00:00'
download = False
file_name = 'data/2023-11-06 06:00:00_2023-11-06 23:00:00_EHAM.csv'

if download:
    history = download_data(start, stop)
    traffic = filter_data(history)
else:
    traffic = filter_data(file_name=file_name)
traffic, summary = overlay_population_data(traffic)
traffic, summary = overlay_pathlength_data(traffic, summary)
traffic, summary, conf_df = get_conflict_data(traffic, summary)

import code
code.interact(local=locals())