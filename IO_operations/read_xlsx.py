"""
@file read_xlsx.py

@brief Read .xlsx input file into dataframe.

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
#   READ_XLSX.PY, v2.0.0, December 2024, Domenico Lanza.
#.................................................
#   This module is needed to read the
#   .xlsx (xlsx Run) file and create the the
#   dataframe object. In particular, the data
#   are extracted from the xlsx file, but not
#   retrieved(checked) except for pressure
#   consistency check. The rest is done in the
#   retrieve_data_xlsx.py module.
#.................................................
import pandas as pd  # Library to read the xlsx file
from utils.classes import DataframeClass  # Module that contains the classes used in the program
from utils.script_run import retrieve_filename  # Module for the script run

def prompt_input_file():
    """This function prompts the user and 
    returns the input filename.

    Returns:
        input_filename (string): the name of the input file
    """
    
    print("Please input the name of the xlsx file with the data.")
    input_file_name = input("Filename: ") 
    # I check if the extension is .xlsx, otherwise I add it
    if (input_file_name.endswith(".xlsx") == False): 
        input_file_name = input_file_name + ".xlsx"
    return input_file_name

def read_xlsx(script_run):
    """This function reads the dataframe from the xlsx file.
    
    Args:
        script_run (boolean): True if the bash.pfs file is present, False otherwise    

    Returns:
        df_object (dataframe_class): the dataframe from the xlsx file
        output_filename (string): the name of the output file
    """
    # Read the xlsx filename
    file_found = False
    if (script_run == True):  # If we are in script mode
        try:  # If we can read the file:
            input_filename = retrieve_filename()  # I retrieve the filename from the script.pfs file
            df = pd.read_excel(input_filename, engine="openpyxl", header=[0,1])  # I read the excel using pandas
            file_found = True 
        except:  # If we cannot read the file:
            print("Error: the file in script.pfs does not exist, is not an xlsx file, or cannot be read.")
            print("The program will continue in manual mode.")
    # If we are not in bash mode or the file is not found:
    while (file_found == False):
        input_filename = prompt_input_file()
        try:  # If we can read the file:
            df = pd.read_excel(input_filename, engine="openpyxl", header=[0,1])
            file_found = True
        except:
            print("Error: the file does not exist or is not an xlsx file.")
    output_filename = input_filename[:-5]+"_out.xlsx"  # I set the output filename
    # DATA EXTRACTION:
    # The excel is multiindex on the rows, I drop the first row level
    try: 
        df_dropped = df.droplevel(level=0, axis=1)  # I drop the first row level
    except:
        raise ValueError("Error: The excel file is not in the correct format. Cannot drop the first row level.")
    n = df_dropped.shape[0]  # Number of the test
    # INPUTS:
    # comment:
    comment = df_dropped['comment']
    # Pressure:
    P = df_dropped['P [kPa]']
    # Dynamic pressure:
    P_dyn = df_dropped['P_dyn [kPa]']
    # Stagnation pressure:
    P_stag = df_dropped['P_stag [kPa]']
    # Heat flux:
    q_target = df_dropped['q_target [W/cm^2]']
    # Plasma gas:
    plasma_gas = df_dropped['plasma_gas']
    # INITIAL CONDITIONS
    # Initial conditions database name:
    ic_db_name = df_dropped['ic_db_name']
    # Initial static temperature:
    T_0 = df_dropped['T_0 [K]']
    # Initial total temperature:
    T_t_0 = df_dropped['T_t_0 [K]']
    # Initial velocity:
    u_0 = df_dropped['u_0 [m/s]']
    # Initial total pressure:
    P_t_0 = df_dropped['P_t_0 [kPa]']
    # PROBE SETTINGS
    #Wall temperature:
    T_w = df_dropped['T_w [K]']
    # Pitot external radius:
    R_p = df_dropped['R_p [mm]'] 
    # Heat flux probe external radius:
    R_m = df_dropped['R_m [mm]'] 
    # Plasma jet radius:
    R_j = df_dropped['R_j [mm]'] 
    # Stagnation type:
    stag_type = df_dropped['stag_type'] 
    # Heat flux law:
    hf_law = df_dropped['hf_law'] 
    # Barker's correction type:
    barker_type = df_dropped['barker_type'] 
    # PROGRAM SETTINGS
    # Number of point for the boundary layer eta discretization:
    N_p = df_dropped['N_p']
    # Maximum number of iterations for the heat flux:
    max_hf_iter = df_dropped['max_hf_iter']
    # Convergence criteria for the heat flux:
    hf_conv = df_dropped['hf_conv']
    # Use previous iteration for the heat transfer:
    use_prev_ite = df_dropped['use_prev_ite'] 
    # Upper integration boundary for the normal coordinate of the boundary layer:
    eta_max = df_dropped['eta_max']
    # Log warning heat flux:
    log_warning_hf = df_dropped['log_warning_hf']
    # Convergence criteria for the Newton solver:
    newton_conv = df_dropped['newton_conv'] 
    # Maximum number of iterations for the Newton solver:
    max_newton_iter = df_dropped['max_newton_iter']
    # Jacobian finite difference epsilon:
    jac_diff = df_dropped['jac_diff']
    # Minimum value for the temperature used for relaxation:
    min_T_relax = df_dropped['min_T_relax [K]'] 
    # Maximum value for the temperature used for relaxation:
    max_T_relax = df_dropped['max_T_relax [K]']
    # I store the values in the dataframe object
    df_object = DataframeClass()  # The dataframe object to be returned
    df_object.n = n
    df_object.comment = comment
    df_object.P = P
    df_object.P_dyn = P_dyn
    df_object.P_stag = P_stag
    df_object.q_target = q_target
    df_object.plasma_gas = plasma_gas
    df_object.ic_db_name = ic_db_name
    df_object.T_0 = T_0
    df_object.T_t_0 = T_t_0
    df_object.u_0 = u_0
    df_object.P_t_0 = P_t_0
    df_object.T_w = T_w
    df_object.R_p = R_p
    df_object.R_m = R_m
    df_object.R_j = R_j
    df_object.stag_type = stag_type
    df_object.hf_law = hf_law
    df_object.barker_type = barker_type
    df_object.N_p = N_p
    df_object.max_hf_iter = max_hf_iter
    df_object.hf_conv = hf_conv
    df_object.use_prev_ite = use_prev_ite
    df_object.eta_max = eta_max
    df_object.log_warning_hf = log_warning_hf
    df_object.newton_conv = newton_conv
    df_object.max_newton_iter = max_newton_iter
    df_object.jac_diff = jac_diff
    df_object.min_T_relax = min_T_relax
    df_object.max_T_relax = max_T_relax
    return df_object, output_filename 
#.................................................
#   Possible improvements:
#   - Add getter and setter for the dataframe object
#   - Maybe drop the first row level directly in excel
#   -More error checking
#.................................................
#   Known problems:
#   - None
#.................................................