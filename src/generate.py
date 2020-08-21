## Part 1: Libraries
import matplotlib.pyplot as plt
from monte_pvwt import full_icdf
import numpy as np
from split_pvwt import SplitRenewables
from sql_numpy import SQL_Numpy

## Part 2: Loading Data
pv_data = np.load('data/preprocessing/pv.npy', allow_pickle=True)

pv_split = SplitRenewables(pv_data)
pv_split.run()

pv_split = SplitRenewables(pv_data)
pv_split.run() # pv_split.data_out

## Part 3: Saving Data into Database
pv_sql = SQL_Numpy('db_pv.db')
pv_sql.connect()
for repeat in range(4):
    pv_gen = full_icdf(pv_split.data_out, repeat)
    pv_sql.insert(pv_gen)

pv_sql.commit()
pv_sql.close()


## Part 4: Saving Data into Database
pv_sql.connect()
pv_sql.first_delete()
pv_sql.first_delete()

pv_sql.commit()
pv_sql.close()
