#! /usr/bin python

#------------------------------------------------------------------------------
# PROGRAM: load-cussh-isimip.py
#------------------------------------------------------------------------------
# Version 0.1
# 7 July, 2023
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
#import pickle
#import netCDF4
#from datetime import datetime

# OS libraries:
import os
import glob
import sys
import time

# Plotting libraries:
#import matplotlib.pyplot as plt; plt.close('all')
#from pandas.plotting import register_matplotlib_converters
#from matplotlib import rcParams
#register_matplotlib_converters()
#import matplotlib.dates as mdates
#import seaborn as sns; sns.set()

#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# SETTINGS: 
#------------------------------------------------------------------------------

versions = list([
            '1.0', '2_0',
        ])
variables = list([
            'cold_days', 'cold_nights', 'cold_spell_duration_index',
            'consecutive_dry_days', 'consecutive_wet_days', 'diurnal_temperature_range',
            'extremely_wet_day_precipitation', 'frost_days', 'growing_season_length',
            'heavy_precipitation_days', 'ice_days', 'maximum_1_day_precipitation',
            'maximum_5_day_precipitation', 'maximum_value_of_daily_maximum_temperature', 'maximum_value_of_daily_minimum_temperature',
            'minimum_value_of_daily_maximum_temperature', 'minimum_value_of_daily_minimum_temperature', 'number_of_wet_days',
            'simple_daily_intensity_index', 'summer_days', 'total_wet_day_precipitation',
            'tropical_nights', 'very_heavy_precipitation_days', 'very_wet_day_precipitation',
            'warm_days', 'warm_nights', 'warm_spell_duration_index',            
            'heat_index', 'humidex', 'universal_thermal_climate_index',
            'wet_bulb_globe_temperature_index', 'wet_bulb_temperature_index',
        ])
product_types = list([        
            'bias_adjusted', 'non_bias_adjusted',
            'base_independent', 'base_period_1961_1990', 'base_period_1981_2010',
        ])
experiments = list([
            'historical', 'ssp1_2_6', 'ssp2_4_5', 'ssp3_7_0', 'ssp5_8_5',
        ])
temporal_aggregations = list([
             'daily', 'monthly', 'yearly',  
        ])
periods = list([
            '19510101-20101230', '19510101-20101231', '19510101-20141230', '19510101-20141231', '20110101-21001230', '20110101-21001231', '20150101-21001230', '20150101-21001231',
            '184901-201412', '185001-201412', '185001-201612', '195101-201412', '201501-203912', '201501-210012', '201501-218012', '201501-230012',
            '1849-2014', '1850-2014', '1850-2016', '1951-2014', '2015-2039', '2015-2100', '2015-2180', '2015-2300',           
        ])
ensemble_members = list([
            'r10i1p1f1', 'r10i1p2f1', 'r11i1p1f1',
            'r11i1p2f1', 'r12i1p1f1', 'r12i1p2f1',
            'r13i1p1f1', 'r13i1p2f1', 'r14i1p1f1',
            'r14i1p2f1', 'r15i1p1f1', 'r15i1p2f1',
            'r16i1p1f1', 'r16i1p2f1', 'r17i1p1f1',
            'r17i1p2f1', 'r18i1p1f1', 'r18i1p2f1',
            'r19i1p1f1', 'r19i1p2f1', 'r1i1p1f1',
            'r1i1p1f2', 'r1i1p1f3', 'r1i1p2f1',
            'r20i1p1f1', 'r20i1p2f1', 'r21i1p1f1',
            'r21i1p2f1', 'r22i1p1f1', 'r22i1p2f1',
            'r23i1p1f1', 'r23i1p2f1', 'r24i1p1f1',
            'r24i1p2f1', 'r25i1p1f1', 'r25i1p2f1',
            'r26i1p1f1', 'r27i1p1f1', 'r28i1p1f1',
            'r29i1p1f1', 'r2i1p1f1', 'r2i1p2f1',
            'r30i1p1f1', 'r31i1p1f1', 'r32i1p1f1',
            'r33i1p1f1', 'r34i1p1f1', 'r35i1p1f1',
            'r36i1p1f1', 'r37i1p1f1', 'r38i1p1f1',
            'r39i1p1f1', 'r3i1p1f1', 'r3i1p2f1',
            'r40i1p1f1', 'r41i1p1f1', 'r42i1p1f1',
            'r43i1p1f1', 'r44i1p1f1', 'r45i1p1f1',
            'r46i1p1f1', 'r47i1p1f1', 'r48i1p1f1',
            'r49i1p1f1', 'r4i1p1f1', 'r4i1p2f1',
            'r50i1p1f1', 'r5i1p1f1', 'r5i1p2f1',
            'r6i1p1f1', 'r6i1p2f1', 'r7i1p1f1',
            'r7i1p2f1', 'r8i1p1f1', 'r8i1p2f1',
            'r9i1p1f1', 'r9i1p2f1',
        ])        
models = list([
            'access_cm2', 'access_esm1_5', 'bcc_csm2_mr',
            'canesm5', 'cnrm_cm6_1', 'cnrm_cm6_1_hr',
            'cnrm_esm2_1', 'ec_earth3', 'ec_earth3_veg',
            'fgoals_g3', 'gfdl_cm4', 'gfdl_esm4',
            'hadgem3_gc31_ll', 'hadgem3_gc31_mm', 'inm_cm4_8',
            'inm_cm5_0', 'kace_1_0_g', 'kiost_esm',
            'miroc6', 'miroc_es2l', 'mpi_esm1_2_hr',
            'mpi_esm1_2_lr', 'mri_esm2_0', 'nesm3',
            'noresm2_lm', 'noresm2_mm', 'ukesm1_0_ll',
        ])        

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

for i in range(len(models)):
       
    modeldir = 'DATA/' + models[i] + '/'
    filelist = sorted( glob.glob( modeldir + '*.nc' ), reverse = False )
    
    # print(filelist)    
    # time.sleep(1.0)    # seconds        

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
# SAVE: metadata dataframe
#------------------------------------------------------------------------------

df.to_csv('cussh-isimip-metadata.csv')

#------------------------------------------------------------------------------
# SAVE: metadata summary per model
#------------------------------------------------------------------------------

dg = df.groupby('model').nunique()
dg.to_csv('cussh-isimip-counts.csv')

dh = df.groupby('model')['ensemble_member','lat_resolution','lon_resolution'].agg(['unique'])
dh.to_csv('cussh-isimip-summary.csv')

#------------------------------------------------------------------------------
print('** END')


    
    
