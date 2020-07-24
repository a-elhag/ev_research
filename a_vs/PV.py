## Part 1: Initialize
import numpy as np
from scipy.io import loadmat

# data ==>
# dict_keys(['__header__', '__version__', '__globals__',
# 'tempX', 'PVdata', 'RTS', 'Wind'])

data = loadmat('1DataOrig.mat')
tempX = data['tempX']
PVdata = data['PVdata']
RTS = data['RTS']

## Part 2: PV Output Power
NOCT = 45
Ki = 0.05
Kv = -0.27  # Kv should always be negative

Isc = 6.43
Voc = 85.6

Impp = 5.97
Vmpp = 72.9

FF = (Vmpp*Impp)/(Voc*Isc)
Ncells = 1
PVRatedPower = 435

## Part 3: Fixing Input Data
tempX = tempX.reshape(1, -1)
tempX = np.repeat(tempX, 24, axis=1)
tempX = tempX.reshape(1, -1)
tempX = np.repeat(tempX, 6, axis=0)

PVdata = PVdata.T  # Sir is in W/m**2
PVdata = PVdata/1000  # Now Sir is in kW/m**2

## Part 3: Calculating Power Output
"""
Because of the fact that there are days with clouds and days without, we have a
two humped shape to our distribution. Making it difficult to model. Thus to
simplify it, we will convert the solar irradiance and temperature into power!

Numpy is row major by default, meaning we have (years, hours).

Check LN02 - Renewable for formulas
"""
Tcell = tempX + PVdata * (NOCT-20)/(0.8)
Ipv = PVdata * (Isc + Ki*(Tcell-25))
Vpv = Voc + Kv * (Tcell - 25)
Ppv = Ncells * FF * Vpv * Ipv

## Scaling Ppv

# Note: Due to assumed limitations of our PV panels
# we will limit the output power to PVRatedPower.
Ppv[Ppv > PVRatedPower] = PVRatedPower

# We will scale our data such that the max nominal power is 1
Ppv = Ppv/Ppv.max()
