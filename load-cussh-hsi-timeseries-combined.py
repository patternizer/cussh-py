#! /usr/bin python

#------------------------------------------------------------------------------
# PROGRAM: load-cussh-hsi-timeseries-combined.py
#------------------------------------------------------------------------------
# Version 0.1
# 24 September, 2023
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

# Silence library version notifications
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")

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

vartypestr = 'regridded-hi-daily'
#vartypestr = 'regridded-humindex-daily'
#vartypestr = 'regridded-utci-daily'
#vartypestr = 'regridded-wbgt-daily'
#vartypestr = 'regridded-wbt-daily'

thresholds = [ 'threshold1', 'threshold2', 'threshold3', 'threshold4' ]
        
if vartypestr == 'regridded-hi-daily':
            
    threshold_1 = 27.0
    threshold_2 = 32.0
    threshold_3 = 41.0
    threshold_4 = 54.0    
    thresholdsstr = [ 'hi27', 'hi32', 'hi41', 'hi54' ]

elif vartypestr == 'regridded-humindex-daily':
            
    threshold_1 = 30.0
    threshold_2 = 40.0
    threshold_3 = 45.0
    threshold_4 = 54.0
    thresholdsstr = [ 'humindex30', 'humindex40', 'humindex45', 'humindex54' ]

elif vartypestr == 'regridded-utci-daily':
            
    threshold_1 = 26.0
    threshold_2 = 32.0
    threshold_3 = 38.0
    threshold_4 = 46.0
    thresholdsstr = [ 'utci26', 'utci32', 'utci38', 'utci46' ]

elif vartypestr == 'regridded-wbgt-daily':
            
    threshold_1 = 29.0
    threshold_2 = 30.5
    threshold_3 = 32.0
    threshold_4 = 37.0
    thresholdsstr = [ 'wbgt29', 'wbgt30_5', 'wbgt32', 'wbgt37' ]
            
elif vartypestr == 'regridded-wbt-daily':
            
    threshold_1 = np.nan
    threshold_2 = np.nan
    threshold_3 = np.nan
    threshold_4 = 35.0
    thresholdsstr = [ 'wbt_NaN', 'wbt_NaN', 'wbt_NaN', 'wbt_35' ]
    
modeldir = 'RUN/'

nsmooth = 30 # n-yr MA
year_start, year_end = 1951, 2100
 
fontsize = 12

#------------------------------------------------------------------------------
# LOAD: C3S CDS ISIMIP model metadata file
#------------------------------------------------------------------------------

di = pd.read_csv( 'OUT/cussh-hsi' + '-' + vartypestr + '-' + 'metadata.csv', index_col=0 )

variables = di.variable.unique()
projections = di.experiment.unique()

#------------------------------------------------------------------------------
# LOAD: timeseries for each variable per projection for all models into separate dataframes
#------------------------------------------------------------------------------

filelist = sorted( glob.glob( modeldir + '*.pkl' ), reverse = False )

#------------------------------------------------------------------------------
# INITIALISE: summary statistics matrices
#------------------------------------------------------------------------------

model_summary_stats_matrix = []

for v in range(len(variables)):

    for j in range(len(thresholds)):
        
        print(v,j)
        
        threshold = thresholds[j]

        parameter = variables[v]
                                            
        #------------------------------------------------------------------------------
        # CONSTRUCT: observations dataframe (NB: no obs so set to NaN)
        #------------------------------------------------------------------------------
    
        t = pd.date_range(start=str(year_start), end=str(year_end), freq='AS')
        ts = [np.nan] * len(t)             
        d_obs = pd.DataFrame( {'obs':ts}, index=t)    
            
        #------------------------------------------------------------------------------
        # SMOOTH: pad with window before and after obs and apply Gaussian filter
        #------------------------------------------------------------------------------
        
        idx_before = pd.date_range(d_obs.index[0]-pd.DateOffset(years=int(nsmooth/2)), periods=int(nsmooth/2), freq='AS')[1:]             
        idx_after = pd.date_range(d_obs.index[-1], periods=int(nsmooth/2), freq='AS')[1:]             
        d_obs_window_before = pd.DataFrame( columns=d_obs.columns, index=idx_before )    
        d_obs_window_after = pd.DataFrame( columns=d_obs.columns, index=idx_after )    
        window_before_mean = np.nanmean( d_obs.obs.values[0:int(nsmooth/2)-1] )
        window_after_mean = np.nanmean( d_obs.obs.values[-int(nsmooth/2):] )
        d_obs_window_before['obs'] = window_before_mean
        d_obs_window_after['obs'] = window_after_mean
        d_obs_ext = pd.concat( [d_obs_window_before, d_obs, d_obs_window_after] ).rolling(nsmooth, center=True, win_type='gaussian').mean(std=3)        
        d_obs_smooth = d_obs_ext[ (d_obs_ext.index >= d_obs.index[0]) & (d_obs_ext.index <= d_obs.index[-1]) ]    
        
        #------------------------------------------------------------------------------
        # SAVE: raw obs dataframe to .pkl
        #------------------------------------------------------------------------------
                                
        d_obs.to_pickle( 'RUN/' + variables[v].lower() + 'ETCCDI' + '_' + 'obs' '_' + city + '.pkl', compression='bz2')
    
        #------------------------------------------------------------------------------
        # TRIM: obs to start of SSP
        #------------------------------------------------------------------------------
    
        d_obs = d_obs[d_obs.index.year <= 2011]
        d_obs_smooth = d_obs_smooth[d_obs_smooth.index.year <= 2011]
    
        #------------------------------------------------------------------------------
        # LOAD: model runs for variable    
        #------------------------------------------------------------------------------
    
        df_historical_in = pd.read_pickle( 'RUN/' + parameter + '_' + threshold + '_' + 'historical' + '_' + city + '.pkl', compression='bz2' )
        df_ssp126_in = pd.read_pickle( 'RUN/' + parameter + '_' + threshold + '_' + 'ssp126' + '_' + city + '.pkl', compression='bz2' )
        df_ssp370_in = pd.read_pickle( 'RUN/' + parameter + '_' + threshold + '_' + 'ssp370' + '_' + city + '.pkl', compression='bz2' )
    
        #------------------------------------------------------------------------------
        # TRIM: model runs to ISIMIP datetime range
        #------------------------------------------------------------------------------

        df_historical = df_historical_in[ (df_historical_in['datetimes'].dt.year>=year_start) ].reset_index(drop=True)
        df_ssp126 = df_ssp126_in[ (df_ssp126_in['datetimes'].dt.year>=year_start) ].reset_index(drop=True)
        df_ssp370 = df_ssp370_in[ (df_ssp370_in['datetimes'].dt.year>=year_start) ].reset_index(drop=True)
    
        df_historical_trimmed = df_historical[ df_historical['datetimes'].dt.year<=2010 ]
        df_ssp126_trimmed = df_ssp126[ (df_ssp126['datetimes'].dt.year>=2011) & (df_ssp126['datetimes'].dt.year<=2100)]
        df_ssp370_trimmed = df_ssp370[ (df_ssp370['datetimes'].dt.year>=2011) & (df_ssp370['datetimes'].dt.year<=2100)]
        
        #------------------------------------------------------------------------------
        # SET: minmax for day parameters
        #------------------------------------------------------------------------------
        
        df_historical_trimmed.iloc[:,1:] = df_historical_trimmed.iloc[:,1:].clip(lower=0, upper=365)
        df_ssp126_trimmed.iloc[:,1:] = df_ssp126_trimmed.iloc[:,1:].clip(lower=0, upper=365)
        df_ssp370_trimmed.iloc[:,1:] = df_ssp370_trimmed.iloc[:,1:].clip(lower=0, upper=365)

        #------------------------------------------------------------------------------
        # COMPUTE: summary statistics
        #------------------------------------------------------------------------------
    
        def calc_stats( baseline_start, baseline_end, d_obs, df_historical, df_ssp126, df_ssp370 ):
    
            obs_mean = np.nanmean( d_obs[ (d_obs.index.year >= baseline_start) & (d_obs.index.year <= baseline_end) ].reset_index(drop=True) )
            obs_p05 = d_obs[ (d_obs.index.year >= baseline_start) & (d_obs.index.year <= baseline_end) ].reset_index(drop=True).quantile(q=0.05, axis=0, numeric_only=True, interpolation='linear', method='single').mean(numeric_only=True)
            obs_p95 = d_obs[ (d_obs.index.year >= baseline_start) & (d_obs.index.year <= baseline_end) ].reset_index(drop=True).quantile(q=0.95, axis=0, numeric_only=True, interpolation='linear', method='single').mean(numeric_only=True)
        
            historical_mean = np.nanmean( df_historical[ (df_historical.datetimes.dt.year >= baseline_start) & (df_historical.datetimes.dt.year <= baseline_end) ].mean(numeric_only=True) )
            historical_p05 = np.nanmean( df_historical[ (df_historical.datetimes.dt.year >= baseline_start) & (df_historical.datetimes.dt.year <= baseline_end) ].iloc[:,1:].quantile(q=0.05, axis=0, numeric_only=True, interpolation='linear', method='single').mean(numeric_only=True) )
            historical_p95 = np.nanmean( df_historical[ (df_historical.datetimes.dt.year >= baseline_start) & (df_historical.datetimes.dt.year <= baseline_end) ].iloc[:,1:].quantile(q=0.95, axis=0, numeric_only=True, interpolation='linear', method='single').mean(numeric_only=True) )
        
            ssp126_mean = np.nanmean( df_ssp126[ (df_ssp126.datetimes.dt.year >= baseline_start) & (df_ssp126.datetimes.dt.year <= baseline_end) ].mean(numeric_only=True) )
            ssp126_p05 = np.nanmean( df_ssp126[ (df_ssp126.datetimes.dt.year >= baseline_start) & (df_ssp126.datetimes.dt.year <= baseline_end) ].iloc[:,1:].quantile(q=0.05, axis=0, numeric_only=True, interpolation='linear', method='single').mean(numeric_only=True) )
            ssp126_p95 = np.nanmean( df_ssp126[ (df_ssp126.datetimes.dt.year >= baseline_start) & (df_ssp126.datetimes.dt.year <= baseline_end) ].iloc[:,1:].quantile(q=0.95, axis=0, numeric_only=True, interpolation='linear', method='single').mean(numeric_only=True) )
        
            ssp370_mean = np.nanmean( df_ssp370[ (df_ssp370.datetimes.dt.year >= baseline_start) & (df_ssp370.datetimes.dt.year <= baseline_end) ].mean(numeric_only=True) )
            ssp370_p05 = np.nanmean( df_ssp370[ (df_ssp370.datetimes.dt.year >= baseline_start) & (df_ssp370.datetimes.dt.year <= baseline_end) ].iloc[:,1:].quantile(q=0.05, axis=0, numeric_only=True, interpolation='linear', method='single').mean(numeric_only=True) )
            ssp370_p95 = np.nanmean( df_ssp370[ (df_ssp370.datetimes.dt.year >= baseline_start) & (df_ssp370.datetimes.dt.year <= baseline_end) ].iloc[:,1:].quantile(q=0.95, axis=0, numeric_only=True, interpolation='linear', method='single').mean(numeric_only=True) )
            
            return obs_mean, obs_p05, obs_p95, historical_mean, historical_p05, historical_p95, ssp126_mean, ssp126_p05, ssp126_p95, ssp370_mean, ssp370_p05, ssp370_p95
    
        baseline_start_vec = [1961,1971,1981,2021,2035,2071]
        baseline_end_vec = [1990,2000,2010,2050,2064,2100]
    
        model_summary_stats_vec = []
        for b in range(len(baseline_start_vec)):
    
            baseline_start = baseline_start_vec[b] 
            baseline_end = baseline_end_vec[b] 
            obs_mean, obs_p05, obs_p95, historical_mean, historical_p05, historical_p95, ssp126_mean, ssp126_p05, ssp126_p95, ssp370_mean, ssp370_p05, ssp370_p95 = calc_stats( baseline_start, baseline_end, d_obs, df_historical_trimmed, df_ssp126_trimmed, df_ssp370_trimmed )        
            model_summary_stats_vec = model_summary_stats_vec + list([ obs_mean, obs_p05, obs_p95, historical_mean, historical_p05, historical_p95, ssp126_mean, ssp126_p05, ssp126_p95, ssp370_mean, ssp370_p05, ssp370_p95 ])
            
        model_summary_stats_matrix.append( model_summary_stats_vec )
    
        #------------------------------------------------------------------------------
        # APPEND: historical to SSPs
        #------------------------------------------------------------------------------
        
        cols = df_historical_trimmed.columns
        df_ssp126_combined = pd.DataFrame( columns = cols )
        df_ssp370_combined = pd.DataFrame( columns = cols )
        for i in range( len( cols ) ):
 
            df_ssp126_combined[cols[i]] = np.array( list( df_historical_trimmed[cols[i]].values ) + list( df_ssp126_trimmed[cols[i]].values ) ).ravel()
            df_ssp370_combined[cols[i]] = np.array( list( df_historical_trimmed[cols[i]].values ) + list( df_ssp370_trimmed[cols[i]].values ) ).ravel()
                        
        #df_ssp126_combined = df_historical_trimmed.combine_first(df_ssp126_trimmed)
        #df_ssp370_combined = df_historical_trimmed.combine_first(df_ssp370_trimmed)
    
        #------------------------------------------------------------------------------
        # SAVE: historical + SSP dataframe for each variable (bias-adjusted)
        #------------------------------------------------------------------------------
                        
        df_ssp126_combined.to_pickle( 'OUT/' + parameter + '_' + threshold + '_' +'ssp126' + '_' + 'with_historical' + '_' + city + '.pkl', compression='bz2')
        df_ssp370_combined.to_pickle( 'OUT/' + parameter + '_' + threshold + '_' +'ssp370' + '_' + 'with_historical' + '_' + city + '.pkl', compression='bz2')
        
        #------------------------------------------------------------------------------
        # SMOOTH: using a Gaussian filter applied to padded data with MA applied (NB: after window is extended by +1 to take fit from 2099 to 2100)
        #------------------------------------------------------------------------------
    
        df_ssp126 = df_ssp126_combined.copy().set_index('datetimes')
        df_ssp370 = df_ssp370_combined.copy().set_index('datetimes')                   
                             
        idx_before = pd.date_range(df_ssp126.index[0]-pd.DateOffset(years=int(nsmooth/2)), periods=int(nsmooth/2), freq='AS')[1:]             
        idx_after = pd.date_range(df_ssp126.index[-1], periods=int(nsmooth/2)+1, freq='AS')[1:]             
        df_ssp126_window_before = pd.DataFrame( columns=df_ssp126.columns, index=idx_before )    
        df_ssp126_window_after = pd.DataFrame( columns=df_ssp126.columns, index=idx_after )    
        window_before_mean = np.nanmean( df_ssp126[0:int(nsmooth/2)-1], axis=0 )
        window_after_mean = np.nanmean( df_ssp126[-int(nsmooth/2):], axis=0 )
        df_ssp126_window_before.iloc[:,:]  = np.tile( window_before_mean, [len(idx_before),1])
        df_ssp126_window_after.iloc[:,:]  = np.tile( window_after_mean, [len(idx_after),1])
    
        idx_before = pd.date_range(df_ssp370.index[0]-pd.DateOffset(years=int(nsmooth/2)), periods=int(nsmooth/2), freq='AS')[1:]             
        idx_after = pd.date_range(df_ssp370.index[-1], periods=int(nsmooth/2)+1, freq='AS')[1:]             
        df_ssp370_window_before = pd.DataFrame( columns=df_ssp370.columns, index=idx_before )    
        df_ssp370_window_after = pd.DataFrame( columns=df_ssp370.columns, index=idx_after )    
        window_before_mean = np.nanmean( df_ssp370[0:int(nsmooth/2)-1], axis=0 )
        window_after_mean = np.nanmean( df_ssp370[-int(nsmooth/2):], axis=0 )
        df_ssp370_window_before.iloc[:,:]  = np.tile( window_before_mean, [len(idx_before),1])
        df_ssp370_window_after.iloc[:,:]  = np.tile( window_after_mean, [len(idx_after),1])
    
        df_ssp126_ext = pd.concat( [df_ssp126_window_before, df_ssp126, df_ssp126_window_after] )
        df_ssp370_ext = pd.concat( [df_ssp370_window_before, df_ssp370, df_ssp370_window_after] )
        df_ssp126_p05 = df_ssp126_ext.copy().quantile(q=0.05, axis=1, numeric_only=False, interpolation='linear', method='single').rolling(nsmooth, center=True, win_type='gaussian').mean(std=3)
        df_ssp126_p50 = df_ssp126_ext.copy().quantile(q=0.5, axis=1, numeric_only=False, interpolation='linear', method='single').rolling(nsmooth, center=True, win_type='gaussian').mean(std=3)
        df_ssp126_p95 = df_ssp126_ext.copy().quantile(q=0.95, axis=1, numeric_only=False, interpolation='linear', method='single').rolling(nsmooth, center=True, win_type='gaussian').mean(std=3)
        df_ssp370_p05 = df_ssp370_ext.copy().quantile(q=0.05, axis=1, numeric_only=False, interpolation='linear', method='single').rolling(nsmooth, center=True, win_type='gaussian').mean(std=3)
        df_ssp370_p50 = df_ssp370_ext.copy().quantile(q=0.5, axis=1, numeric_only=False, interpolation='linear', method='single').rolling(nsmooth, center=True, win_type='gaussian').mean(std=3)
        df_ssp370_p95 = df_ssp370_ext.copy().quantile(q=0.95, axis=1, numeric_only=False, interpolation='linear', method='single').rolling(nsmooth, center=True, win_type='gaussian').mean(std=3)                
        dg_ssp126 = df_ssp126_ext.copy().rolling(nsmooth, center=True, win_type='gaussian').mean(std=3)
        dg_ssp370 = df_ssp370_ext.copy().rolling(nsmooth, center=True, win_type='gaussian').mean(std=3)               
            
        # TRIM: back to data range
    
        df_ssp126_p05 = df_ssp126_p05[ (df_ssp126_p05.index >= df_ssp126.index[0]) & (df_ssp126_p05.index <= df_ssp126.index[-1]) ]    
        df_ssp126_p50 = df_ssp126_p50[ (df_ssp126_p50.index >= df_ssp126.index[0]) & (df_ssp126_p50.index <= df_ssp126.index[-1]) ]    
        df_ssp126_p95 = df_ssp126_p95[ (df_ssp126_p95.index >= df_ssp126.index[0]) & (df_ssp126_p95.index <= df_ssp126.index[-1]) ]    
        df_ssp370_p05 = df_ssp370_p05[ (df_ssp370_p05.index >= df_ssp370.index[0]) & (df_ssp370_p05.index <= df_ssp370.index[-1]) ]    
        df_ssp370_p50 = df_ssp370_p50[ (df_ssp370_p50.index >= df_ssp370.index[0]) & (df_ssp370_p50.index <= df_ssp370.index[-1]) ]    
        df_ssp370_p95 = df_ssp370_p95[ (df_ssp370_p95.index >= df_ssp370.index[0]) & (df_ssp370_p95.index <= df_ssp370.index[-1]) ]    
        dg_ssp126 = dg_ssp126[ (dg_ssp126.index >= df_ssp126.index[0]) & (dg_ssp126.index <= df_ssp126.index[-1]) ]    
        dg_ssp370 = dg_ssp370[ (dg_ssp370.index >= df_ssp370.index[0]) & (dg_ssp370.index <= df_ssp370.index[-1]) ]    
            
        #------------------------------------------------------------------------------
        # PLOT
        #------------------------------------------------------------------------------
    
        figstr = 'PLOTS/' + thresholdsstr[j] + '_' + 'SSPs_with_historical' + '_' + city + '.png'
        titlestr = 'ISIMIP HSI models (regridded to 0.5° degrees, no offset): ' + thresholdsstr[j] + ' (' + str(nsmooth) + '-yr MA)'  + ': ' + city + ' (' + str(np.round(location_lat,3)) + '°N,' + str(np.round(location_lon,3)) + '°E)'
                        
        fig, ax = plt.subplots(figsize=(15,10))     
        for i in range(len(dg_ssp126.columns)): plt.plot(dg_ssp126[dg_ssp126.index.year<=2011].index, dg_ssp126[dg_ssp126.index.year<=2011][dg_ssp126.columns[i]].values, color='grey', lw=1, zorder=1)    
        for i in range(len(dg_ssp126.columns)): plt.plot(dg_ssp126[dg_ssp126.index.year>=2011].index, dg_ssp126[dg_ssp126.index.year>=2011][dg_ssp126.columns[i]].values, color='lime', lw=1, zorder=2)    
        for i in range(len(dg_ssp370.columns)): plt.plot(dg_ssp370[dg_ssp370.index.year<=2011].index, dg_ssp370[dg_ssp370.index.year<=2011][dg_ssp370.columns[i]].values, color='grey', lw=1, zorder=1)    
        for i in range(len(dg_ssp370.columns)): plt.plot(dg_ssp370[dg_ssp370.index.year>=2011].index, dg_ssp370[dg_ssp370.index.year>=2011][dg_ssp370.columns[i]].values, color='orange', lw=1, zorder=3)    
        
        plt.fill_between(df_ssp126_p05[df_ssp126_p05.index.year<=2011].index, df_ssp126_p05[df_ssp126_p05.index.year<=2011].values, df_ssp126_p95[df_ssp126_p95.index.year<=2011].values, color='lightgrey', edgecolor="black", linewidth=0.0, alpha=0.5, label='Historical (5-95% CI)', zorder=11)                
        plt.fill_between(df_ssp126_p05[df_ssp126_p05.index.year>=2011].index, df_ssp126_p05[df_ssp126_p05.index.year>=2011].values, df_ssp126_p95[df_ssp126_p95.index.year>=2011].values, color='lime', edgecolor="green", linewidth=0.0, alpha=0.5, label='SSP1-2.6 (5-95% CI)',zorder=12)
        plt.fill_between(df_ssp370_p05[df_ssp370_p05.index.year<=2011].index, df_ssp370_p05[df_ssp370_p05.index.year<=2011].values, df_ssp370_p95[df_ssp370_p95.index.year<=2011].values, color='lightgrey', edgecolor="black", linewidth=0.0, alpha=0.5, zorder=11)
        plt.fill_between(df_ssp370_p05[df_ssp370_p05.index.year>=2011].index, df_ssp370_p05[df_ssp370_p05.index.year>=2011].values, df_ssp370_p95[df_ssp370_p95.index.year>=2011].values, color='orange', edgecolor="red", linewidth=0.0, alpha=0.5, label='SSP3-7.0 (5-95% CI)',zorder=12)
    
        plt.plot(df_ssp126_p05[df_ssp126_p05.index.year<=2011].index, df_ssp126_p05[df_ssp126_p05.index.year<=2011].values, color='black', alpha=0.5, lw=3, zorder=101)
        plt.plot(df_ssp126_p50[df_ssp126_p50.index.year<=2011].index, df_ssp126_p50[df_ssp126_p50.index.year<=2011].values, color='black', lw=3, zorder=101)
        plt.plot(df_ssp126_p95[df_ssp126_p95.index.year<=2011].index, df_ssp126_p95[df_ssp126_p95.index.year<=2011].values, color='black', alpha=0.5, lw=3, zorder=101)
        plt.plot(df_ssp126_p05[df_ssp126_p05.index.year>=2011].index, df_ssp126_p05[df_ssp126_p05.index.year>=2011].values, color='green', alpha=0.5, lw=3, zorder=102)
        plt.plot(df_ssp126_p50[df_ssp126_p50.index.year>=2011].index, df_ssp126_p50[df_ssp126_p50.index.year>=2011].values, color='green', lw=3, zorder=102)
        plt.plot(df_ssp126_p95[df_ssp126_p95.index.year>=2011].index, df_ssp126_p95[df_ssp126_p95.index.year>=2011].values, color='green', alpha=0.5, lw=3, zorder=102)
    
        plt.plot(df_ssp370_p05[df_ssp370_p05.index.year<=2011].index, df_ssp370_p05[df_ssp370_p05.index.year<=2011].values, color='black', alpha=0.5, lw=3, zorder=101)
        plt.plot(df_ssp370_p50[df_ssp370_p50.index.year<=2011].index, df_ssp370_p50[df_ssp370_p50.index.year<=2011].values, color='black', lw=3, zorder=101)
        plt.plot(df_ssp370_p95[df_ssp370_p95.index.year<=2011].index, df_ssp370_p95[df_ssp370_p95.index.year<=2011].values, color='black', alpha=0.5, lw=3, zorder=101)
        plt.plot(df_ssp370_p05[df_ssp370_p05.index.year>=2011].index, df_ssp370_p05[df_ssp126_p05.index.year>=2011].values, color='red', alpha=0.5, lw=3, zorder=102)
        plt.plot(df_ssp370_p50[df_ssp370_p50.index.year>=2011].index, df_ssp370_p50[df_ssp126_p50.index.year>=2011].values, color='red', lw=3, zorder=102)
        plt.plot(df_ssp370_p95[df_ssp370_p95.index.year>=2011].index, df_ssp370_p95[df_ssp126_p95.index.year>=2011].values, color='red', alpha=0.5, lw=3, zorder=102)
    
        #plt.plot(d_obs.index, d_obs.obs, color='blue', alpha=0.5, lw=1, label=obs_str, zorder=1001)
        #plt.plot(d_obs_smooth.index, d_obs_smooth.obs, color='blue', alpha=1, lw=3, zorder=1002)
    
        ax.set_axisbelow(True)
        ax.xaxis.grid(color='gray', linestyle='dashed')
        ax.yaxis.grid(color='gray', linestyle='dashed')
    
        plt.xlim( pd.to_datetime('1900', format='%Y'), pd.to_datetime('2100', format='%Y'))
        ax.set_xticks( pd.date_range( start=str(1900), end=str(2100), freq='10AS') )
        ax.set_xticklabels([ '1900','','','','','1950','','','','','2000','','','','','2050','','','','','2100'  ])
    
        ystr = thresholdsstr[j] + ', [days]'
        
        plt.ylabel(ystr, fontsize=fontsize)
    
        plt.legend(loc='upper left', markerscale=1, ncol=1, facecolor='white', framealpha=0.9, fontsize=10)    
        plt.tick_params(labelsize=fontsize)    
        plt.title(titlestr, fontsize=fontsize)
        plt.savefig(figstr, dpi=300, bbox_inches='tight')
        plt.close('all')

#------------------------------------------------------------------------------
# SAVE: model summary stats array
#------------------------------------------------------------------------------

model_summary_stats_matrix = np.vstack( model_summary_stats_matrix )
cols = [
        'obs_mean_1961_1990','obs_p05_1961_1990','obs_p95_1961_1990','historical_mean_1961_1990','historical_p05_1961_1990','historical_p95_1961_1990','ssp126_mean_1961_1990','ssp126_p05_1961_1990','ssp126_p95_1961_1990','ssp370_mean_1961_1990','ssp370_p05_1961_1990','ssp370_p95_1961_1990',
        'obs_mean_1971_2000','obs_p05_1971_2000','obs_p95_1971_2000','historical_mean_1971_2000','historical_p05_1971_2000','historical_p95_1971_2000','ssp126_mean_1971_2000','ssp126_p05_1971_2000','ssp126_p95_1971_2000','ssp370_mean_1971_2000','ssp370_p05_1971_2000','ssp370_p95_1971_2000',
        'obs_mean_1981_2010','obs_p05_1981_2010','obs_p95_1981_2010','historical_mean_1981_2010','historical_p05_1981_2010','historical_p95_1981_2010','ssp126_mean_1981_2010','ssp126_p05_1981_2010','ssp126_p95_1981_2010','ssp370_mean_1981_2010','ssp370_p05_1981_2010','ssp370_p95_1981_2010',
        'obs_mean_2021_2050','obs_p05_2021_2050','obs_p95_2021_2050','historical_mean_2021_2050','historical_p05_2021_2050','historical_p95_2021_2050','ssp126_mean_2021_2050','ssp126_p05_2021_2050','ssp126_p95_2021_2050','ssp370_mean_2021_2050','ssp370_p05_2021_2050','ssp370_p95_2021_2050',
        'obs_mean_2035_2064','obs_p05_2035_2064','obs_p95_2035_2064','historical_mean_2035_2064','historical_p05_2035_2064','historical_p95_2035_2064','ssp126_mean_2035_2064','ssp126_p05_2035_2064','ssp126_p95_2035_2064','ssp370_mean_2035_2064','ssp370_p05_2035_2064','ssp370_p95_2035_2064',
        'obs_mean_2071_2100','obs_p05_2071_2100','obs_p95_2071_2100','historical_mean_2071_2100','historical_p05_2071_2100','historical_p95_2071_2100','ssp126_mean_2071_2100','ssp126_p05_2071_2100','ssp126_p95_2071_2100','ssp370_mean_2071_2100','ssp370_p05_2071_2100','ssp370_p95_2071_2100'
        ]
df_stats = pd.DataFrame(index=thresholdsstr)
for i in range(len(cols)):
    df_stats[cols[i]] = model_summary_stats_matrix[:,i]

# DROP: not needed columns

cols_to_drop = list([ 'obs_p05_1961_1990','obs_p95_1961_1990','ssp126_mean_1961_1990','ssp126_p05_1961_1990','ssp126_p95_1961_1990','ssp370_mean_1961_1990','ssp370_p05_1961_1990','ssp370_p95_1961_1990',
                      'obs_p05_1971_2000','obs_p95_1971_2000','ssp126_mean_1971_2000','ssp126_p05_1971_2000','ssp126_p95_1971_2000','ssp370_mean_1971_2000','ssp370_p05_1971_2000','ssp370_p95_1971_2000',
                      'obs_p05_1981_2010','obs_p95_1981_2010','ssp126_mean_1981_2010','ssp126_p05_1981_2010','ssp126_p95_1981_2010','ssp370_mean_1981_2010','ssp370_p05_1981_2010','ssp370_p95_1981_2010',
                      'obs_mean_2021_2050','obs_p05_2021_2050','obs_p95_2021_2050','historical_mean_2021_2050','historical_p05_2021_2050','historical_p95_2021_2050', 
                      'obs_mean_2035_2064','obs_p05_2035_2064','obs_p95_2035_2064','historical_mean_2035_2064','historical_p05_2035_2064','historical_p95_2035_2064',
                      'obs_mean_2071_2100','obs_p05_2071_2100','obs_p95_2071_2100','historical_mean_2071_2100','historical_p05_2071_2100','historical_p95_2071_2100'
                        ])


df_stats = df_stats.drop( columns = cols_to_drop ).round(2)
df_stats.to_csv( 'OUT/' + 'stats' + '-' + vartypestr + '-' + city + '.csv' )

#------------------------------------------------------------------------------
# SAVE: model summary stats baseline difference array
#------------------------------------------------------------------------------

cols_to_drop = list([ 
    'obs_mean_1961_1990', 'historical_mean_1961_1990',
    'historical_p05_1961_1990', 'historical_p95_1961_1990',
    'obs_mean_1971_2000', 'historical_mean_1971_2000',
    'historical_p05_1971_2000', 'historical_p95_1971_2000',
    'obs_mean_1981_2010', 'historical_mean_1981_2010',
    'historical_p05_1981_2010', 'historical_p95_1981_2010',
                        ])

df_stats_difference = pd.DataFrame( columns=df_stats.columns, index=df_stats.index)
df_stats_difference = df_stats_difference.drop( columns = cols_to_drop )

cols = df_stats_difference.columns
                
for i in range(len(cols)):
    if 'mean' in cols[i]:
        df_stats_difference[cols[i]] = df_stats[cols[i]] - df_stats['historical_mean_1981_2010']
    elif 'p05' in cols[i]:
        df_stats_difference[cols[i]] = df_stats[cols[i]] - df_stats['historical_p05_1981_2010']
    elif 'p95' in cols[i]:
        df_stats_difference[cols[i]] = df_stats[cols[i]] - df_stats['historical_p95_1981_2010']

df_stats_difference = df_stats_difference.round(2)
df_stats_difference.to_csv( 'OUT/' + 'stats' + '-' + '1981-2010-difference' + '-' + vartypestr + '-' + city + '.csv' )

#------------------------------------------------------------------------------
print('** END')

    
