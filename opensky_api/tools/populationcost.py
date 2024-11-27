"""
Determine population exposed to noise, for now just assume pop/d^2 following the inverse square law of noise dissipation.
Later versions can also include a scaling factor for actual engine / airframe noise.
"""

import numpy as np

noisepollution = None

def kwikqdrdist(lata, lona, latb, lonb):
    """Gives quick and dirty qdr[deg] and dist [m]
       from lat/lon. (note: does not work well close to poles)"""

    re      = 6371000.  # radius earth [m]
    dlat    = np.radians(latb - lata)
    dlon    = np.radians(((lonb - lona)+180)%360-180)
    cavelat = np.cos(np.radians(lata + latb) * 0.5)

    dangle  = np.sqrt(dlat * dlat + dlon * dlon * cavelat * cavelat)
    dist    = re * dangle

    qdr     = np.degrees(np.arctan2(dlon * cavelat, dlat)) % 360.

    return qdr, dist

class Noisepollution():
    def __init__(self, 
                 population_file = 'data/population_1km.csv', 
                 x_file = 'data/x_array.csv',
                 y_file = 'data/y_array.csv',
                 ref_airport = [52.3068953,4.760783],
                 window_size = 20,
                 cell_size = 1000):
       
        self.pop_array = np.genfromtxt(population_file, delimiter = ' ')
        self.x_array = np.genfromtxt(x_file, delimiter = ' ')
        self.y_array = np.genfromtxt(y_file, delimiter = ' ')
        self.x_max = np.max(self.x_array)
        self.y_max = np.max(self.y_array)
        self.window_size = window_size
        self.cell_size = cell_size

        self.airport = ref_airport # lat,lon coords of airport for reference to x_array and y_array

    def get_noise(self, lat, lon, alt):
        brg, dist = kwikqdrdist(self.airport[0], self.airport[1], lat, lon)

        x = np.sin(np.radians(brg))*dist
        y = np.cos(np.radians(brg))*dist
        z = alt

        x_index_min = int(((x+self.x_max)/self.cell_size)-self.window_size)
        x_index_max = int(((x+self.x_max)/self.cell_size)+self.window_size)
        y_index_min = int(((self.y_max - y)/self.cell_size)-self.window_size)
        y_index_max = int(((self.y_max - y)/self.cell_size)+self.window_size)

        distance2 = (self.x_array[y_index_min:y_index_max,x_index_min:x_index_max]-x)**2 + (self.y_array[y_index_min:y_index_max,x_index_min:x_index_max]-y)**2 + z**2

        return np.sum(self.pop_array[y_index_min:y_index_max,x_index_min:x_index_max]/distance2)

