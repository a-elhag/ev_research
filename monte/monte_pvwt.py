import numpy as np
from split_pvwt import SplitRenewables
import time

Ppv = np.load('../data/preprocessing/pv.npy')
Pwt = np.load('../data/preprocessing/wt.npy')

split_pv = SplitRenewables(Ppv)
split_pv.run() # split_pv.data_out

split_wt = SplitRenewables(Pwt)
split_wt.run() # split_wt.data_out

def simple_icdf(iter):
    rand = np.random.rand(iter)
    B = np.quantile(split_pv.data_out[2,10], rand)
    return B

PV = simple_icdf(1000*8760)

"""
Season 1 (Winter): Dec21-Mar19 || (89 Days)
Season 2 (Spring): Mar20-Jun20 || (93 Days)
Season 3 (Summer): Jun21-Sep21 || (93 Days)
Season 4 (Autumn): Sep22-Dec20 || (90 Days)

But in this one, we are just going to simply go in order.
Jan 1st is the first day of winter and Dec 31st is he last day of Autumn.
"""

def timing(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        output = func(*args, **kwargs)
        end_time = time.time() - start_time
        print(end_time)
        return output
    return wrapper

@timing
def full_icdf(data, years):
    out_array = np.zeros((8760, years))
    for year in range(years):
        seasons = np.r_[89, 93, 93, 90]
        seasons = seasons.cumsum()

        for day in range(365):
            season = seasons[seasons>day][0]
            season = (seasons == season)
            season = np.where(season)[0][0]

            for hour in range(24):
                rand = np.random.rand()
                out = np.quantile(data[season, hour], rand)
                idx_hour = hour + day*24
                out_array[idx_hour, year]

    return np.array(out_array)

A = full_icdf(split_pv.data_out, 100)
