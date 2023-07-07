# cussh-py

Python codebase for CUSSH project.

## Contents

* `c3s-cds-api-cussh.py` - python api caller to download selected ISIMIP model runs from the C3S CDS using the cdsapi client
* `load-cussh-isimip.py` - python reader to load in downloaded netCDF-4 climate model ensemble members and extract metadata

The first step is to clone the latest cussh-py code and step into the check out directory: 

    $ git clone https://github.com/patternizer/cussh-py.git
    $ cd cussh-py

### Usage

The code was tested locally in a Python 3.8.11 virtual environment.

    $ python c3s-cds-api-cussh.py
    $ python load-cussh-isimip.py
    
Observations and projection source data extracted from C3S CDS are available on request.

## License

The code is distributed under terms and conditions of the [Open Government License](http://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/).

## Contact information

* [Michael Taylor](michael.a.taylor@uea.ac.uk)


