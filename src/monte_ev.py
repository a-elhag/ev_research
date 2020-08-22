import numpy as np
import time

## Part 1
def timing(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        output = func(*args, **kwargs)
        end_time = time.time() - start_time
        print(end_time)
        return output
    return wrapper

## Part 2
# @timing
def full_icdf(data, years):
    out_array = np.zeros((years, 8760))
    for year in range(years):
        seasons = np.r_[89, 93, 93, 90]
        seasons = seasons.cumsum()

        for day in range(365):
            season = seasons[seasons > day][0]
            season = (seasons == season)
            season = np.where(season)[0][0]

            for hour in range(24):
                rand = np.random.rand()
                out = np.quantile(data[season, hour], rand)
                idx_hour = hour + day*24
                out_array[year, idx_hour] = out

    return np.array(out_array)

## Starting
""" 
data_ev[0] ==> arrival
data_ev[1] ==> duration
"""
data_ev = np.load('data/preprocessing/ev.npy', allow_pickle=True)

## 
