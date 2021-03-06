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

    amy_sum = np.zeros((nrows, ncols))
    step = 12 * deficit_period
    i = step
    y = 0
    for year in range(st+deficit_period, en+1):
        print(year)
        for m in range(12):

            # Loop over last N (deficit period) years, calculating summed
            # monthly rainfall over the previous 12 months of each year
            amy_sum = 0.0
            stepx = int(step / deficit_period)
            ii = i
            for j in range(deficit_period):

                # summed monthly rainfall over the previous 12 months of the yr
                amy = ds["precip"][i-stepx:ii,:,:].values.sum(axis=0)
                amy_sum += (amy - map) / map

                ii = i-stepx
                stepx += int(step/deficit_period)

            foley_d[y,m,:,:] = amy_sum

            i += 1
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
