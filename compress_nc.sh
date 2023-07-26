#!/bin/bash

#------------------------------------------------------------------------------
# PROGRAM: compress-nc.sh
#------------------------------------------------------------------------------
# Version 0.1
# 16 July, 2023
# Michael Taylor
# https://patternizer.github.io
# michael DOT a DOT taylor AT uea DOT ac DOT uk
#------------------------------------------------------------------------------
# Bash script to interpolate all CMIP6 models from native resolution to CRU TS 0.5 degrees
#------------------------------------------------------------------------------

# Set the output directory
output_dir="regridded-compressed"

# Create the output directory if it doesn't exist
mkdir -p "$output_dir"

# Loop through the NetCDF files in regridded/

for file in ~/Documents/REPOS/cussh-py/DATA/regridded/*.nc; do

	# Get the file name without the extension
	file_name=$(basename "$file" .nc)    

	# Define the output file path
	output_file="$output_dir/${file_name}.zip"   

	zip "$file" "$output_file"

done

