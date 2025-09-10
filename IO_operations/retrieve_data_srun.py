#.................................................
#   RETRIEVE_DATA_SRUN.PY, v2.0.0, December 2024, Domenico Lanza.
#.................................................
#   This module is needed to retrieve the needed
#   data from the dataframe object for the srun case.
#   In particular, the remaining checks are performed
#.................................................
import utils.classes as classes_file  # Module with the classes
from IO_operations.retrieve_helper import retrieve_mixture_name  # Function to retrieve the mixture name
from IO_operations.retrieve_helper import retrieve_ic  # Function to retrieve the initial conditions
from IO_operations.retrieve_helper import retrieve_stag_type  # Function to retrieve the stagtype
from IO_operations.retrieve_helper import retrieve_hf_law  # Function to retrieve the hf_law
from IO_operations.retrieve_helper import retrieve_barker_type  # Function to retrieve the barker type
from IO_operations.retrieve_helper import retrieve_stag_var  # Function to retrieve the stagvar
from IO_operations.retrieve_helper import retrieve_use_prev_ite  # Function to retrieve the use_prev_iter
from IO_operations.retrieve_helper import retrieve_log_warning_hf  # Function to retrieve the log_warning_hf

def retrieve_data(df):
    """This function retrieves the needed data from 
    the dataframe object for the srun case.

    Args:
        df (dataframe_class): the dataframe object

    Raises:
        ValueError: when an invalid input is found

    Returns:
        inputs_object (inputs_class): the inputs object
        initials_object (initials_class): the initials object
        probes_object (probes_class): the probes object
        settings_object (settings_class): the settings object
    """
    # I create the objects
    inputs_object = classes_file.Inputs()
    initials_object = classes_file.Initials() 
    probes_object = classes_file.Probes()
    settings_object = classes_file.Settings()
    warnings = "" 
    # Inputs:
    inputs_object.comment = df.comment
    inputs_object.P = df.P
    inputs_object.P_dyn = df.P_dyn
    inputs_object.P_stag = df.P_stag
    inputs_object.q_target = df.q_target
    mixture_name = retrieve_mixture_name(df.plasma_gas)
    inputs_object.mixture_name = mixture_name
    # Initial conditions:
    if (df.ic_db_name == ""):
        initials_object.T_0 = df.T_0
        initials_object.T_t_0 = df.T_t_0
        initials_object.u_0 = df.u_0
        initials_object.P_t_0 = df.P_t_0
    else:  # We have to read the initial conditions from the database
        initials_object, warnings_int = retrieve_ic(
            df.ic_db_name, df.P, df.P_dyn, df.q_target,
            df.T_w, df.max_T_relax
            )
        if(warnings_int is not None):
            warnings += warnings_int
    probes_object.T_w = df.T_w
    probes_object.R_p = df.R_p
    probes_object.R_m = df.R_m
    probes_object.R_j = df.R_j
    stag_type = retrieve_stag_type(df.stag_type)
    probes_object.stag_type = stag_type
    probes_object.hf_law = retrieve_hf_law(df.hf_law)
    probes_object.barker_type = retrieve_barker_type(df.barker_type)
    stag_var = retrieve_stag_var(stag_type, probes_object.R_m, probes_object.R_j)
    probes_object.stag_var = stag_var
    # Program settings:
    settings_object.N_p = df.N_p
    settings_object.max_hf_iter = df.max_hf_iter
    settings_object.hf_conv = df.hf_conv
    settings_object.use_prev_ite = retrieve_use_prev_ite(df.use_prev_ite)
    settings_object.eta_max= df.eta_max
    settings_object.log_warning_hf= retrieve_log_warning_hf(df.log_warning_hf)
    settings_object.newton_conv = df.newton_conv
    settings_object.max_newton_iter = df.max_newton_iter
    settings_object.jac_diff = df.jac_diff
    settings_object.min_T_relax = df.min_T_relax
    settings_object.max_T_relax = df.max_T_relax
    # Barker effect and P_t_0 consistency check:
    if (probes_object.barker_type == 0 and initials_object.P_t_0 != inputs_object.P_stag):
        # If the Barker effect is not considered, the P_t_0 must be equal to P_stag
        initials_object.P_t_0 = inputs_object.P_stag
        warnings += "P_t_0 not consistent with the Barker's correction, set to P_stag|"
    # I return the result
    if (warnings != "" and warnings[-1] == "|"):  # I remove the last character
        warnings = warnings[:-1]
    if(warnings == ""):
        warnings = "None"
    return inputs_object, initials_object, probes_object, settings_object, warnings
#.................................................
#   Possible improvements:
#   - More specific exceptions
#   - More checks
#   - Move all the checks in this module or in read_data_srun.py
#.................................................
#   KNOW PROBLEMS:
#   -None
#.................................................