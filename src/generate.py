import matplotlib.pyplot as plt
import numpy as np
from split_pvwt import SplitRenewables
from sql_numpy import SQL_Numpy

pv_data = np.load('data/preprocessing/pv.npy', allow_pickle=True)

split_pv = SplitRenewables(pv_data)
split_pv.run()
# pv_sql = SQL_Numpy('pv.db')

