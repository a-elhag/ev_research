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
ev_split = np.load('data/preprocessing/ev_split.npy', allow_pickle=True)
ev_split[1,0][0, 13] # Arrivals
rand = np.random.rand(100)
A = np.quantile(ev_split[1, 0][0, 13], rand)
A = np.round(A)
## 
# Weekday
rand = np.empty((4,2), object)
ev_arr = np.empty((4,2), object)
for lot in range(4):
    for day in range(2):
        rand[lot, day] = np.empty((1, 24), object)
        ev_arr[lot, day] = np.empty((1, 24), object)


week = 3
for lot in range(4):
    for day in range(2):
        for hour in range(24):
            if day == 0:
                rand[lot, day][0, hour] = np.random.rand(week*5)
            else:
                rand[lot, day][0, hour] = np.random.rand(week*2)

            ev_arr[lot, day][0, hour] = np.quantile(ev_split[lot, day][0, hour], rand[lot, day][0, hour])
            ev_arr[lot, day][0, hour] = np.round(ev_arr[lot, day][0, hour])
