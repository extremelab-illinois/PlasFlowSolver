"""
@file heat_flux.py

@brief Dispatch heat flux calculations for available laws.

Copyright (C) 2023-2025 The Board of Trustees of the University of Illinois.
All rights reserved.

This file is part of PlasFlowSolver: a data reduction model for ICP wind tunnels.

PlasFlowSolver is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

PlasFlowSolver is distributed in the hope that it will be useful, 
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with PlasFlowSolver.  If not, see 
<http://www.gnu.org/licenses/>.
"""

#.................................................
#   HEAT_FLUX.PY, v2.0.0, December 2024, Domenico Lanza.
#.................................................
#   This module is needed to compute the heat flux
#   for different heat flux laws.
#.................................................

import heat_flux.heat_flux_hf_law0 as heat_flux_hf_law0_file  # Module to compute the heat flux with the exact heat flux law
import heat_flux.heat_flux_hf_law1 as heat_flux_hf_law1_file  # Module to compute the heat flux with the Fay-Riddell heat flux law

def heat_flux(probes, settings, P_t, T_t, u, mixture_object):
    """This function computes the stagnation
    heat flux of the flux with different heat flux laws.

    Args:
        probes (probes_class): the probes object containing the probe properties
        settings (settings_class): the settings object containing the program settings
        P_t (float): the total pressure at the stagnation point
        T_t (float): the total temperature at the stagnation point
        u (float): the freestream velocity of the flow
        mixture_object (mpp.Mixture): the Mutation++ mixture object

    Returns:
        q (float): the heat flux
    """
    # Retrieve the heat flux law
    hf_law = probes.hf_law
    bad_hf = False
    # Match the heat flux law
    match(hf_law):
        case 0:  # Exact heat flux law (boundary layer)
            q, bad_hf = heat_flux_hf_law0_file.heat_flux(probes, settings, P_t, T_t, u, mixture_object) 
        case 1:  # Fay-Riddell heat flux law
            q = heat_flux_hf_law1_file.heat_flux(probes, P_t, T_t, u, mixture_object)
            bad_hf = False
        case _:  # Heat flux law not implemented
            raise ValueError("The heat flux law is not valid. You should not see this message. Check retrieve_helper.py")
    return q, bad_hf
#.................................................
#   Possible improvements:
#   -Implement other heat flux laws.
#.................................................
#   KNOW PROBLEMS: Please refer to the specific heat flux law.
#.................................................