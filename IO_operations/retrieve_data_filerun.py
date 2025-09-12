"""
@file retrieve_data_filerun.py

@brief Extract inputs for file-run cases from dataframe.

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
#   RETRIEVE_DATA_FILERUN.PY, v2.0.0, December 2024, Domenico Lanza.
#.................................................
#   This module is needed to retrieve the needed
#   data from the dataframe object for the current loop
#   iteration using the filerun mode.
#.................................................
import utils.classes as classes_file  # Module with the classes
from IO_operations.retrieve_helper import retrieve_stag_var  # Function to retrieve the stagnation variable
from IO_operations.retrieve_helper import retrieve_ic  # Function to retrieve the initial conditions database

def retrieve_data(df, n_case):
    """This function retrieves the needed data 
    from the dataframe object from the current loop iteration
    for the filerun mode.

    Args:
        df (dataframe_class): the dataframe object
        n_case (int): the number of the current case

    Returns:
        inputs_class (inputs_class): the inputs object containing the inputs
        initials_class (initials_class): the initials object containing the initials
        probes_class (probes_class): the probes object containing the probes
        settings_class (settings_class): the settings object containing the settings
    """
    # Initialize the objects
    inputs_object = classes_file.Inputs()  
    initials_object = classes_file.Initials() 
    probes_object = classes_file.Probes() 
    settings_object = classes_file.Settings()
    warnings = ""
    # INPUTS:
    # Comment:
    comment = df.comment[n_case]  # comment (string)
    inputs_object.comment = comment
    # Pressure:
    try:
        P = float(df.P[n_case])  # Pressure (float)
    except:
        raise ValueError("Error: The static pressure value is not valid.")
    if (P<=0):
        raise ValueError("Error: The pressure value is negative or zero.")
    else:
        inputs_object.P = P 
    # Dynamic pressure:
    try:
        P_dyn = float(df.P_dyn[n_case])  # Dynamic pressure (float)
    except:
        raise ValueError("Error: The dynamic pressure value is not valid.")
    if (P_dyn<=0):
        raise ValueError("Error: The dynamic pressure value is negative or zero.")
    else:
        inputs_object.P_dyn = P_dyn
    # Heat flux:
    try:
        q_target = float(df.q_target[n_case])  # Heat flux (float)
    except: 
        raise ValueError("Error: The heat flux value is not valid.")
    if(q_target<=0):
        raise ValueError("Error: The heat flux value is negative or zero.")
    else:
        inputs_object.q_target = q_target
    # Plasma gas:
    plasma_gas = df.plasma_gas  # Plasma gas (string)
    inputs_object.mixture_name = plasma_gas  # Already managed in read_filerun.py
    # Stagnation pressure:
    inputs_object.P_stag = inputs_object.P + inputs_object.P_dyn  # Stagnation pressure (float)
    # Database name:
    ic_db_name = df.ic_db_name  # Initial conditions database name (string)
    # Initials:
    if (ic_db_name != ""):
        initials_object, warnings_int = retrieve_ic(
            ic_db_name, inputs_object.P, inputs_object.P_dyn, inputs_object.q_target,
            df.T_w, df.max_T_relax
            )
        if (warnings_int is not None):
            warnings += warnings_int
    else:
        T_0 = df.T_0  # Initial temperature (float)
        initials_object.T_0 = T_0 
        T_t_0 = df.T_t_0  # Initial total temperature (float)
        initials_object.T_t_0=T_t_0 
        u_0 = df.u_0  # Initial velocity (float)
        initials_object.u_0 = u_0  # Initial velocity (float)
        P_t_0 = df.P_t_0  # Initial total pressure (float)
        if (P_t_0 == 0):  # If the initial total pressure is zero we set it as the stagnation pressure
            P_t_0 = inputs_object.P_stag
        initials_object.P_t_0 = P_t_0 
    # Probe properties:
    # Wall temperature:
    T_w = df.T_w  # Wall temperature, float
    probes_object.T_w = T_w
    # Pitot probe external radius:
    R_p = df.R_p  #Pitot probe external radius (float)
    probes_object.R_p = R_p 
    # Flux probe external radius:
    R_m = df.R_m  #Flux probe external radius (float)
    probes_object.R_m = R_m  #Flux probe external radius (float)
    # Plasma jet radius:
    R_j = df.R_j  #Plasma jet radius (float)
    probes_object.R_j = R_j  
    # Stagnation type:
    stag_type = df.stag_type  #Stagnation type (integer)
    probes_object.stag_type = stag_type  # Already managed in read_filerun.py
    # Heat flux law:
    hf_law = df.hf_law  #Heat flux law (integer)
    probes_object.hf_law = hf_law  # Already managed in read_filerun.py
    # Barker's correction type:
    barker_type = df.barker_type  #Barker's correction type (integer)
    probes_object.barker_type = barker_type  # Already managed in read_filerun.py
    # Stagnation variable:
    stag_var = retrieve_stag_var(stag_type, R_m, R_j)  #Stagnation variable (float)
    probes_object.stag_var = stag_var
    # Settings:
    N_p = df.N_p  # Number of point for the boundary layer eta discretization (integer)
    settings_object.N_p = N_p 
    # Maximum number of iterations for the heat flux:
    max_hf_iter = df.max_hf_iter  #Maximum number of iterations for the heat flux (integer)
    settings_object.max_hf_iter = max_hf_iter 
    # Convergence criteria for the heat flux:
    hf_conv = df.hf_conv  #Convergence criteria for the heat flux (float)
    settings_object.hf_conv = hf_conv 
    # Use previous iteration for the heat transfer:
    use_prev_ite = df.use_prev_ite  #Use previous iteration for the heat transfer (integer)
    settings_object.use_prev_ite = use_prev_ite  # Already managed in read_filerun.py
    # Maximum value for the boundary layer eta:
    eta_max = df.eta_max  # Maximum value for the boundary layer eta (float)
    settings_object.eta_max = eta_max 
    # Log warning for when the heat flux does not converge:
    log_warning_hf = df.log_warning_hf  # Log warning for when the heat flux does not converge (integer)
    settings_object.log_warning_hf = log_warning_hf  # Already managed in read_filerun.py
    # Convergence criteria for the Newton solver:
    newton_conv = df.newton_conv  #Convergence criteria for the newton solver (float)
    settings_object.newton_conv = newton_conv 
    # Maximum number of iterations for the Newton solver:
    max_newton_iter = df.max_newton_iter  #Maximum number of iterations for the newton solver (integer)
    settings_object.max_newton_iter = max_newton_iter 
    # Jacobian finite difference epsilon
    jac_diff = df.jac_diff  # Jacobian finite difference epsilon (float)
    settings_object.jac_diff = jac_diff 
    # Minimum value for the temperature used for relaxation
    min_T_relax = df.min_T_relax  # Minimum value for the temperature used for relaxation (float)
    settings_object.min_T_relax = min_T_relax 
    # Maximum value for the temperature used for relaxation
    max_T_relax = df.max_T_relax  # Maximum value for the temperature used for relaxation (float)
    settings_object.max_T_relax = max_T_relax 
    # Check Barker's effect and initial total pressure consistency:
    if (probes_object.barker_type == 0 and initials_object.P_t_0 != inputs_object.P_stag):
        initials_object.P_t_0 = inputs_object.P_stag
        warnings += "P_t_0 not consistent with the Barker's correction, set to P_stag|"
    # Return the objects
    if (warnings != "" and warnings[-1] == "|"):  # Remove the last character if it is a "|"
        warnings = warnings[:-1]
    if (warnings == ""):
        warnings = "None"
    return inputs_object, initials_object, probes_object, settings_object, warnings
#.................................................
#   Possible improvements:
#   - Use getter and setter for the inputs, initials, probes and settings objects
#   - stagvar is being computed a lot of times uselessly
#   - Improve efficiency
#   - Better exception throwing
#.................................................
#   Known problems:
#   None.
#.................................................
