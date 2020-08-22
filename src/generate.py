## Part 1: Libraries
import matplotlib.pyplot as plt
from monte_pvwt import full_icdf
import numpy as np
from split_pvwt import SplitRenewables
from sql_numpy import SQL_Numpy

## Part 2: Making Class
class Generate():
    def __init__(self, data_loc, db_loc):
        self.db_loc = db_loc
        self.data_loc = data_loc
        self.data_in = np.load(data_loc, allow_pickle=True)
        self.data_in_split = SplitRenewables(self.data_in)
        self.data_in_split.run() # pv_split.data_out

    def sql_connect(self):
        self.sql = SQL_Numpy(self.db_loc)
        self.sql.connect()

    def sql_commit_close(self):
        self.sql.commit()
        self.sql.close()

    def monte(self, years):
        self.sql_connect()
        self.data_gen = full_icdf(self.data_in_split.data_out, years)
        self.sql.insert(self.data_gen)
        self.sql_commit_close()

    def yank(self):
        self.sql_connect()
        self.sql.first_select()
        self.data_out = self.sql.data
        self.sql.first_delete()
        self.sql_commit_close()

## Part 3: Running
if __name__ == "__main__":
    pv_gen = Generate('data/preprocessing/pv.npy', 'data/db/pv.db')
    for year in range(1, 5):
        pv_gen.monte(year)
    pv_gen.yank()
