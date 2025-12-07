#! /usr/bin python

#------------------------------------------------------------------------------
# PROGRAM: merge_models.py
#------------------------------------------------------------------------------
# Version 0.1
# 22 September, 2023
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
#import xarray as xr
#import cftime

# OS libraries:
import os
import glob
#import sys
#import time

#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# SETTINGS: 
#------------------------------------------------------------------------------

year_start, year_end = 1850, 2100
thresholds = [ 'threshold1', 'threshold2', 'threshold3', 'threshold4' ]
 
#------------------------------------------------------------------------------
# LOAD: timeseries for each variable per projection for all models from .pkl and extract lists
#------------------------------------------------------------------------------

filelist = sorted( glob.glob( 'RUN/' + '*.pkl' ), reverse = False )

variablelist = []
projectionlist = []
citylist = []
modellist = []

for i in range(len(filelist)):
    
    words = filelist[i].split('/')[1].split('.')[0].split('_')
    variable = words[0]
    projection = words[1].split('-')[1]
    city = words[2]
    model = words[3]

    variablelist.append( variable )    
    projectionlist.append( projection )    
    citylist.append( city ) 
    modellist.append( model )
    
variables = np.unique( np.array( variablelist ) )
projections = np.unique( np.array( projectionlist ) )
cities = np.unique( np.array( citylist ) )
models = np.unique( np.array( modellist ) )
models = [ models[i].replace('-','_').lower() for i in range(len(models)) ]
    
for v in range(len(variables)):

    for j in range(len(thresholds)):

        for c in range(len(cities)):
    
            for p in range(len(projections)):                        
    
                # INIT: standard dataframe for timeseries
                
                t = pd.date_range(start=str(year_start), end=str(year_end), freq='AS')
                df = pd.DataFrame( {'datetimes':t} )
    
                for f in range(len(filelist)):
                                      
                    words = filelist[f].split('/')[1].split('.')[0].split('_')
                    variable = words[0]
                    parameter = words[1].split('-')[0]
                    projection = words[1].split('-')[1]
                    city = words[2]
                    model = words[3]
                                                                                        
                    if ( ( variable == variables[v] ) & ( parameter == thresholds[j] ) ) &  ( ( city == cities[c] )  & ( projection == projections[p] ) ):
        
                        print(variable, parameter, city, projection, model)                
        
                        # EXTRACT: timeseries at location and append to dataframe
                
                        ds = pd.read_pickle( filelist[f], compression='bz2' )                
    
                        t = pd.date_range(start=str(ds.datetimes.dt.year.values[0]), end=str(ds.datetimes.dt.year.values[-1]+1), freq='AS')[0:-1]
                        ts = ds[model].values
                                                          
                        dv = pd.DataFrame( {'datetimes':t, model:ts} )    
                        df = df.merge(dv, how='left', on='datetimes')
                        
                    else:
                        
                        continue
                                    
                #------------------------------------------------------------------------------
                # SAVE: dataframe for each variable per projection for all models
                #------------------------------------------------------------------------------
                                    
                df.to_pickle( variables[v] + '_' + thresholds[j] + '_' + projections[p] + '_' + cities[c] + '.pkl', compression='bz2')

#------------------------------------------------------------------------------
print('** END')

    
