import datetime as dt
import matplotlib.pyplot as plt
import numpy as np


array_ev_clean = np.load('../data/preprocessing/ev_clean.npy', allow_pickle=True)


wday = np.arange(0,5)

split_ev = np.empty((4,1), object)

wday_count = 0; wend_count = 0
date_idx = dt.date(2012, 1, 1)
while date_idx.year != 2013:
    if date_idx.weekday() in wday:
        wday_count += 1
    else:
        wend_count += 1
    date_idx += dt.timedelta(days=1)

for lot in range(4):
    split_ev[lot, 0] = np.empty((1,2), object)
    split_ev[lot, 0][0, 0] = np.empty((1, wday_count), object)
    split_ev[lot, 0][0, 1] = np.empty((1, wend_count), object)

"""
split_ev[lot, 0][0, Wday?][0, day]
Wday == 0 if weekday
Wday == 1 if weekend
"""
fig = plt.figure()
ax = plt.axes()

def plot_ev(array, fig, ax, wday, lot, count):
    if wday:
        location = f'../data/monte/Lot {lot} Wday {count}.png'
        title = f'Lot{lot} Wday{count}'
    else:
        location = f'../data/monte/Lot {lot} Wend {count}.png'
        title = f'Lot{lot} Wend{count}'

    x = np.arange(array.shape[0])
    ax.scatter(x, array[:, 0], label='Arrival')
    ax.scatter(x, array[:, 0] + array[:, 1], label='Duration')
    ax.set_title(title)
    ax.legend()
    fig.savefig(location, dpi=150, bbox_inches='tight')
    plt.close(fig)
    ax.cla()

#             plot_ev(split_ev[lot, 0][0, 0][0, wday_count], \
#                     fig, ax, True, lot, wday_count)
#             plot_ev(split_ev[lot, 0][0, 1][0, wend_count], \
#                     fig, ax, False, lot, wend_count)

for lot in range(4):
    wday_count = 0; wend_count = 0; day_count=0
    date_idx = dt.date(2012, 1, 1)
    while date_idx.year != 2013:
        # Return day of the week, where Monday == 0 ... Sunday == 6
        if date_idx.weekday() in wday:
            split_ev[lot, 0][0, 0][0, wday_count] = \
                    array_ev_clean[lot, day_count]

            wday_count += 1
        else:
            split_ev[lot, 0][0, 1][0, wend_count] = \
                    array_ev_clean[lot, day_count]
            wend_count += 1
        day_count += 1
        date_idx += dt.timedelta(days=1)
