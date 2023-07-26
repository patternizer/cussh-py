![image](https://github.com/patternizer/cussh-py/blob/main/PLOTS/tn90pETCCDI_SSPs_with_historical_regridded_Beijing.png)

# cussh-py

Python codebase for CUSSH project.

## Contents

* `c3s-cds-api-cussh.py` - python api caller to download selected ISIMIP model runs from the C3S CDS using the cdsapi client
* `c3s-cds-api-cussh-pre-historical.py` - python api caller to download CMIP6 precipitation model historical runs from 1850-2014 from the C3S CDS using the cdsapi client
* `c3s-cds-api-cussh-pre-126.py` - python api caller to download CMIP6 precipitation model SSP1-2.6 projections from 2015-2100 from the C3S CDS using the cdsapi client
* `c3s-cds-api-cussh-pre-370.py` - python api caller to download CMIP6 precipitation model SSP3-7.0 projections from 2015-2100 from the C3S CDS using the cdsapi client
* `c3s-cds-api-cussh-tmp-historical.py` - python api caller to download CMIP6 near surface temperature model historical runs from 1850-2014 from the C3S CDS using the cdsapi client
* `c3s-cds-api-cussh-tmp-126.py` - python api caller to download CMIP6 near surface temperature model SSP1-2.6 projections from 2015-2100 from the C3S CDS using the cdsapi client
* `c3s-cds-api-cussh-tmp-370.py` - python api caller to download CMIP6 near surface temperature model SSP3-7.0 projections from 2015-2100 from the C3S CDS using the cdsapi client
* `merge_netcdfs.py` - python script to merge CMIP6 run fragments along the time dimension (overcomes CDO mergetime fail error)
* `downscale-nc.sh` - bash script to interpolate ISIMIP model runs from their native resolution to the CRU TS 0.5 degree resolution (loop over model directories)
* `downscale-nc-single_dir.sh` - bash script to interpolate ISIMIP model runs from their native resolution to the CRU TS 0.5 degree resolution (single directory version)
* `compress_nc.sh` - bash script to compress model run archives
* `load-cruts.py` - python reader to load CRUTS v4.7 station precipitation and near surface temperature series ASCII output from GoogleEarth
* `load-cussh-isimip.py` - python reader to load in downloaded netCDF-4 climate model ensemble members and extract metadata
* `load-cussh-isimip-timeseries.py` - python reader to load in downloaded netCDF-4 climate model ensemble members and extract timeseries per variable per experiment across models
* `load-cussh-isimip-timeseries-combined.py` - python code to load in CMIP6 experiments .pkl files and combine historical and SSP projections and apply Gaussian filter to 90% C.I.

The first step is to clone the latest cussh-py code and step into the check out directory: 

    $ git clone https://github.com/patternizer/cussh-py.git
    $ cd cussh-py

### Usage

The code was tested locally in a Python 3.8.11 virtual environment.

    $ python c3s-cds-api-cussh.py 		# [or variants]
    $ python downscale-nc.py 			# [or single dir variant]
    $ python load-cussh-isimip.py
    $ python load-cussh-isimip-timeseries.py
    $ python load-cussh-isimip-timeseries-combined.py
    
Observations and projection source data extracted from C3S CDS are available on request. Example plots (updating) are in the /PLOTS directory.

## License

The code is distributed under terms and conditions of the [Open Government License](http://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/).

## Contact information

* [Michael Taylor](michael.a.taylor@uea.ac.uk)


