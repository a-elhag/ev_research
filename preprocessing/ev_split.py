import datetime as dt
import ipdb
import numpy as np
dbg1 = ipdb.set_trace  # BREAKPOINT

ev_clean = np.load('../data/preprocessing/ev_clean.npy',
                         allow_pickle=True)
"""
ev_clean_split[lot, wday][0, hour]
lot ==> 0:4
wday ==> 0 if Weekday and 1 if Weekend
hour ==> 0:24
"""



ev_arr = np.empty((4, 366), object)
ev_dur = np.empty((4, 366), object)

for lot in range(4):
    for day in range(366):
        ev_arr[lot, day] = np.zeros((1,24))
        ev_dur[lot, day] = np.empty((1,24), object)
        for hour in range(24):
            ev_dur[lot, day][0, hour] = np.array([], dtype=int)


for lot in range(4):
    for day in range(366):
        rows = ev_clean[lot, day].shape[0]
        if rows == 0:
            continue
        for row in range(rows):
            arr_time = ev_clean[lot, day][row, 0] # Get the first column out
            arr_time = arr_time.astype(int)
            ev_arr[lot, day][0, arr_time] += 1

            duration = ev_clean[lot, day][row, 1] # Second column out
            ev_dur[lot, day][0, arr_time] = np.append(
                ev_dur[lot, day][0, arr_time], duration)

# Dates
Jan1 = dt.date(2012, 1, 1)
Jan1.weekday() # Return day of the week, where Monday == 0 ... Sunday == 6
wday = range(0, 5)

ev_split = np.empty((4,2), object)
for lot in range(4):
    ev_split[lot, 0] = np.empty((2,24), object) # Weekday
    ev_split[lot, 1] = np.empty((2,24), object) # Weekend
    for hour in range(24):
        for _ in range(2): # 0 == arr || 1 == dur
            ev_split[lot, 0][_, hour] = np.array([])
            ev_split[lot, 1][_, hour] = np.array([])

for lot in range(4):
    for day in range(366):
        day_idx = Jan1 + dt.timedelta(days=day)

        # Might be useless, think of removing in future
        if ev_clean[lot, day].ndim == 0:
            continue

        for hour in range(24):
            array_arr = ev_arr[lot, day][0, hour]
            array_dur = ev_dur[lot, day][0, hour]

            if day_idx.weekday() in wday:
                ev_split[lot, 0][0, hour] = np.hstack(
                    (ev_split[lot, 0][0, hour], array_arr))
                ev_split[lot, 0][1, hour] = np.hstack(
                    (ev_split[lot, 0][1, hour], array_dur))
            else:
                ev_split[lot, 1][0, hour] = np.hstack(
                    (ev_split[lot, 1][0, hour], array_arr))
                ev_split[lot, 1][1, hour] = np.hstack(
                    (ev_split[lot, 1][1, hour], array_dur))

np.save('../data/preprocessing/ev_split.npy', ev_split)