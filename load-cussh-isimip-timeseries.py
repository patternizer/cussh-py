#! /usr/bin python

#------------------------------------------------------------------------------
# PROGRAM: load-cussh-isimip-timeseries.py
#------------------------------------------------------------------------------
# Version 0.1
# 8 July, 2023
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

# Plotting libraries:
import matplotlib.pyplot as plt; plt.close('all')
from pandas.plotting import register_matplotlib_converters
from matplotlib import rcParams
register_matplotlib_converters()
import matplotlib.dates as mdates
import seaborn as sns; sns.set()

#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# SETTINGS: 
#------------------------------------------------------------------------------

location_lat, location_lon = -1.28638, 36.817222 # Nairobi

#------------------------------------------------------------------------------
# LOAD: C3S CDS ISIMIP model metadata file
#------------------------------------------------------------------------------

di = pd.read_csv( 'cussh-isimip-metadata.csv', index_col=0 )
variables = di.variable.unique()
projections = di.experiment.unique()
models = di.model.unique()

#------------------------------------------------------------------------------
# LOAD: timeseries for each variable per projection for all models into separate dataframes
#------------------------------------------------------------------------------

for v in range(len(variables)):

    for p in range(len(projections)):                        

        # INIT: standard dataframe for timeseries
        
        t = pd.date_range(start=str(1850), end=str(2100), freq='AS')
        df = pd.DataFrame( {'datetimes':t} )
    
        for i in range(len(models)):
               
            modeldir = 'DATA/' + models[i].lower() + '/'
            filelist = sorted( glob.glob( modeldir + '*.nc' ), reverse = False )
            
            for j in range(len(filelist)):
                        
                words = filelist[j].replace(modeldir,'').split('_')
                parameter = words[0]
                projection = words[3]
                            
                if ( parameter == variables[v] ) & ( projection == projections[p] ):
    
                    # EXTRACT: timeseries at location and append to dataframe
            
                    ds = xr.open_dataset( filelist[j], decode_times=True )
                    t = pd.date_range(start=str(ds.time.dt.year[0].values+0), end=str(ds.time.dt.year[-1].values+0), freq='AS')
                    
                    if ( parameter == 'wsdiETCCDI' ) | ( parameter == 'csdiETCCDI' ):                    
                        ts = ds[parameter].sel( lat = location_lat, lon = location_lon, method='nearest').values.astype('timedelta64[D]').astype(int)
                    else:
                        ts = ds[parameter].sel( lat = location_lat, lon = location_lon, method='nearest').values
            
                    dv = pd.DataFrame( {'datetimes':t, models[i]:ts} )    
                    df = df.merge(dv, how='left', on='datetimes')
        
                    #------------------------------------------------------------------------------
                    # SAVE: dataframe for each variable per projection for all models
                    #------------------------------------------------------------------------------
                    
                    df.to_pickle( variables[v] + '_' + projections[p] + '.pkl', compression='bz2')
#                    df.to_csv( variables[v] + '_' + projections[p] + '.csv')
        
#------------------------------------------------------------------------------
print('** END')


    
    
