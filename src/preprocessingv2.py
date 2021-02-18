## Part 0: Intializing
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

## Part 1: Data In
base = 'data/in/toronto/'
ext = '.csv'
years = np.arange(1998, 2019)

loc = base + str(years[0]) + ext

cols = ['Year', 'Month', 'Day', 'Hour', 'Minute', 'GHI',
        'Cloud Type', 'Wind Speed', 'Temperature']
data = pd.read_csv(loc, skiprows=2, low_memory=False, usecols = cols)


