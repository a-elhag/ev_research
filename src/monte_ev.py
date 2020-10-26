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

## Starting
ev_split = np.load('data/preprocessing/ev_split.npy', allow_pickle=True)

rand = np.empty((4,2), object)
ev_arr = np.empty((4,2), object)
ev_dur = np.empty((4,2), object)
for lot in range(4):
    for day in range(2):
        rand[lot, day] = np.empty((1, 24), object)
        ev_arr[lot, day] = np.empty((1, 24), object)
        ev_dur[lot, day] = np.empty((1, 24), object)


week = 3
# Generate the number of drivers
for lot in range(4):
    for day in range(2):
        for hour in range(24):
            if day == 0:
                rand[lot, day][0, hour] = np.random.rand(week*5)
            else:
                rand[lot, day][0, hour] = np.random.rand(week*2)

            ev_arr[lot, day][0, hour] = \
                    np.quantile(ev_split[lot, day][0, hour], rand[lot, day][0, hour])
            ev_arr[lot, day][0, hour] = np.round(ev_arr[lot, day][0, hour])


for lot in range(4):
    for day in range(2):
        for hour in range(24):
            print(ev_arr[lot, day][0, hour])
#             ev_dur[lot, day][0, hour] = \
#                     np.quantile(ev_split[lot, day][1, hour], rand[lot, day][0, hour])
