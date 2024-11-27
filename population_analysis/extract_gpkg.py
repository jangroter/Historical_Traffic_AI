import geopandas as gpd
import numpy as np
from shapely.geometry import box

bounding_box = 1000 #km
array_size = int((bounding_box)-1)

schiphol_bbox_epsg = box(4557739,3884228,3337224,2740642) # Bounding box for loading only part of the data, in EPSG:3035
schiphol = np.array([3964000,3257000]) #Approximate center of Schiphol in EPSG:3035-1149 ETRS89-extended

# Initialize a variable to track whether the CSV exists
csv_initialized = False

data = gpd.read_file('data/grid_1km_point.gpkg', bbox = schiphol_bbox_epsg)
data['x_schiphol'] = data['geometry'].x - schiphol[0]
data['y_schiphol'] = data['geometry'].y - schiphol[1]

sel_data = data[(abs(data['x_schiphol']) < bounding_box*1000/2) & (abs(data['y_schiphol']) < bounding_box*1000/2 )]
sel_data[['x_correct','y_correct']] = sel_data[['x_schiphol','y_schiphol']] / 1000
sel_data['y_correct'] = sel_data['y_correct'] * -1
sel_data[['x_correct','y_correct']] = sel_data[['x_correct','y_correct']] + int(array_size/2)

pop_array = np.zeros((array_size,array_size))
x_array = np.zeros((array_size,array_size))
y_array = np.zeros((array_size,array_size))

for i in sel_data.index: 
    pop_array[int(sel_data['y_correct'][i]),int(sel_data['x_correct'][i])]= sel_data['TOT_P_2021'].loc[i]

for i in range(array_size):
    x_array[:,i] = (-int(array_size/2)+i) * 1000 # meters distance for cell from schiphol
    y_array[i,:] = (int(array_size/2)-i) * 1000
    
np.savetxt('population_1km.csv', pop_array)
np.savetxt('x_array.csv', x_array)
np.savetxt('y_array.csv', y_array)
