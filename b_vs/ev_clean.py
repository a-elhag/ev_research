import numpy as np

array_ev = np.load('../a_data/b_vs/out/ev.npy', allow_pickle=True)

print(array_ev.shape)

# Remove the first day
array_ev = array_ev[:, 1:]

