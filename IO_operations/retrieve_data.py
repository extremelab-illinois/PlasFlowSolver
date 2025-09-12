"""
@file retrieve_data.py

@brief Wrapper to retrieve data for current case based on mode.

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
#   RETRIEVE_DATA.PY, v2.0.0, December 2024, Domenico Lanza.
#.................................................
#   This module is needed to retrieve the needed
#   data from the dataframe object for the current case in the program loop.
#.................................................
from utils.exit_program import exit_program  # Function to exit the program
import IO_operations.retrieve_data_srun as retrieve_data_srun_file  # Module to retrieve the data from the .srun file
import IO_operations.retrieve_data_xlsx as retrieve_data_xlsx_file  # Module to retrieve the data from the .xlsx file
import IO_operations.retrieve_data_filerun as retrieve_data_filerun_file  # Module to retrieve the data from the .in and .pfs files
from IO_operations.retrieve_helper import retrieve_converted_inputs  # Function to retrieve the converted inputs

def retrieve_data(df_object, program_mode, n_case):
    """This function retrieves the needed data from the dataframe object
    for the current case in the program loop.
    
    Args:
        df_object (pandas.DataFrame): the dataframe object
        program_mode (int): the program mode
        n_case (int): the case number
    
    Returns:
        inputs_object (object): the inputs object
        initials_object (object): the initials object
        probes_object (object): the probes object
        settings_object (object): the settings object
        warnings (list): the warnings list
    """
    
    if (program_mode == 1):  # .srun run
        try:
            inputs_object, initials_object, probes_object, settings_object, warnings = retrieve_data_srun_file.retrieve_data(df_object)
        except Exception as e:
            raise Exception(e)  # Handled in the main program
    elif (program_mode == 2):  # .xlsx run
        try:
            inputs_object, initials_object, probes_object, settings_object, warnings = retrieve_data_xlsx_file.retrieve_data(df_object, n_case)
        except Exception as e:
            print("Error while retrieving the data from the dataframe: "+str(e))
            print("The case number " + str(n_case+1) + " will be skipped.")
            raise Exception(e)
    elif (program_mode == 3):  # File run
        try:
            inputs_object, initials_object, probes_object, settings_object, warnings = retrieve_data_filerun_file.retrieve_data(df_object, n_case)
        except Exception as e:
            print("Error while retrieving the data from the dataframe: "+str(e))
            print("The case number " + str(n_case+1) + " will be skipped.")
            raise Exception(e)
    else:
        print("ERROR: Invalid program mode. You should never see this message...")
        print("The program will now terminate")
        exit_program()
    # Units conversion (same for all the cases):
    inputs_object, initials_object, probes_object = retrieve_converted_inputs(inputs_object, initials_object, probes_object)
    # Return:
    return inputs_object, initials_object, probes_object, settings_object, warnings 
#.................................................
#   Possible improvements:
#   - More specific exceptions
#.................................................
#   KNOW PROBLEMS:
#   -None
#.................................................
    