#!/usr/bin/env python
# coding: utf-8

"""
Figure out the mean annual rainfall (MAP) from the GPCC Global Precipitation
Climatology Centre monthly precipitation dataset
"""

__author__ = "Martin De Kauwe"
__version__ = "1.0 (31.05.2018)"
__email__ = "mdekauwe@gmail.com"

import os
import sys
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt


def main(fname, odir):

    ds = xr.open_dataset(fname)
    nrows = ds["lat"].size
    ncols = ds["lon"].size
    ntime = ds["time"].size

    map = np.zeros((nrows,ncols))
    st = int(ds["time"][0].values.astype(str)[:4])
    en = int(ds["time"][-1].values.astype(str)[:4])
    nyears = (en - st) + 1

    i = 0
    for year in range(st, en+1):
        print(year)
        map += ds["precip"][i:i+12,:,:].values.sum(axis=0)

        i += 12

    map /= float(nyears)
    map = map.astype(np.float32)

    #plt.imshow(map)
    #plt.colorbar()
    #plt.show()

    ofile = open(os.path.join(odir, "map.bin"), "w")
    map.tofile(ofile)
    

if __name__ == "__main__":

    met_dir = "data/"
    fname = os.path.join(met_dir, "precip.mon.total.v7.nc")

    odir = "outputs"
    if not os.path.exists(odir):
        os.makedirs(odir)

    main(fname, odir)
