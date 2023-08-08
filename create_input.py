#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import calliope


def build_model(path_to_model, scenario, path_to_output):

    calliope.set_log_verbosity("info", include_solver_output=True, capture_warnings=True)
    model = calliope.Model(path_to_model, scenario=scenario)

    model._model_data.attrs["scenario"] = scenario

    # model.to_netcdf(path_to_output)
    
    return (model)

