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

# Plotting libraries:
import matplotlib.pyplot as plt; plt.close('all')
from pandas.plotting import register_matplotlib_converters
from matplotlib import rcParams
register_matplotlib_converters()
import matplotlib.dates as mdates
#import seaborn as sns; sns.set()

#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# SETTINGS: 
#------------------------------------------------------------------------------

city, location_lat, location_lon = 'London', 51.5, -0.1
#city, location_lat, location_lon = 'Rennes', 48.1, -1.7
#city, location_lat, location_lon = 'Kisumu', -0.1, 34.8
#city, location_lat, location_lon = 'Nairobi', -1.3, 36.8
#city, location_lat, location_lon = 'Homa', -0.5, 34.5
#city, location_lat, location_lon = 'Beijing', 39.9, 116.4
#city, location_lat, location_lon = 'Ningbo', 29.9, 121.6

use_tas = True 			# [True (default), False=pr]

if use_tas == True:
    vartypestr = 'regridded-tas-monthly'
else:
    vartypestr = 'regridded-pr-monthly'

modeldir = 'DATA/' + vartypestr + '/'

year_start, year_end = 1850, 2100
 
# PLOT PARAMETERS (only)

plot_experiment = True # [True, False (default) ]
fontsize = 12
nsmooth = 30 # n-yr MA

#------------------------------------------------------------------------------
# LOAD: C3S CDS ISIMIP model metadata file
#------------------------------------------------------------------------------

df = pd.read_csv( 'OUT/cussh-cmip6' + '-' + vartypestr + '-' + 'metadata.csv', index_col=0 )
dh = pd.read_csv( 'OUT/cussh-cmip6' + '-' + vartypestr + '-' + 'counts.csv', index_col=0 )

di = df.copy()

variables = di.variable.unique()
projections = di.experiment.unique()
modellist = di.model.unique()
models = [ modellist[i].replace('-','_').lower() for i in range(len(modellist)) ]

#------------------------------------------------------------------------------
# LOAD: timeseries for each variable per projection for all models into separate dataframes
#------------------------------------------------------------------------------

filelist = sorted( glob.glob( modeldir + '*.nc' ), reverse = False )

for v in range(len(variables)):

    for p in range(len(projections)):                        

        # INIT: standard dataframe for timeseries
    
        t = pd.date_range(start=str(year_start), end=str(year_end), freq='MS')

        df = pd.DataFrame( {'datetimes':t} )
                   
        for f in range(len(filelist)):
                                        
            words = filelist[f].split('/')[2].split('_')
            parameter = words[0]
            projection = words[3]
            model = words[2]
                            
            if ( parameter == variables[v] ) & ( projection == projections[p] ):
    
                # EXTRACT: timeseries at location and append to dataframe
            
                try:                    

                    ds = xr.open_dataset( filelist[f], decode_times=True )                

                except:

                    ds = xr.open_mfdataset( filelist[f], coords="minimal", decode_times = False, use_cftime=True)                
                    units, reference_date = ds.time.attrs['units'].split('since')
                    ds['time'] = pd.date_range(start=reference_date, periods=ds.sizes['time'], freq='MS')                

                t = pd.date_range(start=str(ds.time.dt.year[0].values+0), end=str(ds.time.dt.year[-1].values+0+1), freq='MS')[0:-1]
                ts = ds[parameter].sel( lat = location_lat, lon = location_lon, method='nearest').values
                                  
                if use_tas == True: ts = ts - 273.15
                    
                dv = pd.DataFrame( {'datetimes':t, model:ts} )    
                df = df.merge(dv, how='left', on='datetimes')
                        
        #------------------------------------------------------------------------------
        # CONVERT: to yearly values
        #------------------------------------------------------------------------------

        t_yearly = pd.date_range(start=str(year_start), end=str(year_end), freq='AS')
        
        if use_tas == True:

            df = df.groupby(df.datetimes.dt.year).mean() # tas yearly mean           
            df = df.reset_index(drop=True)            
            df['datetimes'] = t_yearly
            df = df[ ['datetimes'] + [ col for col in df.columns if col != 'datetimes' ] ]            
            
        else:
            
            df = df.groupby(df.datetimes.dt.year).sum() * (60*60*24*30)  # pr yearly total flux (mm/s) * 360 day/yr
            df = df.reset_index(drop=True)            
            df['datetimes'] = t_yearly
            df = df[ ['datetimes'] + [ col for col in df.columns if col != 'datetimes' ] ]            
            
        #------------------------------------------------------------------------------
        # SAVE: dataframe for each variable per projection for all models
        #------------------------------------------------------------------------------
                            
        df.to_pickle( 'RUN/' + variables[v] + '_' + projections[p] + '_' + city + '.pkl', compression='bz2')

        if plot_experiment == True:

            #------------------------------------------------------------------------------
            # PLOT
            #------------------------------------------------------------------------------
                    
            dg = df.copy().set_index('datetimes').rolling(nsmooth, center=True).mean()                   
            colors = plt.cm.viridis(np.linspace(0,1,len(dg.columns)))
    
            figstr = variables[v] + '_' + projections[p] + '_' + 'regridded' + '_' + city + '.png'
            titlestr = 'ISIMIP CMIP6 models (regridded to 0.5 degrees): ' + variables[v] + ': ' + projections[p] + ' (' + str(nsmooth) + '-yr MA)'  + ': ' + city + ' (' + str(np.round(location_lat,3)) + '°N,' + str(np.round(location_lon,3)) + '°E)'
                        
            fig, ax = plt.subplots(figsize=(15,10))     
            for i in range(len(dg.columns)): plt.plot(dg.index, dg[dg.columns[i]].values, color=colors[i], lw=1, label=dg.columns[i], zorder=1)    
        
            plt.fill_between(dg.index, np.nanpercentile(dg, 2.5, axis=1), np.nanpercentile(dg, 97.5, axis=1), color='black', edgecolor="black", linewidth=0.0, alpha=0.025, label='2.5-97.5% C.I.', zorder=11)                
            plt.fill_between(dg.index, np.nanpercentile(dg, 5, axis=1), np.nanpercentile(dg, 95, axis=1), color='black', edgecolor="black", linewidth=0.0, alpha=0.05, label='5-95% C.I.', zorder=12)                
            plt.fill_between(dg.index, np.nanpercentile(dg, 10, axis=1), np.nanpercentile(dg, 90, axis=1), color='black', edgecolor="black", linewidth=0.0, alpha=0.1, label='10-90% C.I.', zorder=13)                
            plt.fill_between(dg.index, np.nanpercentile(dg, 25, axis=1), np.nanpercentile(dg, 75, axis=1), color='black', edgecolor="black", linewidth=0.0, alpha=0.2, label='25-75% C.I.', zorder=14)                
            plt.fill_between([0,1],[0,1], color="none", hatch="X", edgecolor="b", linewidth=0.0)
            plt.plot(dg.index, np.nanpercentile(dg, 50,axis=1), color='black', lw=3, label='Median')
    
            plt.xlim( pd.to_datetime('1850', format='%Y'), pd.to_datetime('2100', format='%Y'))
            plt.xlabel('Year', fontsize=fontsize)
            plt.ylabel('Value', fontsize=fontsize)
    
            fig.legend(loc='lower left', bbox_to_anchor=(0.1, -0.1), markerscale=1, ncol=6, facecolor='white', framealpha=0.9, fontsize=10)    
    
            plt.tick_params(labelsize=fontsize)    
            plt.title(titlestr, fontsize=fontsize)
            plt.savefig(figstr, dpi=300, bbox_inches='tight')
            plt.close('all')
                
#------------------------------------------------------------------------------
print('** END')

    
