#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 13:13:05 2023

@author: hidde
"""

import create_input
import run
import calliope
import pandas as pd
# from create_override import cap_results_to_override
from utils import duals_to_pickle, load_duals, process_system_balance_duals
# import matplotlib.pyplot as plt
# import sys

# sys.stdout = open('console_log.txt', 'w')
calliope.set_log_verbosity('INFO') #sets the level of verbosity of Calliope's operations

#%% 
# CREATING MODEL INPUTS
###

# Select optimisation horizon: 2020, 2030 or 2050
opt_horizon = 2050
path_to_model_yaml = '{}/model/national/model-2015.yaml'.format(opt_horizon)

# Define scenarios
scenario_string = {}

scenario_string['2050_2_8'] = "industry_fuel,transport,heat,config_overrides,res_1h,gas_storage,"\
                        "link_cap_dynamic,freeze-hydro-capacities,add-biofuel,synfuel_transmission,"\
                        "north_sea,scenario_2050_2_8,floatwind_cap_max,offshorewind_cap_max,onshorewind_cap_min"

selected_scenario = '2050_2_8' 
# Generate and save model inputs
path_to_netcdf_of_model_inputs = '{}/national/inputs_2050_2_8.nc'.format(opt_horizon)
model_input = create_input.build_model(path_to_model_yaml, scenario_string[selected_scenario], path_to_netcdf_of_model_inputs)

#%%
# RUNNING THE MODEL & saving results (including duals)
###

path_to_netcdf_of_results = 'results/north-sea_{}.nc'.format(selected_scenario)
model_run, duals = run.run_model(model_input, path_to_netcdf_of_results)
