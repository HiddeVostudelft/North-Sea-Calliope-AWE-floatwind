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
path_to_model_yaml = '{}/model/national/model-2014.yaml'.format(opt_horizon)

# Define scenarios
scenario_string = {}

scenario_string['2050_2_11'] = "industry_fuel,transport,heat,config_overrides,res_12h,gas_storage,"\
                        "link_cap_dynamic,freeze-hydro-capacities,add-biofuel,synfuel_transmission,"\
                        "north_sea,scenario_2050_2_11,floatwind_cap_max,offshorewind_cap_max,onshorewind_cap_min"

selected_scenario = '2050_2_11' 
# Generate and save model inputs
path_to_netcdf_of_model_inputs = '{}/national/inputs_2050_2_11_test.nc'.format(opt_horizon)
model_input = create_input.build_model(path_to_model_yaml, scenario_string[selected_scenario], path_to_netcdf_of_model_inputs)

#%%
# RUNNING THE MODEL & saving results (including duals)
###

path_to_netcdf_of_results = 'results/north-sea_{}_test.nc'.format(selected_scenario)
model_run, duals = run.run_model(model_input, path_to_netcdf_of_results)

model = calliope.read_netcdf('results/north-sea_2050_2_11_test.nc')
# duals = load_duals(path_to_duals)
transmissionplot=model.plot.transmission()
# For example, installed capacities per location (country)

# The timeseries plot can be also helpful to understand what's happening overall
model.plot.timeseries(subset={'costs':'monetary'})

# lcoes = model.results.systemwide_levelised_cost.loc[{'carriers': 'electricity', 'costs':'monetary'}].to_pandas()
lcoe_system=model.plot.capacity(subset={'costs':'monetary'})


# caps_per_country = model.get_formatted_array('energy_cap').to_pandas().fillna(0)*1e2
# caps_per_country = caps_per_country.where(caps_per_country> 1e-6,0)
# sup = caps_per_country # shorter name for easier code   
# sup['hydro'] = sup[['hydro_reservoir', 'hydro_run_of_river']].sum(axis=1)
# sup = sup.drop(['hydro_reservoir', 'hydro_run_of_river'], axis=1)
# sup['synfuel imports'] = sup[['syn_diesel_distribution_import','syn_methanol_distribution_import',
#         'syn_methane_distribution_import', 'syn_kerosene_distribution_import']].sum(axis=1)
# sup = sup.drop(['syn_diesel_distribution_import','syn_methanol_distribution_import',
#         'syn_methane_distribution_import', 'syn_kerosene_distribution_import'], axis=1)
# sup['solar'] = sup[['roof_mounted_pv','open_field_pv']].sum(axis=1)
# sup = sup.drop(['roof_mounted_pv','open_field_pv'],axis=1)
# sup['wind onshore'] = sup[['wind_onshore_competing']].sum(axis=1)
# sup = sup.drop(['wind_onshore_competing'],axis=1)
# sup['biofuel & waste'] = sup[['biofuel_supply','waste_supply']].sum(axis=1)
# sup = sup.drop(['biofuel_supply','waste_supply'],axis=1)
# sup=sup.iloc[:,[10,11,12,13,14,90,91,92,94,95,96]]
# axes = sup.plot.bar(figsize=(10,10), stacked=True, colormap='tab20c', title='scenario2')
# axes.legend()
# plt.ylabel('GW')
