"""
@file continuity.py

@brief Integrate continuity equation dV/deta = -F using Simpson's rule.

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
#   CONTINUITY.PY, v2.0.0, December 2024, Domenico Lanza.
#.................................................
#   This module is needed to solve the continuity equation: dV/deta=-F
#.................................................
def continuity(deta, y): 
    """This function solves the continuity equation: dV/deta=-F
    by using a Simpson numerical integration.

    Args:
        deta (float): step for the numerical integration
        y (array): function to integrate

    Returns:
        V (float): integral of y (array)
    """
    # Initialization
    V = [] 
    # Integration
    V.append(0)  # Boundary condition
    # Simpson rule:
    V.append( (17*y[0]+42*y[1]-16*y[2]+6*y[3]-y[4])*deta/48 )
    for i in range(2,len(y)):
        V.append(V[i-2]+(y[i-2]+4*y[i-1]+y[i])*deta/3) 
    return V
#.................................................
#   Possible improvements:
#   -Implement a more efficient integration method
#.................................................
#   KNOW PROBLEMS:
#   None.
#.................................................