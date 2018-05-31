#!/usr/bin/env python
# coding: utf-8

"""
Calculate long-term drought index standardised by the MAP following:

Fensham et al. (2009) Global Change Biology, 15, 380-387.

Which is actually based on:

Foley JC (1957) Droughts in Australia. Review of records from earliest years of
settlement to 1955. Bulletin No. 47, Bureau of Meteorology, Commonwealth of
Australia, Melbourne.
"""

__author__ = "Martin De Kauwe"
__version__ = "1.0 (31.05.2018)"
__email__ = "mdekauwe@gmail.com"

import os
import sys
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt


def main(odir, map, met_fname, deficit_period):

    ds = xr.open_dataset(met_fname)
    nrows = ds["lat"].size
    ncols = ds["lon"].size
    ntime = ds["time"].size
    st = int(ds["time"][0].values.astype(str)[:4])
    en = int(ds["time"][-1].values.astype(str)[:4])
    nyears = (en - st) + 1
    nmonths = 12

    # drought index
    foley_d = np.zeros((nyears-deficit_period,nmonths,nrows,ncols))

    # rainfall in month, year in a given year
    dmy = np.zeros((nyears-1,nmonths,nrows,ncols))

    y = 0
    i = nmonths
    for year in range(st+1, en+1):
        for m in range(12):
            dmy[y,m,:,:] += (ds["precip"][i-m,:,:] - map) / map
        y += 1
        i += nmonths

    y = deficit_period
    for year in range(st+deficit_period, en+1):
        for m in range(12):
            print(year, y-deficit_period, y, m)
            foley_d[y-deficit_period,m,:,:] = dmy[y-deficit_period:y,m,:,:].sum(axis=0)
        y += 1

    ofile = open(os.path.join(odir, "drought_index.bin"), "w")
    foley_d.tofile(ofile)


if __name__ == "__main__":

    met_dir = "data/"
    met_fname = os.path.join(met_dir, "precip.mon.total.v7.nc")

    odir = "outputs"
    map = os.path.join(odir, "map.bin")

    nrows = 360
    ncols = 720
    fname = os.path.join(odir, "map.bin")
    map = np.fromfile(fname, dtype=np.float32).reshape(nrows, ncols)

    deficit_period = 3
    main(odir, map, met_fname, deficit_period)
