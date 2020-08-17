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

class PV:
    def __init__(self, data_location):
        """
        data:
        'tempX' ==> Temperature
        'PVdata' ==> Solar insolation
        'Wind' ==> Wind speed
        """
        self.data = loadmat(data_location)

        self.tempX = self.data['tempX']
        self.tempX = self.tempX.reshape(1, -1)
        self.tempX = np.repeat(self.tempX, 24, axis=1)
        self.tempX = self.tempX.reshape(1, -1)
        self.tempX = np.repeat(self.tempX, 6, axis=0)

        self.PVdata = self.data['PVdata']
        self.PVdata = self.PVdata.T  # Sir is in W/m**2
        self.PVdata = self.PVdata/1000  # Now Sir is in kW/m**2

    def characteristics(self):
        self.NOCT = 45
        self.Ki = 0.05
        self.Kv = -0.27  # Kv should always be negative

        self.Isc = 6.43
        self.Voc = 85.6

        self.Impp = 5.97
        self.Vmpp = 72.9

        self.FF = (self.Vmpp*self.Impp)/(self.Voc*self.Isc)
        self.Ncells = 1
        self.PVRatedPower = 435

    def power_output(self):
        """
        Because of the fact that there are days with clouds and days without, we have a
        two humped shape to our distribution. Making it difficult to model. Thus to
        simplify it, we will convert the solar irradiance and temperature into power!

        Numpy is row major by default, meaning we have (years, hours).

        Check LN02 - Renewable for formulas
        """
        self.Tcell = self.tempX + self.PVdata * (self.NOCT-20)/(0.8)
        self.Ipv = self.PVdata * (self.Isc + self.Ki*(self.Tcell-25))
        self.Vpv = self.Voc + self.Kv * (self.Tcell - 25)
        self.Ppv = self.Ncells * self.FF * self.Vpv * self.Ipv

        # Note: Due to assumed limitations of our PV panels
        # we will limit the output power to PVRatedPower.
        self.Ppv[self.Ppv > self.PVRatedPower] = self.PVRatedPower

        # We will scale our data such that the max nominal power is 1
        self.Ppv = self.Ppv/self.Ppv.max()

    def run(self):
        self.characteristics()
        self.power_output()

    def save(self, out_location):
        np.save(out_location, self.Ppv)

class WT:
    def __init__(self, data_location):
        """
        data:
        'tempX' ==> Temperature
        'PVdata' ==> Solar insolation
        'Wind' ==> Wind speed
        """
        self.data = loadmat(data_location)

        self.wind = self.data['Wind']
        self.wind = self.wind.reshape((10, 8760))

    def characteristics(self):

        """
        Using Approximated WT characteristics

        Wind Edges:
        Cut_In Speed  = 4m/s
        Rated Speed   = 16m/s
        Cut_Out Speed = 25m/s

        How they should look:
        00 0.0  ==>  00 - 01 0.0
        01 4.0  ==>  01 - 02 (4.0+5.5)/2
        02 5.5  ==>  02 - 03 (5.5+7.0)/2
        03 7.0  ==>  03 - 04 (7.0+8.5)/2
        04 8.5  ==>  04 - 05 (8.5+10.0)/2
        05 10.0 ==>  05 - 06 (10.0+11.5)/2
        06 11.5 ==>  06 - 07 (11.5+13.0)/2
        07 13.0 ==>  07 - 08 (13.0+14.5)/2
        08 14.5 ==>  08 - 09 (14.5+16.0)/2
        09 16.0 ==>  09 - 10 16.0 # Rated Speed
        10 25.0 ==>  10 - 11 0.0 # Cut_Out Speed
        11 0.0
        """
        self.edges_wt = np.r_[0, 4:16.5:1.5, 25, 100] # shape(12,)
        self.pow_edges_wt = np.copy(self.edges_wt)
        self.pow_edges_wt = self.pow_edges_wt[:-1] # Power Edges to simulate WT
        self.pow_edges_wt[-1] = 0
        for _ in range(1,self.pow_edges_wt.shape[0]-2):
            self.pow_edges_wt[_] += self.pow_edges_wt[_+1]
            self.pow_edges_wt[_] /= 2

        self.pow_edges_wt = np.r_[0, self.pow_edges_wt] # Placeholder, because bins is always less by one of the edges

    def power_output(self):
        self.Pwt = np.digitize(self.wind, self.edges_wt) # Power Wind Turbine
        self.Pwt = self.pow_edges_wt[self.Pwt]
        self.Pwt = self.Pwt/self.Pwt[:,:].max()

    def run(self):
        self.characteristics()
        self.power_output()

    def save(self, out_location):
        np.save(out_location, self.Pwt)
