#! /usr/bin python

#------------------------------------------------------------------------------
# PROGRAM: load-cussh-isimip-metadata.py
#------------------------------------------------------------------------------
# Version 0.3
# 28 August, 2023
# Michael Taylor
# https://patternizer.github.io
# michael DOT a DOT taylor AT uea DOT ac DOT uk
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# IMPORT PYTHON LIBRARIES
#------------------------------------------------------------------------------
# Dataframe libraries:
import numpy as np
import pandas as pd
import xarray as xr
# OS libraries:
import os
import glob
import sys
import time
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# SETTINGS: 
#------------------------------------------------------------------------------

use_yearly = True 		        # [True (default), False=monthly]
use_percentile_based = True 	# [True (default), False=baseline-independent]

if use_percentile_based == True:
    if use_yearly == True:
        vartypestr = 'regridded-etccdi-percentile-based-yearly'
    else:
        vartypestr = 'regridded-etccdi-percentile-based-monthly'
else:
    if use_yearly == True:
        vartypestr = 'regridded-etccdi-baseline-independent-yearly'
    else:
        vartypestr = 'regridded-etccdi-baseline-independent-monthly'

modeldir = 'DATA/' + vartypestr + '/'

#------------------------------------------------------------------------------
# LOAD: all C3S CDS models and extract metadata
#------------------------------------------------------------------------------

df = pd.DataFrame()

version = []
variable = []
product_type = []
experiment = []
temporal_aggregation = []
period = []
ensemble_member = []
model = []
lon_resolution = []
lat_resolution = []
    
filelist = sorted( glob.glob( modeldir + '*.nc' ), reverse = False )

for j in range(len(filelist)):

        file = filelist[j]
        ds = xr.open_dataset( file, decode_times=False )
        dlon = (ds.lon[1] - ds.lon[0]).values + 0
        dlat = (ds.lat[1] - ds.lat[0]).values + 0
        lat_resolution.append( dlat )
        lon_resolution.append( dlon )
        
        words = filelist[j].replace(modeldir,'').split('_')

        version.append(words[8].split('.')[0])
        variable.append(words[0])
        product_type.append(words[5])
        experiment.append(words[3])
        temporal_aggregation.append(words[1])
        period.append(words[7])
        ensemble_member.append(words[4])
        model.append(words[2])

        '''
        csdiETCCDI_yr_ACCESS-CM2_historical_r1i1p1f1_b1961-1990_v20191108_1850-2014_v2-0.nc         # percetile-based-yearly
        tn10pETCCDI_mon_ACCESS-CM2_historical_r1i1p1f1_b1961-1990_v20191108_185001-201412_v2-0.nc   # percetile-based-yearly
        cddETCCDI_yr_ACCESS-CM2_historical_r1i1p1f1_no-base_v20191108_1850-2014_v2-0.nc             # baseline-independent-yearly
        dtrETCCDI_mon_ACCESS-CM2_historical_r1i1p1f1_no-base_v20191108_185001-201412_v2-0.nc        # baseline-independent-monthly 
        '''

df['version'] = version
df['variable'] = variable
df['product_type'] = product_type
df['experiment'] = experiment
df['temporal_aggregation'] = temporal_aggregation
df['period'] = period
df['ensemble_member'] = ensemble_member
df['model'] = model
df['lat_resolution'] = lat_resolution
df['lon_resolution'] = lon_resolution

#------------------------------------------------------------------------------
# EXTRACT: unique cases and count
#------------------------------------------------------------------------------

dg = df.groupby('model').nunique()
dh = df.groupby('model')[list(['ensemble_member','lat_resolution','lon_resolution'])].agg(['unique'])

#------------------------------------------------------------------------------
# FILTER: models that do not have full complement (historical,ssp126,ssp370)
#------------------------------------------------------------------------------

modeldroplist = dg.index[dg.experiment<3]
df = df[~df['model'].isin(modeldroplist)]
dg = dg[~dg.index.isin(modeldroplist)]
dh = dh[~dh.index.isin(modeldroplist)]

#------------------------------------------------------------------------------
# SAVE: metadata dataframe and variable counts and summary per model
#------------------------------------------------------------------------------

df.to_csv('OUT/cussh-isimip' + '-' + vartypestr + '-' + 'metadata.csv')
dg.to_csv('OUT/cussh-isimip' + '-' + vartypestr + '-' + 'counts.csv')
dh.to_csv('OUT/cussh-isimip' + '-' + vartypestr + '-' + 'summary.csv')
    
#------------------------------------------------------------------------------
print('** END')


    
    
