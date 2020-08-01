import matplotlib.pyplot as plt
import numpy as np
from split_pvwt import SplitRenewables
import time

Ppv = np.load('../data/preprocessing/pv.npy')
Pwt = np.load('../data/preprocessing/wt.npy')

split_pv = SplitRenewables(Ppv)
split_pv.run() # split_pv.data_out

split_wt = SplitRenewables(Pwt)
split_wt.run() # split_wt.data_out

bins_pv = np.empty((4,24), object)
bins_wt = np.empty((4,24), object)

def timing(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        output = func(*args, **kwargs)
        end_time = time.time() - start_time
        print(end_time)
        return output
    return wrapper

@timing
def simple_icdf(iter):
    rand = np.random.rand(iter)
    B = np.quantile(split_pv.data_out[2,10], rand)
    return B


PV = simple_icdf(1000*8760)
