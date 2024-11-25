import xarray as xr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the .grib file with xarray and cfgrib engine
ds = xr.open_dataset("data/ERA5_data.grib", engine="cfgrib")

u_wind = ds['u']
v_wind = ds['v']

# Calculate total wind speed at each latitude, longitude, and time
total_wind_speed = np.sqrt(u_wind**2 + v_wind**2)

# Calculate the average total wind speed over latitude and longitude for each time
avg_total_wind_speed = total_wind_speed.mean(dim=['latitude', 'longitude'])

# Convert to a pandas DataFrame with time and average total wind speed
df = avg_total_wind_speed.to_dataframe(name="avg_total_wind_speed").reset_index()

df.to_csv('data/average_wind_23_24.csv', index=False)

sns.lineplot(data = df, x = 'valid_time', y = 'avg_total_wind_speed', hue = 'isobaricInhPa')
plt.show()


# for t in ds['time']:
#     count +=1
#     if count%100 == 0:
#         print(count)
#     u_wind = ds['u'].sel(isobaricInhPa=800, time=t)
#     v_wind = ds['v'].sel(isobaricInhPa=800, time=t) 
#     absolute_wind = np.sqrt(np.square(u_wind)+np.square(v_wind))

#     if np.mean(np.array((absolute_wind))) < lowest_total_wind:
#         lowest_total_wind = np.mean(np.array((absolute_wind)))
#         lowest_time = t

#     if count == 1000:
#         break

# u_wind = ds['u'].sel(isobaricInhPa=800, time=lowest_time)
# v_wind = ds['v'].sel(isobaricInhPa=800, time=lowest_time)

# absolute_wind = np.sqrt(np.square(u_wind)+np.square(v_wind))
# print(lowest_time, np.mean(np.array((absolute_wind))))

# plt.figure(figsize=(10, 6))
# absolute_wind.plot(
#     cmap="coolwarm",  # Color map
#     cbar_kwargs={"label": "total wind (m/s)"}  # Add color bar label
# )

# # Set plot title and labels
# plt.title(f"Absolute Wind Component at 800 hPa on {lowest_time}")
# plt.xlabel("Longitude")
# plt.ylabel("Latitude")

# # Show the plot
# plt.show()