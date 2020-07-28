import numpy as np

array_ev = np.load('../data/preprocessing/ev.npy', allow_pickle=True)

np.save('../data/preprocessing/ev_clean.npy', array_ev)

print('Hey there')
