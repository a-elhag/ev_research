import numpy as np

array_ev = np.load('../a_data/b_vs/out/ev.npy', allow_pickle=True)

# Remove the first day
array_ev = array_ev[:, 1:]

# # Remove all zeros
# for year in range(6):
#     for day in range(1):
#         if year>0:
#             break
#         print(array_ev[year, day])

rem_count=0
total_count=0
for year in range(array_ev.shape[0]):
    for day in range(array_ev.shape[1]):
        if array_ev[year, day].ndim == 1:
            break

        shape1 = array_ev[year, day].shape[0]
        remove_hours = [0, 1, 2, 3, 4, 22, 23, 24]
        for remove in remove_hours:
            array_ev[year, day] = array_ev[year, day][array_ev[year, day][:,0] != remove]
        shape2 = array_ev[year, day].shape[0]
        total_count += shape2

        rem_count += shape1-shape2

# print(rem_count)
# print(total_count)
# print(rem_count/total_count)
