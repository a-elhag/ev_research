import calendar
import datetime as dt
import matplotlib.pyplot as plt
import numpy as np

array_ev = np.load('../data/preprocessing/ev.npy', allow_pickle = True)


def what_day(day):
    new_year = dt.date(2012, 1, 1)
    day_now = new_year + dt.timedelta(days=day)
    return day_now.__str__(), calendar.day_name[day_now.weekday()]


fig = np.empty((6, 366), object)
ax = np.empty((6, 366), object)

for lot in range(array_ev.shape[0]):
    for day in range(array_ev.shape[1]):
        fig[lot, day] = plt.figure()
        ax[lot, day] = plt.axes()
        if array_ev[lot, day].ndim ==1:
            continue

        date_num, day_name = what_day(day)

        x = np.arange(array_ev[lot, day].shape[0])
        ax[lot, day].scatter(x, array_ev[lot, day][:,0], label='Arrival')
        ax[lot, day].scatter(x, array_ev[lot, day][:,0] + array_ev[lot, day][:,1], label='Duration')
        ax[lot, day].set_title(f"Lot: {lot}, Day: {day_name}, {date_num}")
        ax[lot, day].legend()
        fig[lot, day].savefig(f'../a_data/b_vs/plots/L{lot}-D{day}.png', dpi=150, bbox_inches='tight')
        plt.close(fig[lot, day])

