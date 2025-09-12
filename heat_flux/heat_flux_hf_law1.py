"""
@file heat_flux_hf_law1.py

@brief Compute stagnation heat flux using the Fay-Riddell law.

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
#   HEAT_FLUX_HF_LAW1.PY, v2.0.0, December 2024, Domenico Lanza.
#.................................................
#   This module is needed to compute the 
#   heat flux for the heat flux law hf_law=1,
#   the Fay-Riddell heat flux law
#.................................................
import math # Math library

def heat_flux(probes, P_e, T_e, u, mixture_object):
    """This function computes the stagnation heat flux
    for the Fay-Riddell heat flux law.

    Args:
        probes (probes_class): the probes object containing the probe properties
        P_e (float): the static pressure at the edge
        T_e (float): the static temperature at the edge
        u (float): the freestream velocity of the flow
        mixture_object (mpp.Mixture): the Mutation++ mixture object

    Returns:
        q (float): the stagnation heat flux
    """
    # Variables:
    T_w = probes.T_w  # Wall temperature
    # Computation at the edge:
    mixture_object.equilibrate(T_e, P_e)
    rho_e = mixture_object.density()  # Edge density
    mu_e = mixture_object.viscosity()  # Edge viscosity
    h_e = mixture_object.mixtureHMass()  # Edge enthalpy
    # Computation at the wall:
    mixture_object.equilibrate(T_w, P_e)
    rho_w = mixture_object.density()  # Wall density
    mu_w = mixture_object.viscosity()  # Wall viscosity
    C_p_w = mixture_object.mixtureEquilibriumCpMass()  # Wall specific heat at constant pressure
    lambda_eq_w = mixture_object.equilibriumThermalConductivity()  # Wall equilibrium thermal conductivity
    h_w = mixture_object.mixtureHMass()  # Wall enthalpy
    Pr_w = mu_w * C_p_w / lambda_eq_w  # Prandtl number at the wall
    beta = probes.stag_var * u/probes.R_m  # Velocity gradient 
    # Heat flux computation:
    q = 0.76* pow(Pr_w, -0.6) * pow(rho_e * mu_e, 0.4)* pow(rho_w * mu_w, 0.1) * math.sqrt(beta) * (h_e - h_w)
    return q
#.................................................
#   Possible improvements:
#   - Check correctness of the heat flux law
#.................................................
#   KNOW PROBLEMS: 
#   None
#.................................................
    