#!/bin/bash

#------------------------------------------------------------------------------
# PROGRAM: downscale-nc.sh
#------------------------------------------------------------------------------
# Version 0.1
# 11 July, 2023
# Michael Taylor
# https://patternizer.github.io
# michael DOT a DOT taylor AT uea DOT ac DOT uk
#------------------------------------------------------------------------------
# Bash script to interpolate all CMIP6 models from native resolution to CRU TS 0.5 degrees
#------------------------------------------------------------------------------

# Set the source and target grids (optional)
source_grid="source_grid.nc"
target_grid="target_grid.nc"

# Set the output directory
output_dir="regridded"

# Create the output directory if it doesn't exist
mkdir -p "$output_dir"

# Set the model root directory
model_dir=`ls ~/Documents/REPOS/cussh-py/DATA/`

# Loop through the NetCDF files in all model directories

for model in $model_dir; do

	for file in ~/Documents/REPOS/cussh-py/DATA/$model/*.nc; do

		# Get the file name without the extension
		file_name=$(basename "$file" .nc)    

		# Define the output file path
		output_file="$output_dir/${file_name}.nc"   

		# Perform bilinear interpolation using CDO
		#cdo remapbil,"$target_grid" "$file" "$output_file"
		cdo remapbil,r720x360 "$file" "$output_file"

	done

done

