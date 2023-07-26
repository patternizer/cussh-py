#!/usr/bin/env python

import cdsapi
c = cdsapi.Client()

formatstr = 'tgz' # ['tgz','zip']

#for v in list(['near_surface_air_temperature', 'precipitation']):
#    for e in list(['historical', 'ssp1_2_6', 'ssp2_4_5', 'ssp3_7_0', 'ssp5_8_5']):

#v = 'near_surface_air_temperature'
v = 'precipitation'

#e = 'historical'
#e = 'ssp1_2_6'
#e = 'ssp2_4_5'
e = 'ssp3_7_0'
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
#            'cesm2_fv2',
#            'cesm2_wacom_fv2',
#            'cmcc_cm2_hr4',
#            'cmcc_esm2',
            'cnrm_cm6_1_hr',
#            'e3sm_1_0',
#            'e3sm_1_1_eca',            
            'ec_earth3_aerchem',            
#            'ec_earth3_veg',            
            'fgoals_f3_l',
#            'fio_esm_2_0',
#            'giss_e2_1_g',            
#            'hadgem3_gc31_ll',
            'iitm_esm',
            'inm_cm5_0',
            'ipsl_cm6a_lr',
#            'kiost_esm',
            'miroc6',
            'miroc_es2l',
#            'mpi-esm1_2_hr',            
            'mri_esm2_0',
#            'norcpm1',
            'noresm2_mm',
            'taiesm1',
#            'access_esm1_5',
#            'awi_esm_1_1_lr',
#            'bcc_esm1',
#            'canesm5',
            'cesm2',
            'cesm2_waccm',
#            'ciesm',
            'cmcc_cm2_sr5',
            'cnrm_cm6_1',
            'cnrm_esm2_1',
#            'e3sm_1_1',
#            'ec_earth3',
#            'ec_earth3_cc',
            'ec_earth3_veg_lr',
            'fgoals_g3',
            'gfdl_esm4',
#            'giss_e2_1_h',
#            'hadgem3_gc31_mm',
            'inm_cm4_8',
            'ipsl_cm5a2_inca',
            'kace_1_0_g',
            'mcm_ua_1_0',
#            'miroc_es2h',
            'mpi_esm_1_2_ham',
            'mpi_esm1_2_lr',
#            'nesm3',
            'noresm2_lm',
#            'sam0_unicon',
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
                    '2015', '2016', '2017', '2018', '2019', 
                    '2020', '2021', '2022', '2023', '2024', '2025', '2026', '2027', '2028', '2029',
                    '2030', '2031', '2032', '2033', '2034', '2035', '2036', '2037', '2038', '2039', 
                    '2040', '2041', '2042', '2043', '2044', '2045', '2046', '2047', '2048', '2049', 
                    '2050', '2051', '2052', '2053', '2054', '2055', '2056', '2057', '2058', '2059',
                    '2060', '2061', '2062', '2063', '2064', '2065', '2066', '2067', '2068', '2069', 
                    '2070', '2071', '2072', '2073', '2074', '2075', '2076', '2077', '2078', '2079', 
                    '2080', '2081', '2082', '2083', '2084', '2085', '2086', '2087', '2088', '2089',
                    '2090', '2091', '2092', '2093', '2094', '2095', '2096', '2097', '2098', '2099',
                    ],
                    'month': ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12',
                    ],
                    },
                    downloadstr)
                    
            except:
            
                print('variable not available')				

#----------------------------------------------

print('** END')



                
