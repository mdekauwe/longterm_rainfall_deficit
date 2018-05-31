#!/usr/bin/env python
# coding: utf-8

"""
Various plots ... document later

"""

__author__ = "Martin De Kauwe"
__version__ = "1.0 (31.05.2018)"
__email__ = "mdekauwe@gmail.com"

import os
import sys
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt


def main():

    odir = "outputs"


    nyears = 110
    nmonths = 12
    nrows = 360
    ncols = 720
    fname = os.path.join(odir, "drought_index.bin")
    d = np.fromfile(fname, dtype=np.float64).reshape(nyears, nmonths,
                                                       nrows, ncols)

    d = d.reshape(nyears*nmonths, nrows, ncols)
    dmin = d.min(axis=0)

    fname = os.path.join(odir, "map.bin")
    map = np.fromfile(fname, dtype=np.float32).reshape(nrows, ncols)

    #plt.plot(map, dmin, "k.", alpha=0.1)
    #plt.xlim(0, 2500)
    #plt.show()
    aus = dmin[200:280,220:320]
    aus_map = map[200:280,220:320]
    afr1 = dmin[100:260,0:120]
    afr2 = dmin[100:260,680:720]
    afr = np.hstack((afr2, afr1))
    afr1_map = map[100:260,0:120]
    afr2_map = map[100:260,680:720]
    afr_map = np.hstack((afr2_map, afr1_map))

    plt.plot(afr_map, afr, "k.", alpha=0.1)
    plt.plot(aus_map, aus, "r.", alpha=0.1)
    #plt.xlim(0, 2500)
    plt.show()


    plt.hist(aus)
    plt.show()
    #dmin = np.where(dmin > -1.0, np.nan, dmin)
    #plt.imshow(dmin, origin="upper")
    #plt.colorbar()
    #plt.show()

if __name__ == "__main__":

    main()
