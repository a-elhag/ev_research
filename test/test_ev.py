import numpy as np
import os

# py.test -v

current_dir = os.getcwd()
if current_dir[-4:] == 'test':
    os.chdir('..')


def test_original_ev():
    array_ev = np.load('a_data/b_vs/out/ev.npy', allow_pickle=True)
    assert array_ev.shape == (6, 366)


