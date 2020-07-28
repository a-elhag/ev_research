import matplotlib.pyplot as plt
import numpy as np
from scipy.io import loadmat

"""
Using Approximated WT characteristics
Wind Edges:
Cut_In Speed  = 4m/s
Rated Speed   = 16m/s
Cut_Out Speed = 25m/s

data:
dict_keys(['__header__', '__version__', '__globals__',
'tempX', 'PVdata', 'RTS', 'Wind'])

Edges_WT = [0 4:1.5:16 25 100]
PowEdg_WT = discretize(Wind_Yr,Edges_WT)
"""

## Part1: Inputting Wind Data
data = loadmat('../data/in/solar_wind.mat')
wind = data['Wind']
wind = wind.reshape((10, 8760))

## Part2: Edging
edges_wt = np.r_[0, 4:16.5:1.5, 25, 100] # shape(12,)

"""
00 0.0  ==>  00 - 01 0.0
01 4.0  ==>  01 - 02 (4.0+5.5)/2
02 5.5  ==>  02 - 03 (5.5+7.0)/2
03 7.0  ==>  03 - 04 (7.0+8.5)/2
04 8.5  ==>  04 - 05 (8.5+10.0)/2
05 10.0 ==>  05 - 06 (10.0+11.5)/2
06 11.5 ==>  06 - 07 (11.5+13.0)/2
07 13.0 ==>  07 - 08 (13.0+14.5)/2
08 14.5 ==>  08 - 09 (14.5+16.0)/2
09 16.0 ==>  09 - 10 16.0 # Rated Speed
10 25.0 ==>  10 - 11 0.0 # Cut_Out Speed
11 0.0
----

Added :
pow_edges_wt = np.r_[0, pow_edges_wt]

First is useless
"""
pow_edges_wt = np.copy(edges_wt)
pow_edges_wt = pow_edges_wt[:-1] # Power Edges to simulate WT
pow_edges_wt[-1] = 0
for _ in range(1,pow_edges_wt.shape[0]-2):
    pow_edges_wt[_] += pow_edges_wt[_+1]
    pow_edges_wt[_] /= 2

pow_edges_wt = np.r_[0, pow_edges_wt]

## Part3: Applying Edges
Pwt = np.digitize(wind, edges_wt) # Power Wind Turbine
Pwt = pow_edges_wt[Pwt]

Pwt = Pwt/Pwt[:,:].max()
np.save('../data/preprocessing/wt.npy', Pwt)

"""
## Part4: Plotting
plt.subplot(311)
plt.plot(wind[0,:], label = 'Orig Y1')
plt.plot(Pwt[0,:], label = 'New Y1')
plt.legend()

plt.subplot(312)
plt.plot(wind[1,:], label = 'Orig Y2')
plt.plot(Pwt[0,:], label = 'New Y2')
plt.legend()

plt.subplot(313)
plt.plot(wind[2,:], label = 'Orig Y3')
plt.plot(Pwt[0,:], label = 'New Y3')
plt.legend()

plt.show()
"""

