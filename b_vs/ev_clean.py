import numpy as np

array_ev = np.load('../a_data/b_vs/out/ev.npy', allow_pickle=True)

# Remove the first day
array_ev = array_ev[:, 1:]


rem_count=0
total_count=0
for year in range(array_ev.shape[0]):
    for day in range(array_ev.shape[1]):
        print(year, day)
        if array_ev[year, day].ndim == 1:
            continue

        if year==0 and day==array_ev[year, day].shape[1]-10:
            print(array_ev[year, day])

        shape1 = array_ev[year, day].shape[0]
        remove_hours = [0, 1, 2, 3, 4, 22, 23, 24]
        for remove in remove_hours:
            array_ev[year, day] = array_ev[year, day][array_ev[year, day][:,0] != remove]
        if year==0 and day==array_ev[year, day].shape[1]-10:
            print(array_ev[year, day])
        shape2 = array_ev[year, day].shape[0]
        total_count += shape2

        rem_count += shape1-shape2

np.save('../a_data/b_vs/out/ev_clean.npy', array_ev)

# print(rem_count)
# print(total_count)
# print(rem_count/total_count) # ~ 20.6% 
