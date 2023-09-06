#! /usr/bin python

#------------------------------------------------------------------------------
# PROGRAM: merge-stats.py
#------------------------------------------------------------------------------
# Version 0.1
# 6 September, 2023
# Michael Taylor
# https://patternizer.github.io
# michael DOT a DOT taylor AT uea DOT ac DOT uk
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# IMPORT PYTHON LIBRARIES
#------------------------------------------------------------------------------
# Dataframe libraries:
import pandas as pd
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

#------------------------------------------------------------------------------
# LOAD: CSV files, merge dataframes, sort by variable name, and save
#------------------------------------------------------------------------------

filename1 = 'OUT/stats-regridded-etccdi-percentile-based-yearly-' + city + '.csv'
filename2 = 'OUT/stats-regridded-etccdi-baseline-independent-yearly-' + city + '.csv'
filename3 = 'OUT/stats-regridded-tas-monthly-' + city + '.csv'
filename4 = 'OUT/stats-regridded-pr-monthly-' + city + '.csv'
df1 = pd.read_csv( filename1, index_col=0)
df2 = pd.read_csv( filename2, index_col=0)
df3 = pd.read_csv( filename3, index_col=0)
df4 = pd.read_csv( filename4, index_col=0)
df = pd.concat([df1, df2, df3, df4])
df = df.sort_index(ascending=True)
df.to_csv('stats-regridded-etccdi-yearly-' + city + '.csv')

filename1 = 'OUT/stats-1981-2010-difference-regridded-etccdi-percentile-based-yearly-' + city + '.csv'
filename2 = 'OUT/stats-1981-2010-difference-regridded-etccdi-baseline-independent-yearly-' + city + '.csv'
filename3 = 'OUT/stats-1981-2010-difference-regridded-tas-monthly-' + city + '.csv'
filename4 = 'OUT/stats-1981-2010-difference-regridded-pr-monthly-' + city + '.csv'
df1 = pd.read_csv( filename1, index_col=0)
df2 = pd.read_csv( filename2, index_col=0)
df3 = pd.read_csv( filename3, index_col=0)
df4 = pd.read_csv( filename4, index_col=0)
df = pd.concat([df1, df2, df3, df4])
df = df.sort_index(ascending=True)
df.to_csv('stats-1981-2010-difference-regridded-etccdi-yearly-' + city + '.csv')

filename1 = 'OUT/stats-regridded-etccdi-percentile-based-yearly-bias_adjusted-' + city + '.csv'
filename2 = 'OUT/stats-regridded-etccdi-baseline-independent-yearly-bias_adjusted-' + city + '.csv'
filename3 = 'OUT/stats-regridded-tas-monthly-bias_adjusted-' + city + '.csv'
filename4 = 'OUT/stats-regridded-pr-monthly-bias_adjusted-' + city + '.csv'
df1 = pd.read_csv( filename1, index_col=0)
df2 = pd.read_csv( filename2, index_col=0)
df3 = pd.read_csv( filename3, index_col=0)
df4 = pd.read_csv( filename4, index_col=0)
df = pd.concat([df1, df2, df3, df4])
df = df.sort_index(ascending=True)
df.to_csv('stats-regridded-etccdi-yearly-bias_adjusted-' + city + '.csv')

filename1 = 'OUT/stats-1981-2010-difference-regridded-etccdi-percentile-based-yearly-bias_adjusted-' + city + '.csv'
filename2 = 'OUT/stats-1981-2010-difference-regridded-etccdi-baseline-independent-yearly-bias_adjusted-' + city + '.csv'
filename3 = 'OUT/stats-1981-2010-difference-regridded-tas-monthly-bias_adjusted-' + city + '.csv'
filename4 = 'OUT/stats-1981-2010-difference-regridded-pr-monthly-bias_adjusted-' + city + '.csv'
df1 = pd.read_csv( filename1, index_col=0)
df2 = pd.read_csv( filename2, index_col=0)
df3 = pd.read_csv( filename3, index_col=0)
df4 = pd.read_csv( filename4, index_col=0)
df = pd.concat([df1, df2, df3, df4])
df = df.sort_index(ascending=True)
df.to_csv('stats-1981-2010-difference-regridded-etccdi-yearly-bias_adjusted-' + city + '.csv')
    
#------------------------------------------------------------------------------
print('** END')


    
    
