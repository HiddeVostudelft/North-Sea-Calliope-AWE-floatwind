#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 15:06:29 2022

@author: fl
"""
import calliope
import create_input


path_to_model_yaml = '2050/model/national/model-2015.yaml'
scenarios_string = 'res_24h,no-nuclear-cap-max'
path_to_netcdf_of_model_inputs = '2050/national/inputs.nc'
create_input.build_model(path_to_model_yaml, scenarios_string, path_to_netcdf_of_model_inputs)

import run
path_to_netcdf_of_results = 'results/test_results.nc'
run.run_model(path_to_netcdf_of_model_inputs, path_to_netcdf_of_results)

model_results = calliope.read_netcdf('results/test_results.nc')
nuclear_GBR = model_results.get_formatted_array('energy_cap').loc[{'techs':'nuclear'}].to_pandas()
model_data = model_results.get_formatted_array('energy_cap_max').loc[{'techs':'nuclear'}].to_pandas()
