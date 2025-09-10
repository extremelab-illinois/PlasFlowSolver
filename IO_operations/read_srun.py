#.................................................
#   READ_SRUN.PY, v2.0.0, December 2024, Domenico Lanza.
#.................................................
#   This module is needed to read the
#   .srun (Single Run) file and create the the
#   dataframe object. In particular, here all the
#   inputs are read, but the settings are not retrieved.
#   That is done in retrieve_data_srun.py.
#.................................................
from utils.classes import DataframeClass  # Class that contains the dataframe object
from utils.script_run import retrieve_filename  # Module that contains the bash run functions
from IO_operations.retrieve_helper import pressure_consistency_check  # Function to check the pressure consistency
from utils.initial_conditions_map import verify_ic_db  # Function to verify the initial conditions database

def prompt_input_file():
    """This function prompts the user for the
    input filename.

    Returns:
        input_filename (string): the name of the input file
    """
    # Variables:
    print("Input the name of the .srun file to read.")
    input_file_name = input("Filename: ") 
    # I check if the extension is .srun, otherwise I add it
    if (input_file_name.endswith(".srun") == False):
        input_file_name = input_file_name + ".srun"
    return input_file_name

def read_srun(script_run):
    """This function create a dataframe_class
    object from a srun file.

    Inputs:
        script_run (bool): True if the program is in bash mode, False otherwise
    
    Returns:
        df_object (dataframe_class) : the dataframe object from the .srun file
        output_filename (string): the name of the output file
    """
    # Reading process:
    file_found = False
    # Check if the program is in bash mode
    if (script_run == True):
        try:  # I try to read the file
            input_filename = retrieve_filename()  # Retrieve the filename from the script.pfs file
            file = open(input_filename, "r")
            file_found = True
            file.close()
        except:
            print("Error: the file in bash.pfs does not exist or is not an .srun file.")
            print("The program will continue in manual mode.")
    # If the bash mode file was not found or the program is not in bash mode, I prompt the user for the input file
    while (file_found == False):
        input_filename = prompt_input_file()
        try:  # I check if the file exists
            file = open(input_filename, "r")
            file_found = True
            file.close()
        except:
            print("Error: the file does not exist or is not an .srun file.")
    # I set the output filename
    output_filename = input_filename[:-5] + "_out.srun"
    # Now I read the input file
    file = open(input_filename, "r")
    # INPUTS:
    file.readline()  # I skip the first line, that is the section title (INPUTS)
    # Comment:
    line = file.readline()
    comment = line.split("=")[1].strip()  # The comment is the string after the "=" sign
    # Static pressure:
    line = file.readline()
    P = float(line.split("=")[1].strip())  # The static pressure is the float after the "=" sign
    # Dynamic pressure:
    P_dyn_used = False
    line = file.readline()
    try:  # I try to read the dynamic pressure
        P_dyn = float(line.split("=")[1].strip())  # The dynamic pressure is the float after the "=" sign
        P_dyn_used = True  # If the user has set the dynamic pressure
    except:
        pass  # Nothing has to be done
    # Stagnation pressure:
    P_stag_used = False
    line = file.readline()
    try:  # I try to read the stagnation pressure
        P_stag = float(line.split("=")[1].strip())  # The stagnation pressure is the float after the "=" sign
        P_stag_used = True  # If the user has set the stagnation pressure
    except:
        pass  # Nothing has to be done
    # Stagnation heat flux:
    line = file.readline()
    q_target = float(line.split("=")[1].strip())  # The heat flux is the float after the "=" sign
    # Plasma gas:
    line = file.readline()
    plasma_gas = line.split("=")[1].strip()  # The plasma gas is the string after the "=" sign
    if (P_dyn_used == True and P_stag_used == False):
        P_stag = P + P_dyn
    elif (P_dyn_used == False and P_stag_used == True):
        P_dyn = P_stag - P
    elif (P_dyn_used == True and P_stag_used == True):
        if ( pressure_consistency_check(P, P_dyn, P_stag) == False ):  # I check if the pressures are consistent 
            raise Exception("ERROR: The pressures are inconsistent.")
    else: 
        raise Exception("ERROR: Either the dynamic pressure or the stagnation pressure must be set.")
    if ( P<=0 or P_dyn <=0 or P_stag <=0 or q_target<=0 ):
        raise Exception("ERROR: At least one of the inputs is zero or less.")
    # Initial conditions:
    line = file.readline()  # I skip the line, that is the section title (INITIAL CONDITIONS)
    # Initial conditions database name:
    line = file.readline()
    ic_db_name = line.split("=")[1].strip()  # The initial conditions database name is the string after the "=" sign
    if(verify_ic_db(ic_db_name) == True):  # If the initial conditions database is specified and valid, it is used, and 
        # the initial conditions are not read from the file
        print("Initial conditions database " + ic_db_name + " verified.")
        # I skip the lines that contain the initial conditions
        line = file.readline()
        line = file.readline()
        line = file.readline()
        line = file.readline()
        T_0 = None
        T_t_0 = None
        u_0 = None
        P_t_0 = None
    else:
        if(ic_db_name != ""):  # If the initial conditions database is specified but invalid, a warning is printed
            print("Initial database " + ic_db_name + " invalid. Initial conditions will be read from the file.")
        ic_db_name = ""
        # Initial static temperature:
        line = file.readline()
        T_0 = float(line.split("=")[1].strip())  # The initial static temperature is the float after the "=" sign
        # Initial total temperature: 
        line = file.readline()
        T_t_0 = float(line.split("=")[1].strip())  # The initial total temperature is the float after the "=" sign
        # Initial velocity:
        line = file.readline()
        u_0 = float(line.split("=")[1].strip())  # The initial velocity is the float after the "=" sign
        # Initial total pressure:
        line = file.readline()
        P_t_0 = float(line.split("=")[1].strip())  # The initial total pressure is the float after the "=" sign
        if (P_t_0 == 0):
            P_t_0 = P_stag  # If the initial total pressure is zero, I set it to the stagnation pressure
        if ( T_0 <= 0 or T_t_0 <= 0 or u_0 <=0 or P_t_0<=0):
            raise Exception("ERROR: At least one of the initial conditions is zero or less.")
    # Probe properties:
    line = file.readline()  # I skip the line, that is the section title (PROBE PROPERTIES)
    # Wall temperature:
    line = file.readline()
    T_w = float(line.split("=")[1].strip())  # The wall temperature is the float after the "=" sign
    # Pitot external radius:
    line = file.readline()
    R_p = float(line.split("=")[1].strip())  # The pitot external radius is the float after the "=" sign
    # Heat flux probe external radius:
    line = file.readline()
    R_m = float(line.split("=")[1].strip())  # The heat flux probe external radius is the float after the "=" sign
    # Plasma jet radius:
    line = file.readline()
    R_j = float(line.split("=")[1].strip())  # The plasma jet radius is the float after the "=" sign
    if ( T_w<=0 or R_p <= 0 or R_m <= 0 or R_j <= 0):
        raise Exception("ERROR: One of the probe properties is zero or less (T_w, R_p, R_m, R_j).")
    # Stagnation type:
    line = file.readline()
    stag_type = line.split("=")[1].strip().lower()  # The stagnation type is the string after the "=" sign
    # Heat flux law:
    line = file.readline()
    hf_law = line.split("=")[1].strip().lower()  # The heat flux law is the string after the "=" sign
    # Barker correction:
    line = file.readline()
    barker_type = line.split("=")[1].strip().lower()  # The Barker correction is the string after the "=" sign
    # Program settings:
    line = file.readline()  # I skip the line, that is the section title (PROGRAM SETTINGS)
    # Number of point for the boundary layer eta discretization:
    line = file.readline()
    N_p = int(line.split("=")[1].strip())  # It is the integer after the "=" sign
    # Maximum number of iterations for the heat flux:
    line = file.readline()
    max_hf_iter = int(line.split("=")[1].strip())  # It is the integer after the "=" sign
    # Convergence criteria for the heat flux:
    line = file.readline()
    hf_conv = float(line.split("=")[1].strip())  # It is the float after the "=" sign
    # Boolean to decide if the program should use previous iterations for the heat transfer:
    line = file.readline()
    use_prev_ite = line.split("=")[1].strip().lower()  # It is the string after the "=" sign
    # Maximum value for the boundary layer eta discretization:
    line = file.readline()
    eta_max = float(line.split("=")[1].strip())  # It is the float after the "=" sign
    # Boolean to decide if a warning should be logged when the heat flux does not converge:
    line = file.readline()
    log_warning_hf = line.split("=")[1].strip().lower()  # It is the string after the "=" sign
    # Convergence criteria for the newton solver:
    line = file.readline()
    newton_conv = float(line.split("=")[1].strip())  # It is the float after the "=" sign
    # Maximum number of iterations for the Newton solver:
    line = file.readline()
    max_newton_iter = int(line.split("=")[1].strip())  # It is the integer after the "=" sign
    # Jacobian finite difference epsilon:
    line = file.readline()
    jac_diff = float(line.split("=")[1].strip())  # It is the float after the "=" sign
    # Minimum value for the temperature used for relaxation:
    line = file.readline()
    min_T_relax = float(line.split("=")[1].strip())  # It is the float after the "=" sign
    # Maximum value for the temperature used for relaxation:
    line = file.readline()
    max_T_relax = float(line.split("=")[1].strip())  # It is the float after the "=" sign
    file.close()    
    # I now store the variables in the dataframe object
    df_object = DataframeClass() # I create the dataframe object to be returned
    df_object.n = 1  # Number of cases (integer)
    df_object.comment = comment  # Comment (string)
    df_object.P = P  # Static pressure (float)
    df_object.P_dyn = P_dyn  # Dynamic pressure (float)
    df_object.P_stag = P_stag  # Stagnation pressure (float)
    df_object.q_target = q_target  # Target heat flux (float)
    df_object.plasma_gas = plasma_gas  # Plasma gas (string)
    df_object.ic_db_name = ic_db_name  # Initial conditions database name (string)
    df_object.T_0 = T_0  # Initial static temperature (float)
    df_object.T_t_0 = T_t_0  # Initial total temperature (float)
    df_object.u_0 = u_0  # Initial flow velocity (float)
    df_object.P_t_0 = P_t_0  # Initial total pressure (float)
    df_object.T_w = T_w  # Probe wall temperature (float)
    df_object.R_p = R_p  # Pitot external radius (float)
    df_object.R_m = R_m  # Heat flux probe external radius (float)
    df_object.R_j = R_j  # Plasma jet radius (float)
    df_object.stag_type = stag_type # Stagnation type (string)
    df_object.hf_law = hf_law  # Heat flux law (string)
    df_object.barker_type = barker_type  # Barker's correction type (string)
    df_object.N_p = N_p  # Number of point for the boundary layer eta discretization (integer)
    df_object.max_hf_iter = max_hf_iter  # Maximum number of iterations for the heat flux (integer)
    df_object.hf_conv = hf_conv  # Convergence criteria for the heat flux (float)
    df_object.use_prev_ite = use_prev_ite  # Use previous iteration for the heat transfer (string)
    df_object.eta_max = eta_max  # Maximum value for the boundary layer eta (float)
    df_object.log_warning_hf = log_warning_hf  # Log warning for when the heat flux does not converge (string)
    df_object.newton_conv = newton_conv  # Convergence criteria for the newton solver (float)
    df_object.max_newton_iter = max_newton_iter  # Maximum number of iterations for the newton solver (integer)
    df_object.jac_diff = jac_diff  # Jacobian finite difference epsilon (float)
    df_object.min_T_relax = min_T_relax  # Minimum value for the temperature used for relaxation (float)
    df_object.max_T_relax = max_T_relax  # Maximum value for the temperature used for relaxation (float)
    return df_object, output_filename
#.................................................
#   Possible improvements:
#   - Add getter and setter for the dataframe object
#   - Throw specific exceptions for each read error
#   - Move the pressure check in retrieve, to
#   be consistent with the other file reading functions
#   -More error checking
#.................................................
#   Known problems:
#   - None
#.................................................