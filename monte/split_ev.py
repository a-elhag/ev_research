import datetime as dt
import matplotlib.pyplot as plt
import numpy as np

array_ev_clean = np.load('../data/preprocessing/ev_clean.npy', allow_pickle=True)

wday = np.arange(0,5)

split_ev = np.empty((4,1), object)


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

for lot in range(4):
    day_count=0
    date_idx = dt.date(2012, 1, 1)
    list_day_arr = []; list_day_dur = []; list_end_arr = []; list_end_dur = []
    while date_idx.year != 2013:
        # Return day of the week, where Monday == 0 ... Sunday == 6
        if array_ev_clean[lot, day_count].size == 0:
            day_count += 1
            date_idx += dt.timedelta(days=1)
            continue
        if date_idx.weekday() in wday:
            list_day_arr.extend(array_ev_clean[lot, day_count][:, 0].tolist())
            list_day_dur.extend(array_ev_clean[lot, day_count][:, 1].tolist())
        else:
            list_end_arr.extend(array_ev_clean[lot, day_count][:, 0].tolist())
            list_end_dur.extend(array_ev_clean[lot, day_count][:, 1].tolist())
        day_count += 1
        date_idx += dt.timedelta(days=1)

for lot in range(4):
    split_ev[lot, 0] = np.empty((1,2), object)

    split_ev[lot, 0][0, 0] = np.array(list_day_arr)
    split_ev[lot, 0][0, 1] = np.array(list_day_dur)
    split_ev[lot, 0][0, 0] = np.array(list_end_arr)
    split_ev[lot, 0][0, 1] = np.array(list_end_dur)

# Test comment

