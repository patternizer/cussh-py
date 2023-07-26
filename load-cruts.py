#! /usr/bin python

#------------------------------------------------------------------------------
# PROGRAM: load-cruts.py
#------------------------------------------------------------------------------
# Version 0.1
# 13 July, 2023
# Michael Taylor
# https://patternizer.github.io
# michael DOT a DOT taylor AT uea DOT ac DOT uk
#------------------------------------------------------------------------------
# READER for CRUTS data scraped from Google Earth
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# IMPORT PYTHON LIBRARIES
#------------------------------------------------------------------------------

# Dataframe libraries:
import numpy as np
import pandas as pd
import pickle

#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# SETTINGS: 
#------------------------------------------------------------------------------

city, location_lat, location_lon = 'London', 51.5, -0.1
#city, location_lat, location_lon = 'Rennes', 48.1, -1.7
#city, location_lat, location_lon = 'Kisumu', -0.1, 34.8
#city, location_lat, location_lon = 'Nairobi', -1.3, 36.8
#city, location_lat, location_lon = 'Beijing', 39.9, 116.4
#city, location_lat, location_lon = 'Ningbo', 29.9, 121.6
 
cruts_obs_file = 'DATA/cruts-tmp-london-0.5.txt'
#cruts_obs_file = 'DATA/cruts-tmp-rennes-0.5.txt'
#cruts_obs_file = 'DATA/cruts-tmp-nairobi-0.5.txt'
#cruts_obs_file = 'DATA/cruts-tmp-kisumu-0.5.txt'
#cruts_obs_file = 'DATA/cruts-tmp-beijing-0.5.txt'
#cruts_obs_file = 'DATA/cruts-tmp-ningbo-0.5.txt'

#cruts_obs_file = 'DATA/cruts-pre-london-0.5.txt'
#cruts_obs_file = 'DATA/cruts-pre-rennes-0.5.txt'
#cruts_obs_file = 'DATA/cruts-pre-nairobi-0.5.txt'
#cruts_obs_file = 'DATA/cruts-pre-kisumu-0.5.txt'
#cruts_obs_file = 'DATA/cruts-pre-beijing-0.5.txt'
#cruts_obs_file = 'DATA/cruts-pre-ningbo-0.5.txt'

cruts_pkl = cruts_obs_file.split('/')[1].split('.txt')[0] + '.pkl'

#------------------------------------------------------------------------------
# LOAD: CRU TS 4.07 Norwich extract --> df_cruts_obs
#------------------------------------------------------------------------------

f = open( cruts_obs_file )
lines = f.readlines()
f.close()
lines2 = lines[7:]
dates = []
values = []
for i in range( len(lines2) ):
    date = lines2[ i ].strip().split()[0] + '-' + lines2[ i ].strip().split()[1] + '-' + '01'
    dates.append( date )
    values.append( float( lines2[ i ].strip().split()[2] ) )        
datetimes_cruts_obs = [ pd.to_datetime( dates[i] ) for i in range(len(dates)) ]

#------------------------------------------------------------------------------
# SAVE: actuals timeseries
#------------------------------------------------------------------------------

df_obs = pd.DataFrame( {'datetime':datetimes_cruts_obs, 'obs':values } )
df_obs.to_pickle( cruts_pkl, compression='bz2' )

#------------------------------------------------------------------------------
# COMPUTE: anomalies
#------------------------------------------------------------------------------

# UNPACK: actuals timeseries to month column format

years = df_obs['datetime'].dt.year.unique()
values = df_obs['obs'].values.reshape( int(len(df_obs)/12), 12 )
df_actuals = pd.DataFrame(columns=['year','1','2','3','4','5','6','7','8','9','10','11','12'])
df_actuals['year'] = years
for i in range(12):
    df_actuals[str(i+1)] = values[:,i]

# COMPUTE: anomalies in month column format

normals = np.nanmean( df_actuals[ (df_actuals.year>=1961) & (df_actuals.year<=1990) ], axis=0)[1:]

df_anomalies = df_actuals.copy()
for i in range(12):
    df_anomalies[str(i+1)] = df_anomalies[str(i+1)] - normals[i]

# REPACK: anomalies timeseries

t_cruts = df_obs['datetime'] + pd.to_timedelta(15, unit="D")
ts_cruts = []    
for i in range(len(df_anomalies)):            
   monthly = df_anomalies.iloc[i,1:]
   ts_cruts = ts_cruts + monthly.to_list()    
ts_cruts = np.array( ts_cruts )

# SAVE: anomalies timeseries

df_anomalies = pd.DataFrame( {'datetime':t_cruts, 'obs':ts_cruts } )

#------------------------------------------------------------------------------
print('** END')
