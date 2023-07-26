#! /usr/bin python

#------------------------------------------------------------------------------
# PROGRAM: load-cussh-isimip-timeseries-combined.py
#------------------------------------------------------------------------------
# Version 0.3
# 26 July, 2023
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
import netCDF4

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

nsmooth = 30 # n-yr MA
year_start, year_end = 1850, 2100
 
fontsize = 12

#------------------------------------------------------------------------------
# LOAD: C3S CDS ISIMIP model metadata file
#------------------------------------------------------------------------------

di = pd.read_csv( 'OUT/cussh-isimip-regridded-metadata.csv', index_col=0 )
variables = di.variable.unique()
projections = di.experiment.unique()

#------------------------------------------------------------------------------
# LOAD: timeseries for each variable per projection for all models into separate dataframes
#------------------------------------------------------------------------------

modeldir = 'OUT/regridded-experiments/'
filelist = sorted( glob.glob( modeldir + '*.pkl' ), reverse = False )

for v in range(len(variables)):

    #------------------------------------------------------------------------------
    # LOAD: historical observations from JRA-55
    #------------------------------------------------------------------------------

    file_obs = 'DATA/jra55/' + variables[v] + '_yr_0.5deg_JRA55' + '.nc'    
    ds = xr.open_mfdataset( file_obs, decode_times = True)                
    
    t = pd.date_range(start=str(ds.time.dt.year[0].values+0), end=str(ds.time.dt.year[-1].values+0), freq='AS')
             
    parameter = variables[v]       
    if ( parameter == 'csdiETCCDI' ) | ( parameter == 'wsdiETCCDI' ):                    
        ts = ds[parameter].sel( lat = location_lat, lon = location_lon, method='nearest').values.astype('timedelta64[D]').astype(float)
    else:
        ts = ds[parameter].sel( lat = location_lat, lon = location_lon, method='nearest').values
                                
    ts[ts < -1.0e6] = np.nan
    ts[ts > 1.0e6] = np.nan
                    
    d_obs = pd.DataFrame( {'obs':ts}, index=t)    
    
    # SMOOTH: pad with window before and after obs and apply Gaussian filter
    
    idx_before = pd.date_range(d_obs.index[0]-pd.DateOffset(years=nsmooth), periods=nsmooth, freq='AS')[1:]             
    idx_after = pd.date_range(d_obs.index[-1], periods=nsmooth, freq='AS')[1:]             
    d_obs_window_before = pd.DataFrame( columns=d_obs.columns, index=idx_before )    
    d_obs_window_after = pd.DataFrame( columns=d_obs.columns, index=idx_after )    
    d_obs_window_before['obs'] = d_obs.obs.values[0]
    d_obs_window_after['obs'] = d_obs.obs.values[-1]
    d_obs_ext = pd.concat( [d_obs_window_before, d_obs, d_obs_window_after] ).rolling(nsmooth, center=True, win_type='gaussian').mean(std=3)        
    d_obs_smooth = d_obs_ext[ (d_obs_ext.index >= d_obs.index[0]) & (d_obs_ext.index <= d_obs.index[-1]) ]    
    
    # SAVE: dataframe for each variable per projection for all models
                            
    d_obs.to_pickle( 'RUN/' + variables[v] + '_' + 'jra55' '_' + city + '.pkl', compression='bz2')

    #------------------------------------------------------------------------------
    # LOAD: model runs for variable    
    #------------------------------------------------------------------------------

    df_historical = pd.read_pickle( 'OUT/regridded-experiments/' + variables[v] + '_' + 'historical' + '_' + city + '.pkl', compression='bz2' )
    df_ssp126 = pd.read_pickle( 'OUT/regridded-experiments/' + variables[v] + '_' + 'ssp126' + '_' + city + '.pkl', compression='bz2' )
    df_ssp245 = pd.read_pickle( 'OUT/regridded-experiments/' + variables[v] + '_' + 'ssp245' + '_' + city + '.pkl', compression='bz2' )
    df_ssp370 = pd.read_pickle( 'OUT/regridded-experiments/' + variables[v] + '_' + 'ssp370' + '_' + city + '.pkl', compression='bz2' )
    df_ssp585 = pd.read_pickle( 'OUT/regridded-experiments/' + variables[v] + '_' + 'ssp585' + '_' + city + '.pkl', compression='bz2' )

    #------------------------------------------------------------------------------
    # APPEND: historical to SSPs
    #------------------------------------------------------------------------------

    df_ssp126 = df_historical.combine_first(df_ssp126)
    df_ssp245 = df_historical.combine_first(df_ssp245)
    df_ssp370 = df_historical.combine_first(df_ssp370)
    df_ssp585 = df_historical.combine_first(df_ssp585)
                            
    #------------------------------------------------------------------------------
    # SAVE: historical + SSP dataframe for each variable
    #------------------------------------------------------------------------------
                    
    df_ssp126.to_pickle( variables[v] + '_' +'ssp126' + '_' + 'with_historical' + '_' + 'regridded' + '_' + city + '.pkl', compression='bz2')
    df_ssp245.to_pickle( variables[v] + '_' +'ssp245' + '_' + 'with_historical' + '_' +'regridded' + '_' + city + '.pkl', compression='bz2')
    df_ssp370.to_pickle( variables[v] + '_' +'ssp370' + '_' + 'with_historical' + '_' +'regridded' + '_' + city + '.pkl', compression='bz2')
    df_ssp585.to_pickle( variables[v] + '_' +'ssp585' + '_' + 'with_historical' + '_' +'regridded' + '_' + city + '.pkl', compression='bz2')
    
    #------------------------------------------------------------------------------
    # SMOOTH: using a Gaussian filter applied to padded data with MA applied
    #------------------------------------------------------------------------------

    df_ssp126 = df_ssp126.copy().set_index('datetimes')
    df_ssp245 = df_ssp245.copy().set_index('datetimes')                   
    df_ssp370 = df_ssp370.copy().set_index('datetimes')                   
    df_ssp585 = df_ssp585.copy().set_index('datetimes')                   

    idx = pd.date_range(df_ssp126.index[-1], periods=nsmooth, freq='AS')[1:]
    df_ssp126_window = pd.DataFrame( columns=df_ssp126.columns, index=idx )
    df_ssp245_window = pd.DataFrame( columns=df_ssp245.columns, index=idx )
    df_ssp370_window = pd.DataFrame( columns=df_ssp370.columns, index=idx )
    df_ssp585_window = pd.DataFrame( columns=df_ssp585.columns, index=idx )

    df_ssp126_window.iloc[:,:] = np.tile( df_ssp126.iloc[-1,:].values, [len(idx),1])
    df_ssp245_window.iloc[:,:] = np.tile( df_ssp245.iloc[-1,:].values, [len(idx),1])
    df_ssp370_window.iloc[:,:] = np.tile( df_ssp370.iloc[-1,:].values, [len(idx),1])
    df_ssp585_window.iloc[:,:] = np.tile( df_ssp585.iloc[-1,:].values, [len(idx),1])

    df_ssp126_ext = pd.concat( [df_ssp126, df_ssp126_window] )
    df_ssp245_ext = pd.concat( [df_ssp245, df_ssp245_window] )
    df_ssp370_ext = pd.concat( [df_ssp370, df_ssp370_window] )
    df_ssp585_ext = pd.concat( [df_ssp585, df_ssp585_window] )

    df_ssp126_p05 = df_ssp126_ext.quantile(q=0.05, axis=1, numeric_only=False, interpolation='linear', method='single').rolling(nsmooth, center=True, win_type='gaussian').mean(std=3)
    df_ssp245_p05 = df_ssp245_ext.quantile(q=0.05, axis=1, numeric_only=False, interpolation='linear', method='single').rolling(nsmooth, center=True, win_type='gaussian').mean(std=3)
    df_ssp370_p05 = df_ssp370_ext.quantile(q=0.05, axis=1, numeric_only=False, interpolation='linear', method='single').rolling(nsmooth, center=True, win_type='gaussian').mean(std=3)
    df_ssp585_p05 = df_ssp585_ext.quantile(q=0.05, axis=1, numeric_only=False, interpolation='linear', method='single').rolling(nsmooth, center=True, win_type='gaussian').mean(std=3)

    df_ssp126_p50 = df_ssp126_ext.quantile(q=0.5, axis=1, numeric_only=False, interpolation='linear', method='single').rolling(nsmooth, center=True, win_type='gaussian').mean(std=3)
    df_ssp245_p50 = df_ssp245_ext.quantile(q=0.5, axis=1, numeric_only=False, interpolation='linear', method='single').rolling(nsmooth, center=True, win_type='gaussian').mean(std=3)
    df_ssp370_p50 = df_ssp370_ext.quantile(q=0.5, axis=1, numeric_only=False, interpolation='linear', method='single').rolling(nsmooth, center=True, win_type='gaussian').mean(std=3)
    df_ssp585_p50 = df_ssp585_ext.quantile(q=0.5, axis=1, numeric_only=False, interpolation='linear', method='single').rolling(nsmooth, center=True, win_type='gaussian').mean(std=3)

    df_ssp126_p95 = df_ssp126_ext.quantile(q=0.95, axis=1, numeric_only=False, interpolation='linear', method='single').rolling(nsmooth, center=True, win_type='gaussian').mean(std=3)
    df_ssp245_p95 = df_ssp245_ext.quantile(q=0.95, axis=1, numeric_only=False, interpolation='linear', method='single').rolling(nsmooth, center=True, win_type='gaussian').mean(std=3)
    df_ssp370_p95 = df_ssp370_ext.quantile(q=0.95, axis=1, numeric_only=False, interpolation='linear', method='single').rolling(nsmooth, center=True, win_type='gaussian').mean(std=3)
    df_ssp585_p95 = df_ssp585_ext.quantile(q=0.95, axis=1, numeric_only=False, interpolation='linear', method='single').rolling(nsmooth, center=True, win_type='gaussian').mean(std=3)
                
    dg_ssp126 = df_ssp126_ext.copy().rolling(nsmooth, center=True).mean() 
    dg_ssp245 = df_ssp245_ext.copy().rolling(nsmooth, center=True).mean()                   
    dg_ssp370 = df_ssp370_ext.copy().rolling(nsmooth, center=True).mean()                   
    dg_ssp585 = df_ssp585_ext.copy().rolling(nsmooth, center=True).mean()                   

    #------------------------------------------------------------------------------
    # PLOT
    #------------------------------------------------------------------------------

     #colors = plt.cm.viridis(np.linspace(0,1,len(dg.columns)))
            
    figstr = variables[v] + '_' + 'SSPs_with_historical' + '_' + 'regridded' + '_' + city + '.png'
    titlestr = 'ISIMIP CMIP6 models (regridded to 0.5 degrees): ' + variables[v] + ' (' + str(nsmooth) + '-yr MA)'  + ': ' + city + ' (' + str(np.round(location_lat,3)) + '°N,' + str(np.round(location_lon,3)) + '°E)'
                    
    fig, ax = plt.subplots(figsize=(15,10))     
    #for i in range(len(dg.columns)): plt.plot(dg.index, dg[dg.columns[i]].values, color=colors[i], lw=1, label=dg.columns[i], zorder=1)    
    for i in range(len(dg_ssp126.columns)): plt.plot(dg_ssp126[dg_ssp126.index.year<=2015].index, dg_ssp126[dg_ssp126.index.year<=2015][dg_ssp126.columns[i]].values, color='grey', lw=1, zorder=1)    
    for i in range(len(dg_ssp126.columns)): plt.plot(dg_ssp126[dg_ssp126.index.year>=2015].index, dg_ssp126[dg_ssp126.index.year>=2015][dg_ssp126.columns[i]].values, color='lime', lw=1, zorder=2)    
    for i in range(len(dg_ssp370.columns)): plt.plot(dg_ssp370[dg_ssp370.index.year>=2015].index, dg_ssp370[dg_ssp370.index.year>=2015][dg_ssp370.columns[i]].values, color='orange', lw=1, zorder=2)    
    
    plt.fill_between(df_ssp126_p05[df_ssp126_p05.index.year<=2015].index, df_ssp126_p05[df_ssp126_p05.index.year<=2015].values, df_ssp126_p95[df_ssp126_p95.index.year<=2015].values, color='lightgrey', edgecolor="black", linewidth=0.0, alpha=0.5, label='Historical (5-95% CI)', zorder=11)                
    plt.fill_between(df_ssp126_p05[df_ssp126_p05.index.year>=2015].index, df_ssp126_p05[df_ssp126_p05.index.year>=2015].values, df_ssp126_p95[df_ssp126_p95.index.year>=2015].values, color='lime', edgecolor="green", linewidth=0.0, alpha=0.5, label='SSP1-2.6 (5-95% CI)',zorder=12)
    plt.fill_between(df_ssp370_p05[df_ssp370_p05.index.year>=2015].index, df_ssp370_p05[df_ssp370_p05.index.year>=2015].values, df_ssp370_p95[df_ssp370_p95.index.year>=2015].values, color='orange', edgecolor="red", linewidth=0.0, alpha=0.5, label='SSP3-7.0 (5-95% CI)',zorder=12)

    plt.plot(df_ssp126_p05[df_ssp126_p05.index.year<=2015].index, df_ssp126_p05[df_ssp126_p05.index.year<=2015].values, color='black', alpha=0.5, lw=3, zorder=101)
    plt.plot(df_ssp126_p50[df_ssp126_p50.index.year<=2015].index, df_ssp126_p50[df_ssp126_p50.index.year<=2015].values, color='black', lw=3, zorder=101)
    plt.plot(df_ssp126_p95[df_ssp126_p95.index.year<=2015].index, df_ssp126_p95[df_ssp126_p95.index.year<=2015].values, color='black', alpha=0.5, lw=3, zorder=101)

    plt.plot(df_ssp126_p05[df_ssp126_p05.index.year>=2015].index, df_ssp126_p05[df_ssp126_p05.index.year>=2015].values, color='green', alpha=0.5, lw=3, zorder=102)
    plt.plot(df_ssp126_p50[df_ssp126_p50.index.year>=2015].index, df_ssp126_p50[df_ssp126_p50.index.year>=2015].values, color='green', lw=3, zorder=102)
    plt.plot(df_ssp126_p95[df_ssp126_p95.index.year>=2015].index, df_ssp126_p95[df_ssp126_p95.index.year>=2015].values, color='green', alpha=0.5, lw=3, zorder=102)

    plt.plot(df_ssp370_p05[df_ssp370_p05.index.year>=2015].index, df_ssp370_p05[df_ssp126_p05.index.year>=2015].values, color='red', alpha=0.5, lw=3, zorder=102)
    plt.plot(df_ssp370_p50[df_ssp370_p50.index.year>=2015].index, df_ssp370_p50[df_ssp126_p50.index.year>=2015].values, color='red', lw=3, zorder=102)
    plt.plot(df_ssp370_p95[df_ssp370_p95.index.year>=2015].index, df_ssp370_p95[df_ssp126_p95.index.year>=2015].values, color='red', alpha=0.5, lw=3, zorder=102)

    plt.plot(d_obs.index, d_obs.obs, color='blue', alpha=0.5, lw=1, label='JRA-55', zorder=1001)
    plt.plot(d_obs_smooth.index, d_obs_smooth.obs, color='blue', alpha=1, lw=3, zorder=1002)

    ax.set_axisbelow(True)
    ax.xaxis.grid(color='gray', linestyle='dashed')
    ax.yaxis.grid(color='gray', linestyle='dashed')

    plt.xlim( pd.to_datetime('1900', format='%Y'), pd.to_datetime('2100', format='%Y'))
    ax.set_xticks( pd.date_range( start=str(1900), end=str(2100), freq='10AS') )
    ax.set_xticklabels([ '1900','','','','','1950','','','','','2000','','','','','2050','','','','','2100'  ])

    if variables[v] == 'csdiETCCDI': ystr = 'csdiETCCDI, [days]'; ax.set_ylim(0,50)
    elif variables[v] == 'wsdiETCCDI': ystr = 'wsdiETCCDI, [days]'; ax.set_ylim(0,365)
    elif variables[v] == 'tn10pETCCDI': ystr = 'tn10pETCCDI, [%] of days'; ax.set_ylim(0,50)
    elif variables[v] == 'tn90pETCCDI': ystr = 'tn90pETCCDI, [%] of days'; ax.set_ylim(0,100)
    elif variables[v] == 'tx10pETCCDI': ystr = 'tx10pETCCDI, [%] of days'; ax.set_ylim(0,50)
    elif variables[v] == 'tx90pETCCDI': ystr = 'tx90pETCCDI, [%] of days'; ax.set_ylim(0,100)
    elif variables[v] == 'r95pETCCDI': ystr = 'r95pETCCDI, [mm]'; ax.set_ylim(0,1000)
    elif variables[v] == 'r99pETCCDI': ystr = 'r99pETCCDI, [mm]'; ax.set_ylim(0,500)

    plt.ylabel(ystr, fontsize=fontsize)

    plt.legend(loc='upper left', markerscale=1, ncol=1, facecolor='white', framealpha=0.9, fontsize=10)    
    plt.tick_params(labelsize=fontsize)    
    plt.title(titlestr, fontsize=fontsize)
    plt.savefig(figstr, dpi=300, bbox_inches='tight')
    plt.close('all')
                
#------------------------------------------------------------------------------
print('** END')

    
