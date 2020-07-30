import numpy as np
import os

# py.test -v

current_dir = os.getcwd()
if current_dir[-4:] == 'test':
    os.chdir('..')


def test_ev_split():
    """ Make sure that we have the same number of arrivals that correspond with durations"""
    ev_split = np.load('data/preprocessing/ev_split.npy', allow_pickle=True)
    for lot in range(4):
        for wday in range(2):
            for hour in range(24):
                arr_size = ev_split[lot, wday][0, hour].sum()
                dur_shape = ev_split[lot, wday][1, hour].shape[0]
                assert arr_size == dur_shape


