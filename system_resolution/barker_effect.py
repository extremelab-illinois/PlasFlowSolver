"""
@file barker_effect.py

@brief Evaluate Pitot pressure corrections using Barker effects.

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
#   BARKER_EFFECT.PY, v2.0.0, December 2024, Domenico Lanza.
#.................................................
#   This module is needed to compute the Barker effect.
#.................................................
import math  # Math library

def barker_effect(probes, mixture_object, P_t, P, T, u):
    """This function returns the barker pressure given the total pressure, 
    the static pressure, the temperature and the velocity.

    Args:
        probes (probes_class): probe properties
        mixture_object (mpp.Mixture): the mixture of the case
        P_t (float): total pressure
        P (float): pressure
        T (float): temperature
        u (float): velocity
    Returns:
        P_b (float): barker pressure
        Re (float): reynolds number
    """
    # Extract:
    barker_type = probes.barker_type  # Barker correction type
    R_p = probes.R_p  # Pitot external radius
    # Compute:
    mixture_object.equilibrate(T, P)
    rho = mixture_object.density() 
    mu = mixture_object.viscosity()
    # Compute Reynolds number
    Re = rho*u*(2*R_p)/mu 
    # Match the Barker type
    match (barker_type):
        case 0:  # No barker effect
            C_p = 0
        case 1:  # Homann's correction
            C_p = 6/(Re+0.455*math.sqrt(Re))
        case 2:  # Carleton's correction
            C_p = 1 + 8/(Re+0.5576*math.sqrt(Re))
        case _:
            print("Error: Barker's correction not yet implemented. You should not see this message. Check retrieve_helper.py")
            exit()
    # Barker pressure (stagnation pressure read instead of the total pressure)
    P_b = P_t + 0.5*rho*pow(u, 2)*C_p
    return P_b, Re
#.................................................
#   Possible improvements:
#   - Add other barker computations
#.................................................
#   KNOW PROBLEMS:
#   None.
#.................................................