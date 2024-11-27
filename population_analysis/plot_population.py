import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.colors import LogNorm

poparray = np.genfromtxt('population_1km.csv')

c_map = plt.get_cmap('viridis')
c_map.set_bad('k')

plt.imshow(poparray,cmap=c_map, norm=LogNorm(vmin=100,vmax=100000))
plt.show()