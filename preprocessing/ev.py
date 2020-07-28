import numpy as np
import pdb
from scipy.io import loadmat

## Part1: Loading EV Data
data_ev = loadmat('../data/in/parking_lot.mat')

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
array_ev = np.empty((6, 366), object)

idx = -1
for key, lot in data_ev.items():
    if type(lot).__module__ == np.__name__:
        idx += 1
        for day in range(lot.shape[1]):
            list_ev = []
            lot_day = lot[0, day]

            for lot_day_row in lot_day:
                try:
                    idx_row = list(lot_day_row).index(1)
                    sum_row = np.sum(lot_day_row)
                    list_ev.append([idx_row, sum_row])
                except:
                    break
            array_ev[idx, day] = np.array(list_ev)


np.save('../data/preprocessing/ev.npy', array_ev)
"""
array_ev[parking_lot, day][driver, 0] ==> Arrival
array_ev[parking_lot, day][driver, 1] ==> Duration
"""
print('hello')
