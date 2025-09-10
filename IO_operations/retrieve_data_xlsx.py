#.................................................
#   RETRIEVE_DATA_XLSX.PY, v2.0.0, December 2024, Domenico Lanza.
#.................................................
#   This module is needed to retrieve the needed
#   data from the dataframe object from the current loop
#   iteration.
#.................................................
import numpy as np  # Library for the numerical operations
import pandas as pd  # Library to read the xlsx file
import mutationpp as mpp  # Thermodynamic library
import utils.classes as classes_file  # Module with the classes
from utils.initial_conditions_map import verify_ic_db  # Function to verify the database
from IO_operations.retrieve_helper import pressure_consistency_check  # Function to check the pressure consistency
from IO_operations.retrieve_helper import retrieve_mixture_name  # Function to retrieve the mixture name
from IO_operations.retrieve_helper import retrieve_ic  # Function to retrieve the initial conditions
from IO_operations.retrieve_helper import retrieve_stag_type  # Function to retrieve the stagtype
from IO_operations.retrieve_helper import retrieve_hf_law  # Function to retrieve the hf_law
from IO_operations.retrieve_helper import retrieve_barker_type  # Function to retrieve the barker type
from IO_operations.retrieve_helper import retrieve_stag_var  # Function to retrieve the stag_var
from IO_operations.retrieve_helper import retrieve_use_prev_ite  # Function to retrieve the use_prev_iter
from IO_operations.retrieve_helper import retrieve_log_warning_hf  # Function to retrieve the log_warning_hf

def generate_std_file(FILENAME):
    """This function generate the standard values file if it does not exist 
    or it is invalid.
    
    Args:
        FILENAME (str): the filename for the standard values file
    """
    # I generate the file:
    file = open(FILENAME, "w")  # I open the file
    file.write("plasma_gas = air_11\n")  # Plasma gas (string)
    file.write("T_0 [K] = 4000\n")  # Initial temperature (float)
    file.write("T_t_0 [K] = 6000\n")  # Initial total temperature (float)
    file.write("u_0 [m/s] = 500\n")  # Initial velocity (float)
    file.write("P_t_0 [kPa] = 0\n")  # Initial total pressure (float)
    file.write("T_w [K] = 400\n")  # Wall temperature (float)
    file.write("R_p [mm] = 4e0\n")  # Pitot external radius (float)
    file.write("R_m [mm] = 10.1e0\n")  # Flux probe external radius (float)
    file.write("R_j [mm] = 50e0\n")  # Plasma jet radius (float)
    file.write("stag_type = 0\n")  # Stagnation type (integer)
    file.write("hf_law = 0\n")  # Heat flux law (integer)
    file.write("barker_type = 0\n")  # Barker's correction (integer)
    file.write("N_p = 251\n")  # Number of point for the boundary layer eta discretization (integer)
    file.write("max_hf_iter = 100\n")  # Maximum number of iterations for the heat transfer (integer)
    file.write("hf_conv = 1e-4\n")  # Convergence criteria for the heat transfer (float)
    file.write("use_prev_ite = 1\n")  # Use previous iteration for the heat transfer (integer)
    file.write("eta_max = 6\n")  # Maximum value for the boundary layer eta (float)
    file.write("log_warning_hf = 1\n")  # Log warning for the heat flux (integer)
    file.write("newton_conv = 1e-8\n")  # Convergence criteria for the newton solver (float)
    file.write("max_newton_iter = 30\n")  # Maximum number of iterations for the newton solver (integer)
    file.write("jac_diff = 1e-2\n")  # Jacobian finite difference epsilon (float)
    file.write("min_T_relax [K] = 200\n")  # Minimum value for the temperature used for relaxation (float)
    file.write("max_T_relax [K] = 18000\n")  # Maximum value for the temperature used for relaxation (float)
    file.close()
#.................................................

def read_file(FILENAME):
    """This function reads the standard values file and returns the dataframe object.
    Args:
        FILENAME (str): the filename for the standard values

    Returns:
        df (dataframe_class): the dataframe object
    """
    # Initialize the dataframe:
    df = classes_file.DataframeClass()
    # Reading:
    file = open(FILENAME, "r")
    line = file.readline()
    df.plasma_gas = line.split(" = ")[1].strip()  # Plasma gas (string)
    line = file.readline()
    df.T_0 = float(line.split(" = ")[1].strip())  # Initial temperature (float)
    line = file.readline() 
    df.T_t_0 = float(line.split(" = ")[1].strip())  # Initial total temperature (float)
    line = file.readline() 
    df.u_0 = float(line.split(" = ")[1].strip())  # Initial velocity (float)
    line = file.readline() 
    df.P_t_0 = float(line.split(" = ")[1].strip())  # Initial total pressure (float)
    line = file.readline() 
    df.T_w = float(line.split(" = ")[1].strip())  # Wall temperature (float)
    line = file.readline() 
    df.R_p = float(line.split(" = ")[1].strip())  # Pitot external radius (float)
    line = file.readline() 
    df.R_m = float(line.split(" = ")[1].strip())  # Flux probe external radius (float)
    line = file.readline() 
    df.R_j = float(line.split(" = ")[1].strip())  # Plasma jet radius (float)
    line = file.readline() 
    df.stag_type = int(line.split(" = ")[1].strip())  # Stagnation type (integer)
    line = file.readline() 
    df.hf_law = int(line.split(" = ")[1].strip())  # Heat flux law (integer)
    line = file.readline() 
    df.barker_type = int(line.split(" = ")[1].strip())  # Barker's correction (integer)
    line = file.readline() 
    df.N_p = int(line.split(" = ")[1].strip())  # Number of point for the boundary layer eta discretization (integer)
    line = file.readline() 
    df.max_hf_iter = int(line.split(" = ")[1].strip())  # Maximum number of iterations for the heat transfer (integer)
    line = file.readline() 
    df.hf_conv = float(line.split(" = ")[1].strip())  # Convergence criteria for the heat transfer (float)
    line = file.readline() 
    df.use_prev_ite = int(line.split(" = ")[1].strip())  # Use previous iteration for the heat transfer (integer)
    line = file.readline() 
    df.eta_max = float(line.split(" = ")[1].strip())  # Maximum value for the boundary layer eta (float)
    line = file.readline() 
    df.log_warning_hf = int(line.split(" = ")[1].strip())  # Log warning for the heat flux (integer)
    line = file.readline() 
    df.newton_conv = float(line.split(" = ")[1].strip())  # Convergence criteria for the newton solver (float)
    line = file.readline() 
    df.max_newton_iter = int(line.split(" = ")[1].strip())  # Maximum number of iterations for the newton solver (integer)
    line = file.readline() 
    df.jac_diff = float(line.split(" = ")[1].strip())  # Jacobian finite difference epsilon (float)
    line = file.readline() 
    df.min_T_relax = float(line.split(" = ")[1].strip())  # Minimum value for the temperature used for relaxation (float)
    line = file.readline() 
    df.max_T_relax = float(line.split(" = ")[1].strip())  # Maximum value for the temperature used for relaxation (float)
    file.close()  # I close the file
    return df
#.................................................

def read_std_values():
    """This function reads the standard values file and, if needed,
    generate a new std values file.

    Returns:
        df (dataframe_class): the dataframe object
    """
    # CONSTANTS:
    program_constants = classes_file.ProgramConstants()  # Program constants
    FILENAME = program_constants.XLSX.STD_VALUES_FILENAME  # Filename for the standard values
    # Initialize the dataframe:
    df = classes_file.DataframeClass()
    # I check if the std values file exists:
    try:
        file = open(FILENAME, "r") 
        file.close() 
    except:  # If the file does not exist, I generate a new one
        generate_std_file(FILENAME) 
    # I read the file:
    try:
        df = read_file(FILENAME)
    except:  # If the file is not valid, we generate a new one
        generate_std_file(FILENAME)
        df = read_file(FILENAME)
    return df
    
    
def is_valid_data(x):
    """This function verifies if
    the data passed is a valid numeric
    data.

    Args:
        x (unknown): the data to check

    Returns:
        bool: true if the data is valid, false otherwise
    """
    if (pd.isna(x) or ( (isinstance(x, np.int64) == False) and (isinstance(x, np.float64) == False) and (isinstance(x, float) == False) and (isinstance(x, int) == False )) or x <= 0):
        return False
    else:
        return True

def retrieve_data(df,n_case):
    """This function retrieves the needed data from the dataframe object 
    for the current loop iteration in the .xlsx mode

    Args:
        df (dataframe_class): the dataframe object
        n_case (int): the case number

    Returns:
        inputs_object(inputs_class): the inputs object containing the inputs
        initials_object (initials_class): the initials object containing the initials
        probes_object (probes_class): the probes object containing the probes
        settings_object (settings_class): the settings object containing the settings
    """
    # Initialize the objects:
    inputs_object = classes_file.Inputs() 
    initials_object = classes_file.Initials() 
    probes_object = classes_file.Probes()
    settings_object = classes_file.Settings() 
    warnings = ""
    # I read the std values:
    std_values = read_std_values()
    # comment
    comment = df.comment[n_case]  # comment, string
    if (pd.isna(comment) or comment == None or comment == ""):
        inputs_object.comment = "Case "+str(n_case)  # We set the default value
    else:
        inputs_object.comment = comment
    # Pressure:
    P = df.P[n_case]  # Pressure (float)
    if (is_valid_data(P) == False):
        raise ValueError("Error: The pressure value is not valid.")
    else:
        inputs_object.P = df.P[n_case]  # To be converted to the right unit
    # Dynamic pressure:
    P_dyn = df.P_dyn[n_case]  # Dynamic pressure (float)
    # Stagnation pressure:
    P_stag = df.P_stag[n_case]  # Stagnation pressure (float)
    if (is_valid_data(P_stag) == False):
        if (is_valid_data(P_dyn) == False):
            raise ValueError("Error: The stagnation pressure or dynamic value is not valid.")
        else:
            P_used = "dyn"
            inputs_object.P_dyn = df.P_dyn[n_case]  
    elif (is_valid_data(P_dyn) == False):
        P_used = "stag"
        inputs_object.P_stag = df.P_stag[n_case]
    else:
        P_used = "Both"
        inputs_object.P_dyn = df.P_dyn[n_case]  
        inputs_object.P_stag = df.P_stag[n_case]
    # Heat flux:
    q_target = df.q_target[n_case]  # Heat flux (float)
    if(is_valid_data(q_target) == False):
        raise ValueError("Error: The heat flux value is not valid.")
    else:
        inputs_object.q_target = df.q_target[n_case]  # To be converted to the right unit 
    # Plasma gas:
    plasma_gas = df.plasma_gas[n_case]  # Plasma gas (string)
    if (pd.isna(plasma_gas) or plasma_gas == None or plasma_gas == ""):
        inputs_object.mixture_name = std_values.plasma_gas
        warnings += "Plasma gas invalid, set to STD|"
    else:
        try:
            inputs_object.mixture_name = retrieve_mixture_name(plasma_gas)  # Plasma gas (string)
        except:
            inputs_object.mixture_name = std_values.plasma_gas
            warnings += "Plasma gas invalid, set to STD|"
    # Check if the mixture exists:
    try:
        mix_temp = mpp.Mixture(inputs_object.mixture_name)
    except Exception as e:
        raise ValueError("Error: Invalid plasma gas in std_value. Please check the mixture name.")
    match P_used:
        case "dyn":
            inputs_object.P_stag = inputs_object.P_dyn + inputs_object.P  # I compute the stagnation pressure
        case "stag":
            inputs_object.P_dyn = inputs_object.P_stag - inputs_object.P  # I compute the dynamic pressure
        case "Both":
            if (pressure_consistency_check(inputs_object.P,inputs_object.P_dyn,inputs_object.P_stag) == False):
                raise ValueError("Error: The stagnation pressure and dynamic pressure values are not consistent.")
    # The 2 following quantities are evaluated now (even if this is not the correct order)
    # because they are needed for the initial conditions:
    # Needed:
    T_w = df.T_w[n_case]  # Wall temperature (float)
    if (is_valid_data(T_w) == False):
        probes_object.T_w = std_values.T_w
        warnings += "T_w invalid, set to STD|"
    else:
        probes_object.T_w=df.T_w[n_case]
    # Needed:
    max_T_relax = df.max_T_relax[n_case]  # Maximum value for the temperature used for relaxation
    if (is_valid_data(max_T_relax) == False):
        settings_object.max_T_relax = std_values.max_T_relax
        warnings += "max_T_relax invalid, set to STD|"
    else:
        settings_object.max_T_relax = df.max_T_relax[n_case] 
    # Initials:
    ic_db_name = df.ic_db_name[n_case]  # Initial conditions database name (string)
    if(verify_ic_db(ic_db_name) == True):
        print("Initial conditions database " + ic_db_name + " verified.")
        initials_object, warnings_int = retrieve_ic(
            ic_db_name, inputs_object.P, inputs_object.P_dyn, inputs_object.q_target,
            probes_object.T_w, settings_object.max_T_relax
            )
        if(warnings_int is not None):
            warnings += warnings_int
    else:
        if(ic_db_name != "" and (pd.isna(ic_db_name) == False)):
            print("Initial conditions database " + ic_db_name + " invalid. Initial conditions will be read from the file.")
            warnings += "Invalid initial conditions database|"
        T_0 = df.T_0[n_case]  # Initial temperature (float)
        if (is_valid_data(T_0) == False):
            initials_object.T_0 = std_values.T_0
            warnings += "T_0 invalid, set to STD|"
        else:
            initials_object.T_0 = df.T_0[n_case] 
        T_t_0 = df.T_t_0[n_case]  # Initial total temperature (float)
        if (is_valid_data(T_t_0) == False):
            initials_object.T_t_0 = std_values.T_t_0
            warnings += "T_t_0 invalid, set to STD|"
        else:
            initials_object.T_t_0 = df.T_t_0[n_case] 
        u_0 = df.u_0[n_case]  # Initial velocity (float)
        if (is_valid_data(u_0) == False):
            initials_object.u_0 = std_values.u_0
            warnings += "u_0 invalid, set to STD|"
        else:
            initials_object.u_0 = df.u_0[n_case] 
        P_t_0 = df.P_t_0[n_case]  # Initial total pressure (float)
        if (is_valid_data(P_t_0) == False):
            if (P_t_0 == 0):
                initials_object.P_t_0 = inputs_object.P_stag
            else:
                initials_object.P_t_0 = std_values.P_t_0
                if (initials_object.P_t_0 == 0):
                    initials_object.P_t_0 = inputs_object.P_stag
                warnings += "P_t_0 invalid, set to STD|"
        else:
            initials_object.P_t_0 = df.P_t_0[n_case]
    # Probe properties:
    R_p = df.R_p[n_case]  # Pitot external radius (float)
    if (is_valid_data(R_p) == False):
        probes_object.R_p = std_values.R_p
        warnings += "R_p invalid, set to STD|"
    else:
        probes_object.R_p = df.R_p[n_case] 
    R_m = df.R_m[n_case]  # Flux probe external radius (float)
    if (is_valid_data(R_m) == False):
        probes_object.R_m = std_values.R_m
        warnings += "R_m invalid, set to STD|"
    else:
        probes_object.R_m = df.R_m[n_case]
    R_j = df.R_j[n_case]  # Plasma jet radius (float)
    if (is_valid_data(R_j) == False):
        probes_object.R_j = std_values.R_j
        warnings += "R_j invalid, set to STD|"
    else:
        probes_object.R_j = df.R_j[n_case]
    stag_type = df.stag_type[n_case]  # Stagnation type (string->integer)
    if (pd.isna(stag_type)):
        probes_object.stag_type = std_values.stag_type
        warnings += "stag_type invalid, set to STD|"
    else:
        try:
            stag_type = stag_type.lower()
            stag_type = retrieve_stag_type(stag_type)  # (integer)
            probes_object.stag_type = stag_type
        except:
            probes_object.stag_type = std_values.stag_type
            warnings += "stag_type invalid or not yet implemented, set to STD|"
    hf_law = df.hf_law[n_case]  # Heat flux law (string->integer)
    if (pd.isna(hf_law)):
        probes_object.hf_law = std_values.hf_law
        warnings += "hf_law invalid, set to STD|"
    else:
        try:
            hf_law = hf_law.lower()
            hf_law = retrieve_hf_law(hf_law)  # (integer)
            probes_object.hf_law = hf_law
        except:
            probes_object.hf_law = std_values.hf_law
            warnings += "hf_law invalid or not yet implemented, set to STD|"
    barker_type = df.barker_type[n_case] #Barker correct, string->integer
    if (pd.isna(barker_type)):
        probes_object.barker_type = std_values.barker_type
        warnings += "barker_type invalid, set to STD|"
    else:
        try:
            barker_type = barker_type.lower()
            barker_type = retrieve_barker_type(barker_type)  # (integer)
            probes_object.barker_type = barker_type
        except:
            probes_object.barker_type = std_values.barker_type
            warnings += "barker_type invalid or not yet implemented, set to STD|"
    stag_var = retrieve_stag_var(probes_object.stag_type, probes_object.R_m, probes_object.R_j)  # Stagnation variable (float)
    # NOTE: R_m and R_j are not in the SI units, but in the current implementation
    # only their ratio is used for stag_var, so this is not a problem.
    probes_object.stag_var = stag_var
    # Barker's effect and P_t_0 consistency check:
    if (probes_object.barker_type == 0 and initials_object.P_t_0 != inputs_object.P_stag):
        initials_object.P_t_0 = inputs_object.P_stag
        warnings += "P_t_0 not consistent with the Barker's correction, set to P_stag|"
    # Settings:
    N_p = df.N_p[n_case]  # Number of point for the boundary layer eta discretization (integer)
    if (is_valid_data(N_p) == False):
        settings_object.N_p = std_values.N_p
        warnings += "N_p invalid, set to STD|"
    else:
        if(int(N_p)==N_p):
            settings_object.N_p = int(df.N_p[n_case])  
        else:
            settings_object.N_p = std_values.N_p
            warnings += "N_p invalid, set to STD|"
    max_hf_iter = df.max_hf_iter[n_case]  # Maximum number of iterations for the heat transfer (integer)
    if (is_valid_data(max_hf_iter) == False):
        settings_object.max_hf_iter = std_values.max_hf_iter
        warnings += "max_hf_iter invalid, set to STD|"
    else:
        if (int(max_hf_iter) == max_hf_iter):
            settings_object.max_hf_iter = df.max_hf_iter[n_case]  # Maximum number of iterations for the heat transfer
        else:
            settings_object.max_hf_iter = std_values.max_hf_iter
            warnings += "max_hf_iter invalid, set to STD|"
    hf_conv = df.hf_conv[n_case]  # Convergence criteria for the heat transfer (float)
    if (is_valid_data(hf_conv) == False):
        settings_object.hf_conv = std_values.hf_conv
        warnings += "hf_conv invalid, set to STD|"
    else:
        settings_object.hf_conv = df.hf_conv[n_case] 
    use_prev_ite = df.use_prev_ite[n_case]  # Use previous iteration for the heat transfer (string->integer)
    if (pd.isna(use_prev_ite)):
        settings_object.use_prev_ite = std_values.use_prev_ite
        warnings += "use_prev_ite invalid, set to STD|"
    else:
        try:
            use_prev_ite = use_prev_ite.lower()
            use_prev_ite = retrieve_use_prev_ite(use_prev_ite)  # (integer)
            settings_object.use_prev_ite = use_prev_ite
        except:
            settings_object.use_prev_ite = std_values.use_prev_ite
            warnings += "use_prev_ite invalid, set to STD|"
    eta_max = df.eta_max[n_case]  # Upper integration boundary for the normal coordinate of the boundary layer (float)
    if (is_valid_data(eta_max) == False):
        settings_object.eta_max = std_values.eta_max
        warnings += "eta_max invalid, set to STD|"
    else:
        settings_object.eta_max = df.eta_max[n_case] 
    log_warning_hf = df.log_warning_hf[n_case]  # Log warning for the heat flux (string)
    if (pd.isna(log_warning_hf)):
        settings_object.log_warning_hf = std_values.log_warning_hf
        warnings += "log_warning_hf invalid, set to STD|"
    else:
        try:
            log_warning_hf = log_warning_hf.lower() 
            log_warning_hf = retrieve_log_warning_hf(log_warning_hf)  # (integer)
            settings_object.log_warning_hf = log_warning_hf
        except:
            settings_object.log_warning_hf = std_values.log_warning_hf
            warnings += "log_warning_hf invalid, set to STD|"
    newton_conv = df.newton_conv[n_case]  # Convergence criteria for the newton solver (float)
    if (is_valid_data(newton_conv) == False):
        settings_object.newton_conv = std_values.newton_conv
        warnings += "newton_conv invalid, set to STD|"
    else:
        settings_object.newton_conv = df.newton_conv[n_case] 
    max_newton_iter = df.max_newton_iter[n_case]  # Maximum number of iterations for the newton solver (integer)
    if (is_valid_data(max_newton_iter) == False):
        settings_object.max_newton_iter = std_values.max_newton_iter
        warnings += "max_newton_iter invalid, set to STD|"
    else:
        if(int(max_newton_iter) == max_newton_iter):
            settings_object.max_newton_iter = df.max_newton_iter[n_case] 
        else:
            settings_object.max_newton_iter = std_values.max_newton_iter
            warnings += "max_newton_iter invalid, set to STD|"
    jac_diff = df.jac_diff[n_case]  # Jacobian finite difference epsilon (float)
    if (is_valid_data(jac_diff) == False):
        settings_object.jac_diff = std_values.jac_diff
        warnings += "jac_diff invalid, set to STD|"
    else:
        settings_object.jac_diff = df.jac_diff[n_case] 
    min_T_relax = df.min_T_relax[n_case]  # Minimum value for the temperature used for relaxation
    if (is_valid_data(min_T_relax) == False):
        settings_object.min_T_relax = std_values.min_T_relax
        warnings += "min_T_relax invalid, set to STD|"
    else:
        settings_object.min_T_relax = df.min_T_relax[n_case] 
    # Return the objects:
    if (warnings != "" and warnings[-1] == "|"):  # I remove the last character
        warnings = warnings[:-1]
    if(warnings == ""):
        warnings = "None"
    return inputs_object, initials_object, probes_object, settings_object, warnings
#.................................................
#   Possible improvements:
#   - Be consistent for the std_values and use names
#   for the flags instead of numbers
#   - Use getter and setter for the inputs, initials, probes and settings objects
#   - Better exception throwing
#   - Use a more efficient (and shorter) way to check the data
#.................................................
#   Known problems:
#   None.
#.................................................
