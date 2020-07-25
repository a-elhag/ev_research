import matplotlib.pyplot as plt
import numpy as np
from scipy.io import loadmat

## Part1: Loading EV Data
data_ev = loadmat('1DataEV.mat')

"""
for key, value in data_ev.items():
    if type(value).__module__ == np.__name__:
        print(key, value.shape)

Logic710_hr (1, 366)
Logic36_hr (1, 366)
Logic89_hr (1, 366)
Logic1_hr (1, 366)
Logic11_hr (1, 366)
Logic801_hr (1, 366)

!Indexing for Dummies!
data_ev['LogicXXX_hr'][0, day][driver, hour]
"""

## Part2: Arrival Locations + Duration
# We need to find when our drivers arrive and for how long they stay
array_ev = np.empty(366, object)

for _ in range(366):
    list_ev = []
    a = data_ev['Logic710_hr'][0, _]

    for row in a:
        try:
            idx_row = list(row).index(1)
            sum_row = np.sum(row)
            list_ev.append([idx_row, sum_row])
        except:
            break
    array_ev[_] = np.array(list_ev)

