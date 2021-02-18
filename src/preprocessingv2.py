## Part 0: Intializing
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

## Part 1: Data In
base = 'data/in/toronto/'
ext = '.csv'
years = np.arange(1999, 2019+1)

loc = base + '1998' + ext

cols = ['Year', 'Month', 'Day', 'Hour', 'Minute',
        'GHI', 'Wind Speed', 'Temperature']
data = pd.read_csv(loc, skiprows=2, low_memory=False, usecols = cols)

for year in years:
    loc = base + str(year) + ext
    data_temp = pd.read_csv(loc, skiprows=2, low_memory=False, usecols = cols)
    data = pd.concat([data, data_temp])

## Part 2: Data Out
data[['GHI', 'Temperature', 'Wind Speed']].describe()
