import numpy as np
"""
We have to get rid of two lots because there are issues with them
==> Lot 2: There really isn't anything wrong with it, but the number of
           drivers don't exceed 20 on a given day. Too much overhead
           for something like this for too little gain
==> Lot 5: Durations are fine, but all arrivals are set at 0
"""
array_ev = np.load('../data/preprocessing/ev.npy', allow_pickle=True)

idx = np.array([0, 1, 3, 4])
array_ev_clean = array_ev[idx, :]

np.save('../data/preprocessing/ev_clean.npy', array_ev_clean)
