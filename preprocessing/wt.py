import numpy as np
from scipy.io import loadmat

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

        np.save('../data/preprocessing/wt.npy', self.Pwt)

    def run(self):
        self.characteristics()
        self.power_output()

    def save(self, out_location):
        np.save(out_location, self.Pwt)

data_location = '../data/in/solar_wind.mat'
out_location = '../data/preprocessing/wt.npy'

my_wt = WT(data_location)
my_wt.run()
my_wt.save(out_location)
