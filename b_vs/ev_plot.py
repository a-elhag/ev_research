import calendar
import datetime as dt
import matplotlib.pyplot as plt
import numpy as np

array_ev = np.load('../a_data/b_vs/out/ev.npy', allow_pickle = True)


def what_day(day):
    new_year = dt.date(2012, 1, 1)
    day_now = new_year + dt.timedelta(days=day)
    return calendar.day_name[day_now.weekday()]


fig = np.empty(20, object)
ax = np.empty(20, object)

year = 0
for c, day in enumerate(range(10, 30)):
    fig[c] = plt.figure()
    ax[c] = plt.axes()
    if array_ev[0, day].ndim ==1:
        continue

    day_name = what_day(day)

    x = np.arange(array_ev[year, day].shape[0])
    ax[c].scatter(x, array_ev[year, day][:,0], label='Arrival')
    ax[c].scatter(x, array_ev[year, day][:,0] + array_ev[year, day][:,1], label='Duration')
    ax[c].set_title(f"Year: {year}, Day: {day_name}")
    ax[c].legend()

# plt.show()
