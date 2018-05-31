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
import seaborn as sns

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

    aus = dmin[200:280,220:320]
    aus_map = map[200:280,220:320]
    afr1 = dmin[100:260,0:120]
    afr2 = dmin[100:260,680:720]
    afr = np.hstack((afr2, afr1))
    afr1_map = map[100:260,0:120]
    afr2_map = map[100:260,680:720]
    afr_map = np.hstack((afr2_map, afr1_map))

    width = 10
    height = 5
    fig = plt.figure(figsize=(width, height))
    fig.subplots_adjust(hspace=0.05)
    fig.subplots_adjust(wspace=0.05)
    plt.rcParams['text.usetex'] = False
    plt.rcParams['font.family'] = "sans-serif"
    plt.rcParams['font.sans-serif'] = "Helvetica"
    plt.rcParams['axes.labelsize'] = 14
    plt.rcParams['font.size'] = 14
    plt.rcParams['legend.fontsize'] = 10
    plt.rcParams['xtick.labelsize'] = 14
    plt.rcParams['ytick.labelsize'] = 14

    ax1 = fig.add_subplot(1,2,1)
    ax2 = fig.add_subplot(1,2,2)

    aus = aus[~np.isnan(aus)]
    afr = afr[~np.isnan(afr)]
    sns.distplot(aus, ax=ax1)
    sns.distplot(afr, ax=ax2)

    props = dict(boxstyle='round', facecolor='white', alpha=1.0,
                 ec="white")

    fig_label = "%s" % ("Australia")
    ax1.text(0.02, 0.95, fig_label,
            transform=ax1.transAxes, fontsize=12, verticalalignment='top',
            bbox=props)
    fig_label = "%s" % ("Africa")
    ax2.text(0.02, 0.95, fig_label,
            transform=ax2.transAxes, fontsize=12, verticalalignment='top',
            bbox=props)

    ax1.set_ylim(0, 1)
    ax2.set_ylim(0, 1)
    ax1.set_xlim(-4, 0)
    ax2.set_xlim(-4, 0)

    from matplotlib.ticker import MaxNLocator
    ax1.yaxis.set_major_locator(MaxNLocator(4))
    ax2.xaxis.set_major_locator(MaxNLocator(4))
    ax1.tick_params(direction='in', length=4)
    ax2.tick_params(direction='in', length=4)

    ax1.set_ylabel("Density")
    ax1.set_xlabel("Foley's Index", position=(0.5, 1.0))

    plt.setp(ax2.get_yticklabels(), visible=False)

    plt.show()

if __name__ == "__main__":

    main()
