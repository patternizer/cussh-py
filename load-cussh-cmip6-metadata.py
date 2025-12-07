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

use_tas = True 			# [True (default), False=pr]

if use_tas == True:
    vartypestr = 'regridded-tas-monthly'
else:
    vartypestr = 'regridded-pr-monthly'

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

        version.append(words[7].split('.')[0])
        variable.append(words[0])
        product_type.append('np.nan')
        experiment.append(words[3])
        temporal_aggregation.append('monthly')
        period.append(words[6])
        ensemble_member.append(words[4])
        model.append(words[2])

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

df.to_csv('OUT/cussh-cmip6' + '-' + vartypestr + '-' + 'metadata.csv')
dg.to_csv('OUT/cussh-cmip6' + '-' + vartypestr + '-' + 'counts.csv')
dh.to_csv('OUT/cussh-cmip6' + '-' + vartypestr + '-' + 'summary.csv')
    
#------------------------------------------------------------------------------
print('** END')


