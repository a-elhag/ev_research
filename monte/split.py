import datetime as dt
import numpy as np

class Split():
    """ Split data to seasons, hours and/or weekends/days """

    def __init__(self, data, ev_flag = False):
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

    def hour_no(self, day):
        return self.day_no(day)*24

    def season_range(self):
        # Day 1 needs to wrap around, in our PV+WT data we have only 365 days but
        # in 2012 there is 366 days (that's why we add 1 extra day)

        self.day1 = self.seasons_days[0] - dt.date(2012, 1, 1)
        self.day1 = self.day1.days + 1
        self.hour1 = self.day1*24

        if self.ev_flag:
            self.seasons_range = np.empty((4), object)
            self.seasons_range[0] = np.array(range(self.day1, self.day_no(1)))
            self.seasons_range[1] = np.array(range(self.day_no(1), self.day_no(2)))
            self.seasons_range[2] = np.array(range(self.day_no(2), self.day_no(3)))
            self.seasons_range[3] = np.array(range(self.day_no(3), self.day_no(4)))
        else:
            self.seasons_range = np.empty((4), object)
            self.seasons_range[0] = np.array(range(self.hour1, self.hour_no(1)))
            self.seasons_range[1] = np.array(range(self.hour_no(1), self.hour_no(2)))
            self.seasons_range[2] = np.array(range(self.hour_no(2), self.hour_no(3)))
            self.seasons_range[3] = np.array(range(self.hour_no(3), self.hour_no(4)))


    def season_split(self):
        self.seasons = np.empty((4), object)

        if self.ev_flag:
            for _ in range(4):
                self.seasons[_] = self.data.take(self.seasons_range[_],
                                                 axis=1, mode='wrap')
        else:
            for _ in range(4):
                self.seasons[_] = self.data.take(self.seasons_range[_],
                                                 axis=1, mode='wrap')

    def hour_split(self):
        self.seasons_hours = np.empty((4, 24), object)

        if self.ev_flag:
            pass
        else:
            for season in range(4):
                for hour in range(24):
                    self.seasons_hours[season, hour] = \
                    self.seasons[season][:, hour::24].flatten()


array_ev_clean = np.load('../data/preprocessing/ev_clean.npy', allow_pickle=True)
Ppv = np.load('../data/preprocessing/pv.npy')
Pwt = np.load('../data/preprocessing/wt.npy')

split_pv = Split(Ppv)
split_pv.season_range()
split_pv.season_split()
split_pv.hour_split()

split_wt = Split(Pwt)
split_wt.season_range()
split_wt.season_split()
split_wt.hour_split()

split_ev = Split(array_ev_clean, True)
split_ev.season_range()
split_ev.season_split()
