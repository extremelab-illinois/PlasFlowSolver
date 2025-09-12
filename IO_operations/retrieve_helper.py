"""
@file retrieve_helper.py

@brief Utility functions for retrieving and validating input data.

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
#   RETRIEVE_HELPER.PY, v2.0.0, December 2024, Domenico Lanza.
#.................................................
#   This module is needed to retrieve the some 
#   of the data from the dataframe object, in 
#   order to provide an easy customization
#   for the user.
#.................................................
import mutationpp as mpp
import utils.initial_conditions_map as ic_map_file  # Module with the initial conditions map functions
from utils.classes import ProgramConstants  # Class with the program constants

def pressure_consistency_check(P, P_dyn, P_stag):
    """This function checks the consistency between the
    static, dynamic and stagnation pressures.

    Args:
        P (float): the pressure
        P_dyn (float): the dynamic pressure
        P_stag (float): the stagnation pressure

    Returns:
        bool: True if the pressures are consistent, False otherwise
    """
    # Constants:
    program_constants = ProgramConstants()
    P_TOL = program_constants.RetrieverHelper.P_TOL  # Tolerance for the pressure difference, P_stag = P + P_dyn
    if (abs(P_stag - P - P_dyn) > P_TOL):
        return False
    else:
        return True

def retrieve_mixture_name(plasma_gas):
    """This function retrieves the mixture name from the plasma gas.

    Args:
        plasma_gas (string): the plasma gas

    Raises:
        ValueError: when an invalid plasma gas is found

    Returns:
        mixture_name (string): the mixture name
    """
    # Match the plasma gas:
    match plasma_gas:
        case "n2":
            mixture_name = "nitrogen2"
        case "N2":
            mixture_name = "nitrogen2"
        case "nitrogen2":
            mixture_name = "nitrogen2"
        case "air_13":
            mixture_name = "air_13"
        case "air_11":
            mixture_name = "air_11"
        case "co2":
            mixture_name = "CO2_8"
        case "CO2":
            mixture_name = "CO2_8"
        case _:  # If the plasma gas is not in the list, I have to check if it is a valid mixture
            try:
                mix_temp = mpp.Mixture(plasma_gas)
                mixture_name = plasma_gas
            except:
                raise ValueError("Error: Invalid plasma gas. Check the input file.")
    return mixture_name
#...................................................
def retrieve_ic(db_name, P, P_dyn, q_target, T_w, max_T_relax):
    """This function retrieves the initial conditions from the database.

    Args:
        db_name (string): the database name
        P (float): the pressure
        P_dyn (float): the dynamic pressure
        q_target (float): the target heat flux
        T_w (float): the wall temperature
        max_T_relax (float): maximum temperature allowed

    Returns:
        ic_db (initial_conditions_db_class): the initial conditions database object
    """
    # Constants:
    program_constants = ProgramConstants()
    CF_CONSTANTS = program_constants.UnitConversion  # Object with the conversion factors
    # Multiplication factor for the initial conditions
    MULTIPLICATION_FACTOR = program_constants.IC_DB.MULTIPLICATION_FACTOR
    # Load the initial conditions database:
    try:
        ic_db = ic_map_file.load_ic_db(db_name)
    except Exception as e:
        raise ValueError("Error: Cannot read the initial conditions database: " + str(e) + ".")
    
    # The inputs are not in the correct units, so I have to convert them:
    # Conversion of the inputs:
    P *= CF_CONSTANTS.P_CF
    P_dyn *= CF_CONSTANTS.P_CF
    q_target *= CF_CONSTANTS.Q_CF
    # Retrieve the initial conditions:
    try:
        initials_object, warnings = ic_map_file.interp_ic_db(ic_db, P, P_dyn, q_target, T_w, max_T_relax, MULTIPLICATION_FACTOR)
    except Exception as e:
        raise ValueError("Error: Interpolation failed: " + str(e) + ".")
    
    return initials_object, warnings
#...................................................
def retrieve_stag_type(stag_type_string):
    """This function retrieves the stagnation type.

    Args:
        stag_type_string (string): the stagnation type

    Raises:
        ValueError: when an invalid stagnation type is found

    Returns:
        stag_type (int): the stagnation type
    """
    # Match the stagnation type:
    match stag_type_string:
        case "flat":  # Flat face probe, Kolesnikov's relation
            stag_type = 0
        case _:
            raise ValueError("Error: Invalid stagnation type. Check the input file.")
    return stag_type
#...................................................

def retrieve_hf_law(hf_law_string):
    """This function retrieves the heat flux law.

    Args:
        hf_law_string (string): the heat flux law

    Raises:
        ValueError: when an invalid heat flux law is found

    Returns:
        hf_law (int): the heat flux law
    """
    # Match the heat flux law:
    match hf_law_string:
            case "exact":  # Exact heat flux law, with boundary layer equations
                hf_law = 0
            case "fay_riddell":  # Fay-Riddell's heat flux law
                hf_law = 1
            case _:
                raise ValueError("Error: Invalid heat flux law. Check the input file.")
    return hf_law

def retrieve_barker_type(barker_type_string):
    """This function retrieves the Barker's correction type.

    Args:
        barker_type_string (string): the Barker's correction type

    Raises:
        ValueError: when an invalid Barker's correction type is found

    Returns:
        barker_type (int): the Barker's correction type
    """
    # Match the Barker's correction type:
    match barker_type_string:
        case "none":
            barker_type = 0
        case "homann":  # Homann's correction for spheres
            barker_type = 1
        case "carleton":  # Carleton's correction
            barker_type = 2
        case _:
            raise ValueError("Error: Invalid Barker's correction type. Check the input file.")
    return barker_type
#...................................................

def retrieve_stag_var(stag_type, R_m, R_j):
    """This function retrieves the stagnation variable.

    Args:
        stag_type (int): the stagnation type
        df (dataframe_class): the dataframe object

    Raises:
        ValueError: when an invalid stagvar is found

    Returns:
        stag_var (float): the stagvar
    """
    # NOTE: R_m and R_j are not in the correct units, but in the current
    # implementation, only the ratio is needed, so I can use them as they are.
    # Match the stag_type:
    match stag_type:
        case 0:  # Flat plate, Kolesnikov's relation
            ratio_L = R_m/R_j
            if (ratio_L <= 1):
                den_sv= 2 - ratio_L - 1.68 * pow ((ratio_L-1), 2) - 1.28 * pow((ratio_L-1), 3)
                stag_var = 1/den_sv
            else:
                stag_var=ratio_L
        case _:
            raise ValueError("Error: Check the code, you should not be here")
    return stag_var

def retrieve_use_prev_ite(use_prev_ite_string):
    """This function retrieves the use_prev_ite.

    Args:
        use_prev_ite_string (string): the use_prev_ite

    Raises:
        ValueError: when an invalid use_prev_ite is found

    Returns:
        use_prev_ite (int): the use_prev_ite
    """
    # Match the use_prev_ite:
    match use_prev_ite_string:
        case "yes":
            use_prev_ite = 1
        case "no":
            use_prev_ite = 0
        case _:
            raise ValueError("Error: Invalid use_prev_ite. Check the input file.")
    return use_prev_ite

def retrieve_log_warning_hf(log_warning_hf_string):
    """This function retrieves the log_warning_hf.

    Args:
        log_warning_hf_string (string): the log_warning_hf

    Raises:
        ValueError: when an invalid log_warning_hf is found

    Returns:
        log_warning_hf (int): the log_warning_hf
    """
    # Match the log_warning_hf:
    match log_warning_hf_string:
        case "yes":
            log_warning_hf = 1
        case "no":
            log_warning_hf = 0
        case _:
            raise ValueError("Error: Invalid log_warning_hf. Check the input file.")
    return log_warning_hf

def retrieve_converted_inputs(inputs_object, initials_object, probes_object):
    """This function retrieves the converted inputs.
    
    Args:
        inputs_object (inputs_class): the inputs object
        initials_object (initials_class): the initials object
        probes_object (probes_class): the probes object
        
    Returns:
        inputs_object (inputs_class): the converted inputs object
        initials_object (initials_class): the converted initials object
        probes_object (probes_class): the converted probes object
    """
    # Constants:
    program_constants = ProgramConstants()
    CF_CONSTANTS = program_constants.UnitConversion  # Object with the conversion factors
    # Conversion of the inputs:
    inputs_object.P *= CF_CONSTANTS.P_CF
    inputs_object.P_dyn *= CF_CONSTANTS.P_CF
    inputs_object.P_stag *= CF_CONSTANTS.P_CF
    inputs_object.q_target *= CF_CONSTANTS.Q_CF
    # Conversion of the initials:
    initials_object.P_t_0 *= CF_CONSTANTS.P_CF
    # Conversion of the probes:
    probes_object.R_p *= CF_CONSTANTS.L_CF
    probes_object.R_m *= CF_CONSTANTS.L_CF
    probes_object.R_j *= CF_CONSTANTS.L_CF
    # Return the objects:
    return inputs_object, initials_object, probes_object
#.................................................
#   Possible improvements:
#   - More specific exceptions
#.................................................
#   KNOW PROBLEMS:
#   -None
#.................................................