![image](https://github.com/patternizer/cussh-py/blob/main/PLOTS/tnxETCCDI_SSPs_with_historical_bias_adjusted-London.png)

# cussh-py

Python codebase for CUSSH project.

## Contents

* `load-cussh-isimip-metadata.py` - python reader to load in downloaded netCDF-4 ISIMIP climate model ensemble members and extract metadata
* `load-cussh-isimip-timeseries.py` - python reader to load in downloaded netCDF-4 ISIMIP climate model ensemble members and extract timeseries per variable per experiment across models
* `load-cussh-isimip-timeseries-combined.py` - python code to load in ISIMIP experiment .pkl files and combine historical and SSP projections and apply Gaussian filter to 90% C.I.
* `load-cussh-cmip6-metadata.py` - python reader to load in downloaded netCDF-4 CMIP6 climate model runs for TAS and PR and extract metadata
* `load-cussh-cmip6-timeseries.py` - python reader to load in downloaded netCDF-4 CMIP6 climate model runs for TAS and PR and extract timeseries per variable per experiment across models
* `load-cussh-cmip6-timeseries-combined.py` - python code to load in CMIP6 experiment .pkl files and combine historical and SSP projections and apply Gaussian filter to 90% C.I.
* `merge_netcdfs.py` - python script to merge CMIP6 run fragments along the time dimension (overcomes CDO mergetime fail error)
* `merge_stats.py` - python script to merge the 30-yr climatological period stats from the ISIMIP and CMIP6 variable runs into single, sorted spreadsheets
* `downscale-nc-single_dir.sh` - bash script to interpolate ISIMIP model runs from their native resolution to the CRU TS 0.5 degree resolution (single directory version)
* `compress_nc.sh` - bash script to compress model run archives

The first step is to clone the latest cussh-py code and step into the check out directory: 

    $ git clone https://github.com/patternizer/cussh-py.git
    $ cd cussh-py

### Usage

The code was tested locally in a Python 3.8.11 virtual environment.

    $ python downscale-nc-single_dir.sh
    $ python load-cussh-isimip-metadata.py
    $ python load-cussh-isimip-timeseries.py
    $ python load-cussh-isimip-timeseries-combined.py
    $ python load-cussh-cmip6-metadata.py
    $ python load-cussh-cmip6-timeseries.py
    $ python load-cussh-cmip6-timeseries-combined.py
    $ python merge-stats.py
    
Observations and projection source data extracted from C3S CDS are available on request. Example plots (updating) are in the /PLOTS directory.

## License

The code is distributed under terms and conditions of the [Open Government License](http://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/).

## Contact information

* [Michael Taylor](michael.a.taylor@uea.ac.uk)


