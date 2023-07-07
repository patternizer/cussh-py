#!/usr/bin/env python

import cdsapi
c = cdsapi.Client()

c.retrieve(
    'sis-extreme-indices-cmip6',
    {
        'version': '2_0',
        'format': 'tgz',
        'model': 'access_cm2',
        'variable': [
            'cold_days', 'cold_nights', 'cold_spell_duration_index',
            'extremely_wet_day_precipitation', 'very_wet_day_precipitation', 'warm_days',
            'warm_nights', 'warm_spell_duration_index',
        ],
        'product_type': 'base_period_1961_1990',
        'ensemble_member': 'r1i1p1f1',
        'experiment': [
            'historical', 'ssp1_2_6', 'ssp2_4_5',
            'ssp3_7_0', 'ssp5_8_5',
        ],
        'temporal_aggregation': 'yearly',
        'period': [
            '1850-2014', '2015-2100',
        ],
    },
    'download-access_cm2.tar.gz')

c.retrieve(
    'sis-extreme-indices-cmip6',
    {
        'version': '2_0',
        'format': 'tgz',
        'model': 'cnrm_cm6_1',
        'variable': [
            'cold_days', 'cold_nights', 'cold_spell_duration_index',
            'extremely_wet_day_precipitation', 'very_wet_day_precipitation', 'warm_days',
            'warm_nights', 'warm_spell_duration_index',
        ],
        'product_type': 'base_period_1961_1990',
        'ensemble_member': 'r1i1p1f2',
        'experiment': [
            'historical', 'ssp1_2_6', 'ssp2_4_5',
            'ssp3_7_0', 'ssp5_8_5',
        ],
        'temporal_aggregation': 'yearly',
        'period': [
            '1850-2014', '2015-2100',
        ],
    },
    'download-cnrm_cm6_1.tar.gz')

c.retrieve(
    'sis-extreme-indices-cmip6',
    {
        'version': '2_0',
        'format': 'tgz',
        'model': 'canesm5',
        'variable': [
            'cold_days', 'cold_nights', 'cold_spell_duration_index',
            'extremely_wet_day_precipitation', 'very_wet_day_precipitation', 'warm_days',
            'warm_nights', 'warm_spell_duration_index',
        ],
        'product_type': 'base_period_1961_1990',
        'ensemble_member': 'r1i1p1f1',
        'experiment': [
            'historical', 'ssp2_4_5', 'ssp3_7_0',
            'ssp5_8_5',
        ],
        'temporal_aggregation': 'yearly',
        'period': [
            '1850-2014', '2015-2100',
        ],
    },
    'download-canesm5.tar.gz')

c.retrieve(
    'sis-extreme-indices-cmip6',
    {
        'version': '2_0',
        'format': 'tgz',
        'model': 'fgoals_g3',
        'variable': [
            'cold_days', 'cold_nights', 'cold_spell_duration_index',
            'extremely_wet_day_precipitation', 'very_wet_day_precipitation', 'warm_days',
            'warm_nights', 'warm_spell_duration_index',
        ],
        'product_type': 'base_period_1961_1990',
        'ensemble_member': 'r1i1p1f1',
        'experiment': [
            'ssp1_2_6', 'ssp2_4_5', 'ssp3_7_0',
            'ssp5_8_5',
        ],
        'temporal_aggregation': 'yearly',
        'period': '2015-2100',
    },
    'download-fgoals_g3.tar.gz')

c.retrieve(
    'sis-extreme-indices-cmip6',
    {
        'version': '2_0',
        'format': 'tgz',
        'model': 'hadgem3_gc31_ll',
        'variable': [
            'cold_days', 'cold_nights', 'cold_spell_duration_index',
            'extremely_wet_day_precipitation', 'very_wet_day_precipitation', 'warm_days',
            'warm_nights', 'warm_spell_duration_index',
        ],
        'product_type': 'base_period_1961_1990',
        'ensemble_member': 'r1i1p1f3',
        'experiment': [
            'historical', 'ssp1_2_6', 'ssp2_4_5',
            'ssp5_8_5',
        ],
        'temporal_aggregation': 'yearly',
        'period': [
            '1850-2014', '2015-2100',
        ],
    },
    'download-hadgem3_gc31_ll.tar.gz')

c.retrieve(
    'sis-extreme-indices-cmip6',
    {
        'version': '2_0',
        'format': 'tgz',
        'model': 'inm_cm5_0',
        'variable': [
            'cold_days', 'cold_nights', 'cold_spell_duration_index',
            'extremely_wet_day_precipitation', 'very_wet_day_precipitation', 'warm_days',
            'warm_nights', 'warm_spell_duration_index',
        ],
        'product_type': 'base_period_1961_1990',
        'ensemble_member': 'r1i1p1f1',
        'experiment': [
            'historical', 'ssp1_2_6', 'ssp2_4_5',
            'ssp3_7_0', 'ssp5_8_5',
        ],
        'temporal_aggregation': 'yearly',
        'period': [
            '1850-2014', '2015-2100',
        ],
    },
    'download-inm_cm5_0.tar.gz')
        
c.retrieve(
    'sis-extreme-indices-cmip6',
    {
        'version': '2_0',
        'format': 'tgz',
        'model': 'miroc_es2l',
        'variable': [
            'cold_days', 'cold_nights', 'cold_spell_duration_index',
            'extremely_wet_day_precipitation', 'very_wet_day_precipitation', 'warm_days',
            'warm_nights', 'warm_spell_duration_index',
        ],
        'product_type': 'base_period_1961_1990',
        'ensemble_member': 'r1i1p1f2',
        'experiment': [
            'historical', 'ssp1_2_6', 'ssp2_4_5',
            'ssp3_7_0', 'ssp5_8_5',
        ],
        'temporal_aggregation': 'yearly',
        'period': [
            '1850-2014', '2015-2100',
        ],
    },
    'download-miroc_es2l.tar.gz')

c.retrieve(
    'sis-extreme-indices-cmip6',
    {
        'version': '2_0',
        'format': 'tgz',
        'model': 'mpi_esm1_2_lr',
        'variable': [
            'cold_days', 'cold_nights', 'cold_spell_duration_index',
            'extremely_wet_day_precipitation', 'very_wet_day_precipitation', 'warm_days',
            'warm_nights', 'warm_spell_duration_index',
        ],
        'product_type': 'base_period_1961_1990',
        'ensemble_member': 'r1i1p1f1',
        'experiment': [
            'historical', 'ssp1_2_6', 'ssp2_4_5',
            'ssp3_7_0', 'ssp5_8_5',
        ],
        'temporal_aggregation': 'yearly',
        'period': [
            '1850-2014', '2015-2100',
        ],
    },
    'download-mpi_esm1_2_lr.tar.gz')

c.retrieve(
    'sis-extreme-indices-cmip6',
    {
        'version': '2_0',
        'format': 'tgz',
        'model': 'noresm2_lm',
        'variable': [
            'cold_days', 'cold_nights', 'cold_spell_duration_index',
            'extremely_wet_day_precipitation', 'very_wet_day_precipitation', 'warm_days',
            'warm_nights', 'warm_spell_duration_index',
        ],
        'product_type': 'base_period_1961_1990',
        'ensemble_member': 'r1i1p1f1',
        'experiment': [
            'historical', 'ssp1_2_6', 'ssp2_4_5',
            'ssp3_7_0', 'ssp5_8_5',
        ],
        'temporal_aggregation': 'yearly',
        'period': [
            '1850-2014', '2015-2100',
        ],
    },
    'download-noresm2_lm.tar.gz')

c.retrieve(
    'sis-extreme-indices-cmip6',
    {
        'version': '2_0',
        'format': 'tgz',
        'model': 'access_esm1_5',
        'variable': [
            'cold_days', 'cold_nights', 'cold_spell_duration_index',
            'extremely_wet_day_precipitation', 'very_wet_day_precipitation', 'warm_days',
            'warm_nights', 'warm_spell_duration_index',
        ],
        'product_type': 'base_period_1961_1990',
        'ensemble_member': 'r1i1p1f1',
        'experiment': [
            'historical', 'ssp1_2_6', 'ssp2_4_5',
            'ssp3_7_0', 'ssp5_8_5',
        ],
        'temporal_aggregation': 'yearly',
        'period': [
            '1850-2014', '2015-2100',
        ],
    },
    'download-access_esm1_5.tar.gz')

c.retrieve(
    'sis-extreme-indices-cmip6',
    {
        'version': '2_0',
        'format': 'tgz',
        'model': 'cnrm_cm6_1_hr',
        'variable': [
            'cold_days', 'cold_nights', 'cold_spell_duration_index',
            'extremely_wet_day_precipitation', 'very_wet_day_precipitation', 'warm_days',
            'warm_nights', 'warm_spell_duration_index',
        ],
        'product_type': 'base_period_1961_1990',
        'ensemble_member': 'r1i1p1f2',
        'experiment': [
            'historical', 'ssp1_2_6', 'ssp5_8_5',
        ],
        'temporal_aggregation': 'yearly',
        'period': [
            '1850-2014', '2015-2100',
        ],
    },
    'download-cnrm_cm6_1_hr.tar.gz')

c.retrieve(
    'sis-extreme-indices-cmip6',
    {
        'version': '2_0',
        'format': 'tgz',
        'model': 'ec_earth3',
        'variable': [
            'cold_days', 'cold_nights', 'cold_spell_duration_index',
            'extremely_wet_day_precipitation', 'very_wet_day_precipitation', 'warm_days',
            'warm_nights', 'warm_spell_duration_index',
        ],
        'product_type': 'base_period_1961_1990',
        'ensemble_member': 'r1i1p1f1',
        'experiment': [
            'historical', 'ssp1_2_6', 'ssp2_4_5',
            'ssp3_7_0', 'ssp5_8_5',
        ],
        'temporal_aggregation': 'yearly',
        'period': [
            '1850-2014', '2015-2100',
        ],
    },
    'download-ec_earth3.tar.gz')

c.retrieve(
    'sis-extreme-indices-cmip6',
    {
        'version': '2_0',
        'format': 'tgz',
        'model': 'gfdl_cm4',
        'variable': [
            'cold_days', 'cold_nights', 'cold_spell_duration_index',
            'extremely_wet_day_precipitation', 'very_wet_day_precipitation', 'warm_days',
            'warm_nights', 'warm_spell_duration_index',
        ],
        'product_type': 'base_period_1961_1990',
        'ensemble_member': 'r1i1p1f1',
        'experiment': [
            'historical', 'ssp2_4_5', 'ssp5_8_5',
        ],
        'temporal_aggregation': 'yearly',
        'period': [
            '1850-2014', '2015-2100',
        ],
    },
    'download-gfdl_cm4.tar.gz')

c.retrieve(
    'sis-extreme-indices-cmip6',
    {
        'version': '2_0',
        'format': 'tgz',
        'model': 'hadgem3_gc31_mm',
        'variable': [
            'cold_days', 'cold_nights', 'cold_spell_duration_index',
            'extremely_wet_day_precipitation', 'very_wet_day_precipitation', 'warm_days',
            'warm_nights', 'warm_spell_duration_index',
        ],
        'product_type': 'base_period_1961_1990',
        'ensemble_member': 'r1i1p1f3',
        'experiment': [
            'historical', 'ssp1_2_6', 'ssp5_8_5',
        ],
        'temporal_aggregation': 'yearly',
        'period': [
            '1850-2014', '2015-2100',
        ],
    },
    'download-hadgem3_gc31_mm.tar.gz')

c.retrieve(
    'sis-extreme-indices-cmip6',
    {
        'version': '2_0',
        'format': 'tgz',
        'model': 'kace_1_0_g',
        'variable': [
            'cold_days', 'cold_nights', 'cold_spell_duration_index',
            'extremely_wet_day_precipitation', 'very_wet_day_precipitation', 'warm_days',
            'warm_nights', 'warm_spell_duration_index',
        ],
        'product_type': 'base_period_1961_1990',
        'ensemble_member': 'r1i1p1f1',
        'experiment': [
            'historical', 'ssp1_2_6', 'ssp2_4_5',
            'ssp3_7_0', 'ssp5_8_5',
        ],
        'temporal_aggregation': 'yearly',
        'period': [
            '1850-2014', '2015-2100',
        ],
    },
    'download-kace_1_0_g.tar.gz')

c.retrieve(
    'sis-extreme-indices-cmip6',
    {
        'version': '2_0',
        'format': 'tgz',
        'model': 'miroc6',
        'variable': [
            'cold_days', 'cold_nights', 'cold_spell_duration_index',
            'extremely_wet_day_precipitation', 'very_wet_day_precipitation', 'warm_days',
            'warm_nights', 'warm_spell_duration_index',
        ],
        'product_type': 'base_period_1961_1990',
        'ensemble_member': 'r1i1p1f1',
        'experiment': [
            'historical', 'ssp1_2_6', 'ssp2_4_5',
            'ssp3_7_0', 'ssp5_8_5',
        ],
        'temporal_aggregation': 'yearly',
        'period': [
            '1850-2014', '2015-2100',
        ],
    },
    'download-miroc6.tar.gz')

c.retrieve(
    'sis-extreme-indices-cmip6',
    {
        'version': '2_0',
        'format': 'tgz',
        'model': 'mri_esm2_0',
        'variable': [
            'cold_days', 'cold_nights', 'cold_spell_duration_index',
            'extremely_wet_day_precipitation', 'very_wet_day_precipitation', 'warm_days',
            'warm_nights', 'warm_spell_duration_index',
        ],
        'product_type': 'base_period_1961_1990',
        'ensemble_member': 'r1i1p1f1',
        'experiment': [
            'historical', 'ssp1_2_6', 'ssp2_4_5',
            'ssp3_7_0', 'ssp5_8_5',
        ],
        'temporal_aggregation': 'yearly',
        'period': [
            '1850-2014', '2015-2100',
        ],
    },
    'download-mri_esm2_0.tar.gz')

c.retrieve(
    'sis-extreme-indices-cmip6',
    {
        'version': '2_0',
        'format': 'tgz',
        'model': 'noresm2_mm',
        'variable': [
            'cold_days', 'cold_nights', 'cold_spell_duration_index',
            'extremely_wet_day_precipitation', 'very_wet_day_precipitation', 'warm_days',
            'warm_nights', 'warm_spell_duration_index',
        ],
        'product_type': 'base_period_1961_1990',
        'ensemble_member': 'r1i1p1f1',
        'experiment': [
            'historical', 'ssp1_2_6', 'ssp2_4_5',
            'ssp3_7_0', 'ssp5_8_5',
        ],
        'temporal_aggregation': 'yearly',
        'period': [
            '1850-2014', '2015-2100',
        ],
    },
    'download-noresm2_mm.tar.gz')

c.retrieve(
    'sis-extreme-indices-cmip6',
    {
        'version': '2_0',
        'format': 'tgz',
        'model': 'bcc_csm2_mr',
        'variable': [
            'cold_days', 'cold_nights', 'cold_spell_duration_index',
            'extremely_wet_day_precipitation', 'very_wet_day_precipitation', 'warm_days',
            'warm_nights', 'warm_spell_duration_index',
        ],
        'product_type': 'base_period_1961_1990',
        'ensemble_member': 'r1i1p1f1',
        'experiment': [
            'historical', 'ssp1_2_6', 'ssp2_4_5',
            'ssp3_7_0', 'ssp5_8_5',
        ],
        'temporal_aggregation': 'yearly',
        'period': [
            '1850-2014', '2015-2100',
        ],
    },
    'download-bcc_csm2_mr.tar.gz')

c.retrieve(
    'sis-extreme-indices-cmip6',
    {
        'version': '2_0',
        'format': 'tgz',
        'model': 'cnrm_esm2_1',
        'variable': [
            'cold_days', 'cold_nights', 'cold_spell_duration_index',
            'extremely_wet_day_precipitation', 'very_wet_day_precipitation', 'warm_days',
            'warm_nights', 'warm_spell_duration_index',
        ],
        'product_type': 'base_period_1961_1990',
        'ensemble_member': 'r1i1p1f2',
        'experiment': [
            'historical', 'ssp1_2_6', 'ssp2_4_5',
            'ssp3_7_0', 'ssp5_8_5',
        ],
        'temporal_aggregation': 'yearly',
        'period': [
            '1850-2014', '2015-2100',
        ],
    },
    'download-cnrm_esm2_1.tar.gz')

c.retrieve(
    'sis-extreme-indices-cmip6',
    {
        'version': '2_0',
        'format': 'tgz',
        'model': 'ec_earth3_veg',
        'variable': [
            'cold_days', 'cold_nights', 'cold_spell_duration_index',
            'extremely_wet_day_precipitation', 'very_wet_day_precipitation', 'warm_days',
            'warm_nights', 'warm_spell_duration_index',
        ],
        'product_type': 'base_period_1961_1990',
        'ensemble_member': 'r1i1p1f1',
        'experiment': [
            'historical', 'ssp1_2_6', 'ssp2_4_5',
            'ssp3_7_0', 'ssp5_8_5',
        ],
        'temporal_aggregation': 'yearly',
        'period': [
            '1850-2014', '2015-2100',
        ],
    },
    'download-ec_earth3_veg.tar.gz')

c.retrieve(
    'sis-extreme-indices-cmip6',
    {
        'version': '2_0',
        'format': 'tgz',
        'model': 'gfdl_esm4',
        'variable': [
            'cold_days', 'cold_nights', 'cold_spell_duration_index',
            'extremely_wet_day_precipitation', 'very_wet_day_precipitation', 'warm_days',
            'warm_nights', 'warm_spell_duration_index',
        ],
        'product_type': 'base_period_1961_1990',
        'ensemble_member': 'r1i1p1f1',
        'experiment': [
            'historical', 'ssp1_2_6', 'ssp2_4_5',
            'ssp3_7_0', 'ssp5_8_5',
        ],
        'temporal_aggregation': 'yearly',
        'period': [
            '1850-2014', '2015-2100',
        ],
    },
    'download-gfdl_esm4.tar.gz')


c.retrieve(
    'sis-extreme-indices-cmip6',
    {
        'version': '2_0',
        'format': 'tgz',
        'model': 'inm_cm4_8',
        'variable': [
            'cold_days', 'cold_nights', 'cold_spell_duration_index',
            'extremely_wet_day_precipitation', 'very_wet_day_precipitation', 'warm_days',
            'warm_nights', 'warm_spell_duration_index',
        ],
        'product_type': 'base_period_1961_1990',
        'ensemble_member': 'r1i1p1f1',
        'experiment': [
            'historical', 'ssp1_2_6', 'ssp2_4_5',
            'ssp3_7_0', 'ssp5_8_5',
        ],
        'temporal_aggregation': 'yearly',
        'period': [
            '1850-2014', '2015-2100',
        ],
    },
    'download-inm_cm4_8.tar.gz')

c.retrieve(
    'sis-extreme-indices-cmip6',
    {
        'version': '2_0',
        'format': 'tgz',
        'model': 'kiost_esm',
        'variable': [
            'cold_days', 'cold_nights', 'cold_spell_duration_index',
            'extremely_wet_day_precipitation', 'very_wet_day_precipitation', 'warm_days',
            'warm_nights', 'warm_spell_duration_index',
        ],
        'product_type': 'base_period_1961_1990',
        'ensemble_member': 'r1i1p1f1',
        'experiment': [
            'historical', 'ssp1_2_6', 'ssp2_4_5',
            'ssp5_8_5',
        ],
        'temporal_aggregation': 'yearly',
        'period': [
            '1850-2014', '2015-2100',
        ],
    },
    'download-kiost_esm.tar.gz')

c.retrieve(
    'sis-extreme-indices-cmip6',
    {
        'version': '2_0',
        'format': 'tgz',
        'model': 'mpi_esm1_2_hr',
        'variable': [
            'cold_days', 'cold_nights', 'cold_spell_duration_index',
            'extremely_wet_day_precipitation', 'very_wet_day_precipitation', 'warm_days',
            'warm_nights', 'warm_spell_duration_index',
        ],
        'product_type': 'base_period_1961_1990',
        'ensemble_member': 'r1i1p1f1',
        'experiment': [
            'historical', 'ssp1_2_6', 'ssp2_4_5',
            'ssp3_7_0', 'ssp5_8_5',
        ],
        'temporal_aggregation': 'yearly',
        'period': [
            '1850-2014', '2015-2100',
        ],
    },
    'download-mpi_esm1_2_hr.tar.gz')

c.retrieve(
    'sis-extreme-indices-cmip6',
    {
        'version': '2_0',
        'format': 'tgz',
        'model': 'nesm3',
        'variable': [
            'cold_days', 'cold_nights', 'cold_spell_duration_index',
            'extremely_wet_day_precipitation', 'very_wet_day_precipitation', 'warm_days',
            'warm_nights', 'warm_spell_duration_index',
        ],
        'product_type': 'base_period_1961_1990',
        'ensemble_member': 'r1i1p1f1',
        'experiment': [
            'historical', 'ssp1_2_6', 'ssp2_4_5',
            'ssp5_8_5',
        ],
        'temporal_aggregation': 'yearly',
        'period': [
            '1850-2014', '2015-2100',
        ],
    },
    'download-nesm3.tar.gz')

c.retrieve(
    'sis-extreme-indices-cmip6',
    {
        'version': '2_0',
        'format': 'tgz',
        'model': 'ukesm1_0_ll',
        'variable': [
            'cold_days', 'cold_nights', 'cold_spell_duration_index',
            'extremely_wet_day_precipitation', 'very_wet_day_precipitation', 'warm_days',
            'warm_nights', 'warm_spell_duration_index',
        ],
        'product_type': 'base_period_1961_1990',
        'ensemble_member': 'r1i1p1f2',
        'experiment': [
            'historical', 'ssp1_2_6', 'ssp2_4_5',
            'ssp3_7_0', 'ssp5_8_5',
        ],
        'temporal_aggregation': 'yearly',
        'period': [
            '1850-2014', '2015-2100',
        ],
    },
    'download-ukesm1_0_ll.tar.gz')
    

            
            
        
        
        
        
    

        
        
        

        
    
    
