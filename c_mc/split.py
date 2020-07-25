import datetime as dt
import numpy as np

array_ev = np.load('../a_data/b_vs/out/ev.npy', allow_pickle=True)
Ppv = np.load('../a_data/b_vs/out/pv.npy')
Pwt = np.load('../a_data/b_vs/out/wt.npy')

class Split():
    """ Split data to seasons, hours and/or weekends/days """

    def __init__(self, data, ev_flag):
        self.data = data
        self.ev_flag = ev_flag

        """
        Season 1 (Winter): Dec21-Mar19 || (89 Days)
        Season 2 (Spring): Mar20-Jun20 || (93 Days)
        Season 3 (Summer): Jun21-Sep21 || (93 Days)
        Season 4 (Autumn): Sep22-Dec20 || (90 Days)
        """
        self.seasons_days = np.empty((5), object)
        self.seasons_days[0] = dt.date(2011, 12, 21) # Winter
        self.seasons_days[1] = dt.date(2012, 3, 20)  # Spring
        self.seasons_days[2] = dt.date(2012, 6, 21)  # Summer
        self.seasons_days[3] = dt.date(2012, 9, 22)  # Autumn
        self.seasons_days[4] = dt.date(2012, 12, 21) # Wrap around

    def day_no(self, day):
        return (self.seasons_days[day] - dt.date(2012, 1, 1)).days

    def season_split(self):
        self.seasons = np.empty((1,4), object)
        self.seasons_range = np.empty((1,4), object)



        if self.ev_flag:
            pass
        else:
            pass


split_pv = Split(Ppv, False)
