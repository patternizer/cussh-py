#!/bin/bash

#------------------------------------------------------------------------------
# PROGRAM: downscale-nc-single-dir.sh
#------------------------------------------------------------------------------
# Version 0.2
# 17 July, 2023
# Michael Taylor
# https://patternizer.github.io
# michael DOT a DOT taylor AT uea DOT ac DOT uk
#------------------------------------------------------------------------------
# Bash script to interpolate all CMIP6 models from native resolution to CRU TS 0.5 degrees
#------------------------------------------------------------------------------

#source_grid="source_grid.nc" # (optional)
#target_grid="target_grid.nc" # (optional)

output_dir="regridded" # output directory
mkdir -p "$output_dir" # create output_dir if it doesn't exist

# Loop through the NetCDF files in directory

for file in ~/Documents/REPOS/cussh-py/DATA/tmp/*.nc; do

	file_name=$(basename "$file" .nc) 				# Get the file name without the extension
	output_file="$output_dir/${file_name}.nc" 		# Define the output file path
	cdo remapbil,r720x360 "$file" "$output_file" 	# bilinear interpolation using CDO
	#cdo remapbil,"$target_grid" "$file" "$output_file" # (optional)

done

