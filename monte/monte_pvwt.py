import numpy as np
import split_pvwt

Ppv = np.load('../data/preprocessing/pv.npy')
Pwt = np.load('../data/preprocessing/wt.npy')

split_pv = SplitRenewables(Ppv)
split_pv.run()

split_wt = SplitRenewables(Pwt)
split_wt.run()
