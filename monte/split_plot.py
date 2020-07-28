import matplotlib.pyplot as plt
import numpy as np
from split import Split

array_ev_clean = np.load('../data/preprocessing/ev_clean.npy', allow_pickle=True)
Ppv = np.load('../data/preprocessing/pv.npy')
Pwt = np.load('../data/preprocessing/wt.npy')

split_pv = Split(Ppv)
split_pv.season_range()
split_pv.season_split()
split_pv.hour_split()

split_wt = Split(Pwt)
split_wt.season_range()
split_wt.season_split()
split_wt.hour_split()

split_ev = Split(array_ev_clean, True)
split_ev.season_range()
split_ev.season_split()

fig = np.empty((4,24), object)
ax = np.empty((4,24), object)

def plot_all(data, name, seasons, hours):
    for season in range(seasons):
        for hour in range(hours):
            fig[season, hour] = plt.figure()
            ax[season, hour] = plt.axes()
            ax[season, hour].plot(data[season, hour])
            ax[season, hour].set_title(f" Season: {season} and Hour: {hour}")
            ax[season, hour].set_ylim(0, 1)
            fig[season, hour].savefig(f'../data/split/{name}_S{season}_H{hour}',
                                  dpi=150, bbox_inches='tight')
            plt.close(fig[season, hour])

plot_all(split_pv.seasons_hours, 'PV', 4, 24)
plot_all(split_wt.seasons_hours, 'WT', 4, 24)
