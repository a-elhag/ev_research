import numpy as np
from scipy.io import loadmat

class EV():
    def __init__(self, data_location):
        """
        for key, value in data_ev.items():
            if type(value).__module__ == np.__name__:
                print(key, value.shape)

        Logic710_hr (1, 366)
        Logic36_hr (1, 366)
        Logic89_hr (1, 366)
        Logic1_hr (1, 366)
        Logic11_hr (1, 366)
        Logic801_hr (1, 366)

        !Indexing for Dummies!
        data_ev['LogicXXX_hr'][0, day][driver, hour]
        """
        self.data = loadmat(data_location)

    def parsing(self):
        """
        We need to find when our drivers arrive and for how long they stay

        self.ev_parse[parking_lot, day][driver, 0] ==> Arrival
        self.ev_parse[parking_lot, day][driver, 1] ==> Duration
        """
        self.ev_parse = np.empty((6, 366), object)

        idx = -1
        for key, lot in self.data.items():
            if type(lot).__module__ == np.__name__:
                idx += 1
                for day in range(lot.shape[1]):
                    list_ev = []
                    lot_day = lot[0, day]

                    for lot_day_row in lot_day:
                        try:
                            idx_row = list(lot_day_row).index(1)
                            sum_row = np.sum(lot_day_row)
                            list_ev.append([idx_row, sum_row])
                        except:
                            break
                    self.ev_parse[idx, day] = np.array(list_ev)

    def clean(self):
        self.lot_keep = np.array([0, 1, 3, 4])
        self.ev_clean = self.ev_parse[self.lot_keep, :]

    def run(self):
        self.parsing()
        self.clean()

    def save(self, out_location):
        np.save(out_location, self.ev_clean)

data_location = '../data/in/parking_lot.mat'
out_location = '../data/preprocessing/ev.npy'

my_ev = EV(data_location)
my_ev.run()
my_ev.save(out_location)
