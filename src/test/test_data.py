import numpy as np
import os

# py.test -v

current_dir = os.getcwd()
if current_dir[-4:] == 'test':
    os.chdir('..')


def test_ev():
    array_ev = np.load('data/preprocessing/ev.npy', allow_pickle=True)
    assert array_ev.shape == (6, 366)


def test_ev_clean():
    array_ev_clean = np.load('data/preprocessing/ev_clean.npy', allow_pickle=True)
    assert array_ev_clean.shape == (4, 366)


def test_pv():
    Ppv = np.load('data/preprocessing/pv.npy')
    assert Ppv.shape == (6, 8760)


def test_wt():
    Pwt = np.load('data/preprocessing/wt.npy')
    assert Pwt.shape == (10, 8760)
