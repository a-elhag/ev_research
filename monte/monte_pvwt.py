import matplotlib.pyplot as plt
import numpy as np
from split_pvwt import SplitRenewables

Ppv = np.load('../data/preprocessing/pv.npy')
Pwt = np.load('../data/preprocessing/wt.npy')

split_pv = SplitRenewables(Ppv)
split_pv.run() # split_pv.data_out

split_wt = SplitRenewables(Pwt)
split_wt.run() # split_wt.data_out

bins_pv = np.empty((4,24), object)
bins_wt = np.empty((4,24), object)

pdf, bin_edges = np.histogram(split_pv.data_out[0,0]) # Density normalizes
pdf = pdf/pdf.sum()
cdf = np.cumsum(pdf)
