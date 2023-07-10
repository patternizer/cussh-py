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

location_lat, location_lon = -1.28638, 36.817222 # Nairobi
year_start, year_end = 1850, 2100
 
fontsize = 12

#------------------------------------------------------------------------------
# LOAD: C3S CDS ISIMIP model metadata file
#------------------------------------------------------------------------------

di = pd.read_csv( 'cussh-isimip-metadata.csv', index_col=0 )
variables = di.variable.unique()
projections = di.experiment.unique()
modellist = di.model.unique()
models = [ modellist[i].replace('-','_').lower() for i in range(len(modellist)) ]

#------------------------------------------------------------------------------
# LOAD: timeseries for each variable per projection for all models into separate dataframes
#------------------------------------------------------------------------------

filelist = []
for m in range(len(models)):      
         
    modeldir = 'DATA/' + models[m] + '/'
    filesdir = sorted( glob.glob( modeldir + '*.nc' ), reverse = False )
    filelist = filelist + list(filesdir)

for v in range(len(variables)):

    for p in range(len(projections)):                        

        # INIT: standard dataframe for timeseries
        
        t = pd.date_range(start=str(year_start), end=str(year_end), freq='AS')
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
                    ds['time'] = pd.date_range(start=reference_date, periods=ds.sizes['time'], freq='AS')                

                t = pd.date_range(start=str(ds.time.dt.year[0].values+0), end=str(ds.time.dt.year[-1].values+0), freq='AS')
                    
                if ( parameter == 'csdiETCCDI' ) | ( parameter == 'wsdiETCCDI' ):                    
                    ts = ds[parameter].sel( lat = location_lat, lon = location_lon, method='nearest').values.astype('timedelta64[D]').astype(float)
                else:
                    ts = ds[parameter].sel( lat = location_lat, lon = location_lon, method='nearest').values
                                
                ts[ts < -1.0e6] = np.nan
                ts[ts > 1.0e6] = np.nan
                    
                dv = pd.DataFrame( {'datetimes':t, model:ts} )    
                df = df.merge(dv, how='left', on='datetimes')
                
        #------------------------------------------------------------------------------
        # SAVE: dataframe for each variable per projection for all models
        #------------------------------------------------------------------------------
                    
        df.to_pickle( 'RUN/' + variables[v] + '_' + projections[p] + '.pkl', compression='bz2')

        #------------------------------------------------------------------------------
        # PLOT
        #------------------------------------------------------------------------------
        
        dg = df.copy().set_index('datetimes').rolling(10, center=True).mean()                   
        colors = plt.cm.viridis(np.linspace(0,1,len(dg.columns)))

        figstr = variables[v] + '_' + projections[p] + '.png'
        titlestr = 'ISIMIP CMIP6 models: ' + variables[v] + ': ' + projections[p] + ' (10-yr MA)'
                
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

    
