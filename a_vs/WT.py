import matplotlib.pyplot as plt
import numpy as np
from scipy.io import loadmat

"""
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

data = loadmat('1DataOrig.mat')
Wind = data['Wind']

edges_wt = np.r_[0, 4:17:1.5, 25, 100] # shape(12,)
"""

00 0.0  =>  00 0.0
01 4.0  =>  01 (4.0+5.5)/2
02 5.5  =>  02 (5.5+7.0)/2
03 7.0  =>  03 (7.0+8.5)/2
04 8.5  =>  04 (8.5+10.0)/2
05 10.0 =>  05 (10.0+11.5)/2
06 11.5 =>  06 (11.5+13.0)/2
07 13.0 =>  07 (13.0+14.5)/2
08 14.5 =>  08 (14.5+16.0)/2
09 16.0 =>  09 16.0
10 25.0 =>  10 25.0
11 0.0  =>  11 0.0
"""
pow_edges_wt = edges_wt # Power Edges to simulate WT

pow_edges_wt[-1] = 0
pow_edges_wt[-2] = 16
for count, _ in enumerate(range(1,edges_wt.shape[0]-2)):
    print(count+1, pow_edges_wt[_])
