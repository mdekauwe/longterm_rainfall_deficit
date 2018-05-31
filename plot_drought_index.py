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

    dmin = np.where(dmin > -1.0, np.nan, dmin)
    plt.imshow(dmin, origin="upper")
    plt.colorbar()
    plt.show()

if __name__ == "__main__":

    main()
