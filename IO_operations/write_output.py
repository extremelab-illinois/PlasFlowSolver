"""
@file write_output.py

@brief Select appropriate writer based on run mode.

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
#   WRITE_OUTPUT.PY, v2.0.0, December 2024, Domenico Lanza.
#.................................................
#   This module is needed to write the output file.
#.................................................
import IO_operations.write_output_srun as write_output_srun_file  # Module to write the output file in a .srun run
import IO_operations.write_output_xlsx as write_output_xlsx_file  # Module to write the output file in a .xlsx run
import IO_operations.write_output_filerun as write_output_filerun_file  # Module to write the output file in a .in run
from utils.exit_program import exit_program  # Module to exit the program

def write_output(output_filename, out_object, program_mode, df_object):
    if program_mode == 1:  # Single run
        write_output_srun_file.write_output_srun(output_filename, out_object)
    elif program_mode == 2:  # xlsx run
        write_output_xlsx_file.write_output_xlsx(output_filename, out_object)
    elif program_mode == 3:  # File run
        write_output_filerun_file.write_output_filerun(df_object, output_filename, out_object)
    else:
        print("ERROR: Invalid program mode. You should never see this message...")
        print("The program will now terminate.")
        exit_program()
#.................................................
#   Possible improvements:
#   - Better structure for functions inputs.
#.................................................
#   Known problems:
#   None.
#.................................................