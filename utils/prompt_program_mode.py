"""
@file prompt_program_mode.py

@brief Prompt user to select execution mode.

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
#   PROMPT_PROGRAM_MODE.PY, v2.0.0, December 2024, Domenico Lanza.
#.................................................
#   This module contains the prompt_program_mode() function.
#   This function prompts the user to select the program mode.
#   The user can choose between the following modes:
#   -Single run: the program runs a single case, from a .srun file
#   -Excel run: the program reads the inputs from a .xlsx file
#   -File run: the program reads the input from a .in file, and the settings from a .pfs file
#.................................................
def is_int(s):
    """This function checks if the input is an integer.

    Args:
        s : variable to check

    Returns:
        Boolean: True if the input is an integer, False otherwise
    """
    try: 
        int(s)
        return True
    except:
        return False

def prompt_program_mode():
    """This function prompt the user to choose the program mode.

    Returns:
        program_mode (int): the program mode
    """
    # Prompt the user to select the program mode
    print("Please select the program mode:")
    print("1: Single run (.srun file)")
    print("2: Excel run (.xlsx file)")
    print("3: File run (.in file + .pfs file)")
    program_mode = input("Please enter your choice: ")
    # Check if the input is valid
    while ( (is_int(program_mode) == False) or (int(program_mode) != 1 and int(program_mode) != 2 and int(program_mode) != 3)):
        print("Invalid choice. Please enter 1, 2 or 3.")
        program_mode = input("Please enter your choice: ")
    # Return the program mode
    program_mode = int(program_mode)
    return program_mode
#.................................................
#   Possible improvements:
#   None.
#.................................................
#   KNOW PROBLEMS:
#   None.
#.................................................