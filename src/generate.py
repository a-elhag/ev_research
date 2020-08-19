import matplotlib.pyplot as plt
from monte_pvwt import full_icdf
import numpy as np
from split_pvwt import SplitRenewables
from sql_numpy import SQL_Numpy

pv_data = np.load('data/preprocessing/pv.npy', allow_pickle=True)

pv_split = SplitRenewables(pv_data)
pv_split.run()

pv_split = SplitRenewables(pv_data)
pv_split.run()
#pv_split.data_out

pv_gen = full_icdf(pv_split.data_out, 1)

pv_sql = SQL_Numpy('pv.db')
pv_sql.connect()
pv_sql.insert(pv_gen)                              
                                                   
pv_sql.first_select()                              
                                                   
pv_sql.commit()                                    
pv_sql.close()                                     
                                                   
