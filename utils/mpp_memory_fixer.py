"""
@file mpp_memory_fixer.py

@brief Temporary workaround for Mutation++ memory leak.

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
#   MPP_MEMORY_FIXER.PY, v2.0.0, April 2024, Domenico Lanza.
#.................................................
#   This module is needed to temporarily fix a memory leak in the MPP library.
#.................................................

import mutationpp as mpp
import os

from utils.classes import ProgramConstants

def create_mixture_file(mixture_name):
    """This function is used to create a mixture file.

    Args:
        mixture_name (str): The name of the mixture, without the extension (".xml")
    """
    # Create the mixture file
    filename = mixture_name + ".xml"
    try:
        f = open(filename, "w")
    except:
        print("Error: Unable to create the mixture file.")
        return False
    # Write the mixture
    f.write("<!-- Temporary mixture-->\n")
    f.write("<mixture state_model=\"EquilTP\">\n")
    f.write("\t<species>\n")
    f.write("\t\tN2 N2+ N N+ e-\n")
    f.write("\t</species>\n")
    f.write("\t\n")
    f.write("\t<element_compositions default=\"default\">\n")
    f.write("\t\t<composition name=\"default\"> N2:1.0, N2+:0.0, N:0.0, N+:0.0, e-:0.0 </composition>\n")
    f.write("\t</element_compositions>\n")
    f.write("</mixture>\n")
    f.close()
    return True
    
def delete_mixture_file(mixture_name):  
    """This function is used to delete the mixture file.

    Args:
        mixture_name (str): The name of the mixture, without the extension (".xml")
    """
    # Delete the file
    filename = mixture_name + ".xml"
    try:
        os.remove(filename)
    except:
        pass

def fix_mpp_memory_leak():
    """This function is needed to temporarily fix a memory leak in the MPP library.
    """
    # Constants
    program_constants = ProgramConstants()
    MIXTURE_NAME = program_constants.TemporaryFiles.TEMP_MIXTURE_NAME
    # Create the mixture file
    if(create_mixture_file(MIXTURE_NAME) == False):
        print("Error: Unable to create the mixture file.")
        print("Memory leak in the MPP library could happen.")
        return
    # Create the Mixture object
    mix = mpp.Mixture(MIXTURE_NAME)
    # Delete the mixture file
    delete_mixture_file(MIXTURE_NAME)
#.................................................
#   Possible improvements:
#   - Indagate the memory leak in the MPP library.
#.................................................
#   KNOW PROBLEMS:
#   None.
#.................................................