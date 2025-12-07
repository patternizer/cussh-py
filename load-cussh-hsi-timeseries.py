#! /usr/bin python

#------------------------------------------------------------------------------
# PROGRAM: load-cussh-isimip-timeseries.py
#------------------------------------------------------------------------------
# Version 0.4
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
import cftime

# OS libraries:
import os
import glob
import sys
import time

#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# SETTINGS: 
#------------------------------------------------------------------------------

#city, location_lat, location_lon = 'London', 51.5, -0.1
#city, location_lat, location_lon = 'Rennes', 48.1, -1.7
#city, location_lat, location_lon = 'Kisumu', -0.1, 34.8
#city, location_lat, location_lon = 'Nairobi', -1.3, 36.8
#city, location_lat, location_lon = 'Homa', -0.5, 34.5
#city, location_lat, location_lon = 'Beijing', 39.9, 116.4
#city, location_lat, location_lon = 'Ningbo', 29.9, 121.6

cities = list([ 'London', 'Rennes', 'Kisumu', 'Nairobi', 'Homa', 'Beijing', 'Ningbo' ])
location_lats = list([ 51.5, 48.1, -0.1, -1.3, -0.5, 39.9, 29.9 ])
location_lons = list([ -0.1, -1.7, 34.8, 36.8, 34.5, 116.4, 121.6 ])

vartypestr = 'hi-daily'
#vartypestr = 'humindex-daily'
#vartypestr = 'utci-daily'
#vartypestr = 'wbgt-daily'
#vartypestr = 'wbt-daily'
        
if vartypestr == 'hi-daily':
            
    threshold_1 = 27.0
    threshold_2 = 32.0
    threshold_3 = 41.0
    threshold_4 = 54.0

elif vartypestr == 'humindex-daily':
            
    threshold_1 = 30.0
    threshold_2 = 40.0
    threshold_3 = 45.0
    threshold_4 = 54.0

elif vartypestr == 'utci-daily':
            
    threshold_1 = 26.0
    threshold_2 = 32.0
    threshold_3 = 38.0
    threshold_4 = 46.0

elif vartypestr == 'wbgt-daily':
            
    threshold_1 = 29.0
    threshold_2 = 30.5
    threshold_3 = 32.0
    threshold_4 = 37.0
            
elif vartypestr == 'wbt-daily':
            
    threshold_1 = np.nan
    threshold_2 = np.nan
    threshold_3 = np.nan
    threshold_4 = 35.0

modeldir = 'DATA/regridded' + '-' + vartypestr + '/'

year_start, year_end = 1951, 2100

t_daily = pd.date_range(start=str(year_start), end=str(year_end), freq='D')

#------------------------------------------------------------------------------
# LOAD: C3S CDS ISIMIP model metadata file
#------------------------------------------------------------------------------

df = pd.read_csv('OUT/cussh-hsi-regridded' + '-' + vartypestr + '-' + 'metadata.csv', index_col=0 )

variables = df.variable.unique()
projections = df.experiment.unique()
modellist = df.model.unique()
models = [ modellist[i].replace('-','_').lower() for i in range(len(modellist)) ]

#------------------------------------------------------------------------------
# LOAD: timeseries for each variable per projection for all models into separate dataframes
#------------------------------------------------------------------------------

filelist = sorted( glob.glob( modeldir + '*.nc' ), reverse = False )

#------------------------------------------------------------------------------
# RUN:
#------------------------------------------------------------------------------
 
# LOOP: over climate models

for c in range(len(cities)):

    city = cities[c]
    location_lat = location_lats[c]    
    location_lon = location_lons[c]    
                   
    for p in range(len(projections)):
 
        # INIT: standard dataframe for timeseries
             
        df = pd.DataFrame( {'datetimes':t_daily} )
        
        for f in range(len(filelist)):
                                                
            words = filelist[f].split('/')[2].split('_')
            parameter = words[0]
            projection = words[3]
            model = words[2]
        
            if (parameter == variables[0]) & (projection == projections[p]):
        
                ds = xr.open_dataset(filelist[f], decode_times=True)                    
                
                print(city, projection, model)
        
                t = pd.date_range(start=str(ds.time.dt.year[0].values+0), end=str(ds.time.dt.year[-1].values+0+1), freq='D')[0:-1]
                
                # EXTRACT: city gridcell timeseries (vectorized)
                '''
                first get lat,lon of nearest gridcell for first time step
                then vectorize using the nearest gridcell lat,lon
                '''

                '''
                n = 10
                t = t[0:n]
                ds_0 = ds[parameter][0,:,:].sel( lat = location_lat, lon = location_lon, method='nearest')        
                ts = [ ds[parameter][i,:,:].sel( lat = ds_0.lat.values + 0, lon = ds_0.lon.values + 0).values + 0 for i in range(n) ]
                '''
                
                ds_0 = ds[parameter][0,:,:].sel( lat = location_lat, lon = location_lon, method='nearest')        
                ts = [ ds[parameter][i,:,:].sel( lat = ds_0.lat.values + 0, lon = ds_0.lon.values + 0).values + 0 for i in range(len(ds[parameter])) ]
                
                if len(ts) != len(t):
         
                    t = ds.indexes['time'].to_datetimeindex() # for models with noleap calendars
                                                                                                              
                dv = pd.DataFrame( {'datetimes':t, model:ts} )    
                df = df.merge(dv, how='left', on='datetimes')
        
            else:
            
                continue
                                                            
        #------------------------------------------------------------------------------
        # CONVERT: to yearly values
        #------------------------------------------------------------------------------
        
        t_yearly = pd.date_range(start=str(year_start), end=str(year_end), freq='AS')
                
        df_1 = df[ df.iloc[:,1:] > threshold_1 ].groupby(df.datetimes.dt.year).count() # days in year above threshold    
        df_1 = df_1.reset_index(drop=True)            
        df_1['datetimes'] = t_yearly
        df_1 = df_1[ ['datetimes'] + [ col for col in df_1.columns if col != 'datetimes' ] ]            
        
        df_2 = df[ df.iloc[:,1:] > threshold_2 ].groupby(df.datetimes.dt.year).count() # days in year above threshold    
        df_2 = df_2.reset_index(drop=True)            
        df_2['datetimes'] = t_yearly
        df_2 = df_2[ ['datetimes'] + [ col for col in df_2.columns if col != 'datetimes' ] ]            
        
        df_3 = df[ df.iloc[:,1:] > threshold_3 ].groupby(df.datetimes.dt.year).count() # days in year above threshold    
        df_3 = df_3.reset_index(drop=True)            
        df_3['datetimes'] = t_yearly
        df_3 = df_3[ ['datetimes'] + [ col for col in df_3.columns if col != 'datetimes' ] ]            
        
        df_4 = df[ df.iloc[:,1:] > threshold_4 ].groupby(df.datetimes.dt.year).count() # days in year above threshold    
        df_4 = df_4.reset_index(drop=True)            
        df_4['datetimes'] = t_yearly
        df_4 = df_4[ ['datetimes'] + [ col for col in df_4.columns if col != 'datetimes' ] ]            
                        
        #------------------------------------------------------------------------------
        # SAVE: dataframes for each variable above threshold per projection for all models
        #------------------------------------------------------------------------------
                                    
        df_1.to_pickle( 'RUN/' + parameter + '_' + 'threshold1' + '-' + projections[p] + '_' + city + '.pkl', compression='bz2')
        df_2.to_pickle( 'RUN/' + parameter + '_' + 'threshold2' + '-' + projections[p] + '_' + city + '.pkl', compression='bz2')
        df_3.to_pickle( 'RUN/' + parameter + '_' + 'threshold3' + '-' + projections[p] + '_' + city + '.pkl', compression='bz2')
        df_4.to_pickle( 'RUN/' + parameter + '_' + 'threshold4' + '-' + projections[p] + '_' + city + '.pkl', compression='bz2')
                
#------------------------------------------------------------------------------
print('** END')


