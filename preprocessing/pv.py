## Part 1: Initialize
import numpy as np
from scipy.io import loadmat

"""
data:
'tempX' ==> Temperature
'PVdata' ==> Solar insolation
'Wind' ==> Wind speed
"""

class PV():
    def __init__(self, data):
        self.tempX = data['tempX']
        self.tempX = self.tempX.reshape(1, -1)
        self.tempX = np.repeat(self.tempX, 24, axis=1)
        self.tempX = self.tempX.reshape(1, -1)
        self.tempX = np.repeat(self.tempX, 6, axis=0)

        self.PVdata = data['PVdata']
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

    def run(self):
        self.characteristics()


data = loadmat('../data/in/solar_wind.mat')
## Part 3: Fixing Input Data

## Part 3: Calculating Power Output
"""
Because of the fact that there are days with clouds and days without, we have a
two humped shape to our distribution. Making it difficult to model. Thus to
simplify it, we will convert the solar irradiance and temperature into power!

Numpy is row major by default, meaning we have (years, hours).

Check LN02 - Renewable for formulas
"""
Tcell = self.tempX + PVdata * (NOCT-20)/(0.8)
Ipv = PVdata * (Isc + Ki*(Tcell-25))
Vpv = Voc + Kv * (Tcell - 25)
Ppv = Ncells * FF * Vpv * Ipv

## Scaling Ppv

# Note: Due to assumed limitations of our PV panels
# we will limit the output power to PVRatedPower.
Ppv[Ppv > PVRatedPower] = PVRatedPower

# We will scale our data such that the max nominal power is 1
Ppv = Ppv/Ppv.max()

np.save('../data/preprocessing/pv.npy', Ppv)
