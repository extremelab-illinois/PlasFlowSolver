"""
@file system_solve.py

@brief Linear system solver for Newton-Raphson iterations.

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
#   SYSTEM_SOLVE.PY, v1.0.0, April 2024, Domenico Lanza.
#.................................................
#   This module is needed to solve the linear system
#   in order to use the Newton-Raphson's method.
#.................................................
import numpy as np  # Module for numerical operations
def system_solve(n, A, b):
    """Solves the linear system Ax=b using the linalg.solve function from the scipy library

    Args:
        n (int): number of equations
        A (list): matrix A
        b (list): vector b
    Raises:
        Exception: Error detected in system_solve.py, the linear system cannot be solved.

    Returns:
        x (float list): solution
    """
    # AA must be A[1:n,1:n]
    # bb must be b[1:n]
    # Extract AA and bb from A and b
    AA = [[0.0 for i in range(n)] for j in range(n)]
    bb = [0.0]*n
    for i in range(n):
        for j in range(n):
            AA[i][j] = A[i][j]
        bb[i] = b[i]
    # Solve the system by using the linalg.solve function
    try: 
        x = np.linalg.solve(AA, bb)
    except Exception as e:
        raise Exception("Error detected in system_solve.py, the linear system cannot be solved: " + str(e))
    return x 
#.................................................
#   Possible improvements:
#   - Improve the efficiency of the code
#.................................................
#   KNOW PROBLEMS:
#   None.
#.................................................