#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 12:43:28 2023

@author: cqz20mbu
"""

#! /usr/bin python

#------------------------------------------------------------------------------
# PROGRAM: plot_gcm_unsmoothed.py
#------------------------------------------------------------------------------
# Version 0.1
# 18 October, 2023
# Michael Taylor
# michael DOT a DOT taylor AT uea DOT ac DOT uk 
#------------------------------------------------------------------------------

import numpy as np
import numpy.ma as ma
import pandas as pd
import xarray as xr
import pickle
from datetime import datetime
import netCDF4

# Colour libraries:
import cmocean

# Plotting libraries:
import matplotlib
#matplotlib.use('agg')
import matplotlib.pyplot as plt; plt.close('all')
import matplotlib.cm as cm
from matplotlib import rcParams
from matplotlib.cm import ScalarMappable
from mpl_toolkits.axes_grid1 import make_axes_locatable
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
from matplotlib import colors as mcolors
# %matplotlib inline # for Jupyter Notebooks

# Mapping libraries:
import cartopy
import cartopy.crs as ccrs
from cartopy.io import shapereader
import cartopy.feature as cf
from cartopy.util import add_cyclic_point
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

# Silence library version notifications
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")

#----------------------------------------------------------------------------
# SETTINGS
#----------------------------------------------------------------------------

fontsize = 16
dpi = 300                   # [144,300,600]

#----------------------------------------------------------------------------
# LOAD: GloSAT anomalies station dataframe
#----------------------------------------------------------------------------

print('loading GCM timeseries ...')

df_historical = pd.read_pickle( 'csdiETCCDI_historical_Kisumu.pkl', compression='bz2' )
df_ssp126 = pd.read_pickle( 'csdiETCCDI_ssp126_Kisumu.pkl', compression='bz2' )
df_ssp370 = pd.read_pickle( 'csdiETCCDI_ssp370_Kisumu.pkl', compression='bz2' )

df_historical.index = df_historical['datetimes']
df_ssp126.index = df_ssp126['datetimes']
df_ssp370.index = df_ssp370['datetimes']

del df_historical['datetimes']
del df_ssp126['datetimes']
del df_ssp370['datetimes']

df_historical.to_csv('kisumu-gcm-historial.csv')
df_ssp126.to_csv('kisumu-gcm-ssp126.csv')
df_ssp370.to_csv('kisumu-gcm-ssp370.csv')
