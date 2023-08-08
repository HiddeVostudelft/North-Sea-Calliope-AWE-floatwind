#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 23 17:57:15 2022

@author: fl
"""

from ruamel.yaml import YAML

yaml = YAML()

#%%

HARDCODED_LINK_DIRECTIONS = ["BEL,DEU","BEL,GBR", "BEL,LUX", "BEL,NLD", "DEU,DNK",
                             "DEU,NOR", "DEU,SWE", "DNK,NOR", "DNK,SWE", "FRA,BEL",
                             "FRA,DEU", "FRA,GBR", "FRA,IRL", "GBR,DEU", "GBR,DNK", 
                             "GBR,IRL", "NLD,DEU", "NLD,DNK", "NLD,GBR", "NLD,NOR", 
                             "NOR,GBR", "NOR,SWE"]

#%%
def cap_results_to_override(caps_per_country):
    countries = caps_per_country.index
    override_dict = {'overrides':{'freeze-capacity-results':{'locations':{}}}}
    techs = [x for x in caps_per_country.columns if 'transmission' not in x and 
             'demand' not in x and 'hydro' not in x and 'methane_storage' not in x and
             '_distribution' not in x]
    links = [x for x in caps_per_country.columns if 'transmission' in x]
    
    # Fixing generation, storage and conversion caps
    for loc in countries:
        override_dict['overrides']['freeze-capacity-results']['locations'][loc+'.techs'] = {}
        for tech in techs:
            override_dict['overrides']['freeze-capacity-results']['locations'][loc+'.techs'][tech] = {}
            override_dict['overrides']['freeze-capacity-results']['locations'][loc+'.techs'][tech]['constraints'] = {}
            if caps_per_country[tech].loc[loc] > 0.001: #filter out noise, i.e. very small numbers
                override_dict['overrides']['freeze-capacity-results']['locations'][loc+'.techs'][tech]['constraints']['energy_cap_equals'] = float(caps_per_country[tech].loc[loc])
            else:
                override_dict['overrides']['freeze-capacity-results']['locations'][loc+'.techs'][tech]['constraints']['energy_cap_equals'] = 0
    
    # Fixing transmission caps
    override_dict['overrides']['freeze-capacity-results']['links'] = {}
    for loc in countries:
        for tech in links:
            end_node = ''.join([c for c in tech if c.isupper()])
            pure_tech = ''.join([c for c in tech if not c.isupper()])
            if caps_per_country[tech].loc[loc] >= 0 and (loc+',{}'.format(end_node)) in HARDCODED_LINK_DIRECTIONS: # check if NaN
                override_dict['overrides']['freeze-capacity-results']['links'][loc+',{}.techs'.format(end_node)] = {}
                override_dict['overrides']['freeze-capacity-results']['links'][
                    loc+',{}.techs'.format(end_node)][pure_tech[:-1]+'.constraints.energy_cap_equals'] = float(caps_per_country[tech].loc[loc])
            else:
                continue   

    # Convert all into a YAML file
    yaml.default_flow_style = False
    yaml.width=1000
    with open('temp_overrides/freeze-plan-results.yaml', 'w') as outfile:
        yaml.dump(override_dict, outfile)
        
    with open("temp_overrides/freeze-plan-results.yaml", "r+") as f:
        contents = f.read()
        f.seek(0)
        f.write(contents.replace('"', ''))
        f.truncate()