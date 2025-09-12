"""
@file thermodyn.py

@brief Compute enthalpy and entropy from pressure and temperature.

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
#   THERMODYN.PY, v2.0.0, December 2024, Domenico Lanza.
#.................................................
#   This module is needed to compute the enthalpy 
#   and entropy given the pressure and the temperature.
#.................................................

def enthalpy(mixture_object, P, T):
    """This function returns the enthalpy of the fluid 
    given the pressure and the temperature.

    Args:
        mixture_object (mpp.Mixture): the mixture of the case
        P (float): pressure
        T (float): temperature

    Returns:
        h (float): enthalpy
    """
    # Compute the enthalpy:
    mixture_object.equilibrate(T, P)  # I equilibrate the mixture
    h = mixture_object.mixtureHMass() # I compute the enthalpy
    return h

def entropy(mixture_object, P, T): 
    """This function returns the entropy of the fluid 
    given the pressure and the temperature.

    Args:
        mixture_object (mpp.Mixture): the mixture of the case
        P (float): pressure
        T (float): temperature
    Returns:
        s (float): entropy
    """
    # Compute the entropy:
    mixture_object.equilibrate(T, P)  # I equilibrate the mixture
    s = mixture_object.mixtureSMass()  # I compute the entropy
    return s 
#.................................................
#   Possible improvements:
#   None.
#.................................................
#   KNOW PROBLEMS:
#   None.
#.................................................