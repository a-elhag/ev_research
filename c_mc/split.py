import numpy as np

array_ev = np.load('../a_data/b_vs/out/ev.npy', allow_pickle=True)
Ppv = np.load('../a_data/b_vs/out/pv.npy')
Pwt = np.load('../a_data/b_vs/out/wt.npy')

"""
Seasons Splits
Season 1 (Winter): Dec21-Mar19 || (89 Days)
Season 2 (Spring): Mar20-Jun20 || (93 Days)
Season 3 (Summer): Jun21-Sep21 || (93 Days)
Season 4 (Autumn): Sep22-Dec20 || (90 Days)

S1_D1 = 8760 - 264 + 1;
S1_D2 = 1872;
S2_D1 = 1872 + 1;
S2_D2 = 1872 + 93*24;
S3_D1 = 4104 + 1;
S3_D2 = 4104 + 93*24;
S4_D1 = 6336 +1;
S4_D2 = 6336 + 90*24;

S1 = S1_D2 + (8760-S1_D1+1);
S2 = S2_D2 - S2_D1 + 1;
S3 = S3_D2 - S3_D1 + 1;
S4 = S4_D2 - S4_D1 + 1;
"""
class Split():
    """ Split data to seasons, hours and/or weekends/days """

    def __init__(self, data, ev_flag):
        self.data = data
        self.ev_flag = ev_flag

    def season_split(self):
        self.seasons = np.empty((1,4), object)

        if self.ev_flag:
            pass
        else:
            pass

split_pv = Split(Ppv, False)
split_pv.season_split()
