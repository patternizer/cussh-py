#!/usr/bin/env python

import cdsapi
c = cdsapi.Client()

formatstr = 'tgz' # ['tgz','zip']

#for v in list(['near_surface_air_temperature', 'precipitation']):
#    for e in list(['historical', 'ssp1_2_6', 'ssp2_4_5', 'ssp3_7_0', 'ssp5_8_5']):

v = 'near_surface_air_temperature'
#v = 'precipitation'

e = 'historical'
#e = 'ssp1_2_6'
#e = 'ssp2_4_5'
#e = 'ssp3_7_0'
#e = 'ssp5_8_5'
	    
if e == 'historical':
    periodstr = '1850-2014'
else:
    periodstr = '2015-2100'
    
for m in list([
            'access_cm2',
            'awi_cm_1_1_mr',
            'bcc_csm2_mr',
            'cams_csm1_0',
            'canesm5_canoe',
            'cesm2_fv2',
            'cesm2_wacom_fv2',
            'cmcc_cm2_hr4',
            'cmcc_esm2',
            'cnrm_cm6_1_hr',
            'e3sm_1_0',
            'e3sm_1_1_eca',            
            'ec_earth3_aerchem',            
#            'ec_earth3_veg',            
            'fgoals_f3_l',
            'fio_esm_2_0',
#            'giss_e2_1_g',            
            'hadgem3_gc31_ll',
            'iitm_esm',
            'inm_cm5_0',
            'ipsl_cm6a_lr',
            'kiost_esm',
            'miroc6',
            'miroc_es2l',
            'mpi-esm1_2_hr',            
            'mri_esm2_0',
            'norcpm1',
            'noresm2_mm',
            'taiesm1',
            'access_esm1_5',
            'awi_esm_1_1_lr',
            'bcc_esm1',
            'canesm5',
            'cesm2',
            'cesm2_waccm',
            'ciesm',
            'cmcc_cm2_sr5',
            'cnrm_cm6_1',
            'cnrm_esm2_1',
            'e3sm_1_1',
#            'ec_earth3',
            'ec_earth3_cc',
#            'ec_earth3_veg_lr',
            'fgoals_g3',
            'gfdl_esm4',
            'giss_e2_1_h',
            'hadgem3_gc31_mm',
            'inm_cm4_8',
            'ipsl_cm5a2_inca',
            'kace_1_0_g',
            'mcm_ua_1_0',
            'miroc_es2h',
#            'mpi_esm_1_2_ham',
            'mpi_esm1_2_lr',
            'nesm3',
#            'noresm2_lm',
            'sam0_unicon',
            'ukesm1_0_ll',
            ]):

            if formatstr == 'zip':
                downloadstr = v + '_' + m + '_' + e + '.zip'
            elif formatstr == 'tgz':
                downloadstr = v + '_' + m + '_' + e + '.tar.gz'
            
            try:
				
                c.retrieve(
                    'projections-cmip6',
                    {
                    'format': formatstr,
                    'temporal_resolution': 'monthly',
                    'experiment': e,
                    'variable': v,
                    'model': m,
                    'year': [
                    '1850', '1851', '1852', '1853', '1854', '1855', '1856', '1857', '1858', '1859', 
                    '1860', '1861', '1862', '1863', '1864', '1865', '1866', '1867', '1868', '1869', 
                    '1870', '1871', '1872', '1873', '1874', '1875', '1876', '1877', '1878', '1879',
                    '1880', '1881', '1882', '1883', '1884', '1885', '1886', '1887', '1888', '1889', 
                    '1890', '1891', '1892', '1893', '1894', '1895', '1896', '1897', '1898', '1899', 
                    '1900', '1901', '1902', '1903', '1904', '1905', '1906', '1907', '1908', '1909', 
                    '1910', '1911', '1912', '1913', '1914', '1915', '1916', '1917', '1918', '1919', 
                    '1920', '1921', '1922', '1923', '1924', '1925', '1926', '1927', '1928', '1929', 
                    '1930', '1931', '1932', '1933', '1934', '1935', '1936', '1937', '1938', '1939',
                    '1940', '1941', '1942', '1943', '1944', '1945', '1946', '1947', '1948', '1949', 
                    '1950', '1951', '1952', '1953', '1954', '1955', '1956', '1957', '1958', '1959', 
                    '1960', '1961', '1962', '1963', '1964', '1965', '1966', '1967', '1968', '1969', 
                    '1970', '1971', '1972', '1973', '1974', '1975', '1976', '1977', '1978', '1979', 
                    '1980', '1981', '1982', '1983', '1984', '1985', '1986', '1987', '1988', '1989', 
                    '1990', '1991', '1992', '1993', '1994', '1995', '1996', '1997', '1998', '1999',
                    '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', 
                    '2010', '2011', '2012', '2013', '2014',                                
                    ],
                    'month': ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12',
                    ],
                    },
                    downloadstr)
                    
            except:
            
                print('variable not available')				

#----------------------------------------------

print('** END')



                
