#.................................................
#   INITIAL_CONDITIONS_MAP.PY, v2.0.0, December 2024, Domenico Lanza.
#.................................................
#   This module is needed to manage the initial
#   conditions database.
#.................................................
import h5py  # Library to manage the database files
import numpy as np  # Library to manage arrays
import scipy.interpolate as scipy_int  # Library to interpolate data
import utils.classes as classes_file  # Module with the classes

def verify_ic_db(db_name):
    """This function verifies if the database specified
    by the user exists and it is accessible.

    Args:
        db_name (string): the name of the database
        
    Returns:
        bool: True if the database exists and it is accessible, False otherwise
    """
    # Variables:
    try:  # I try to open the file
        with h5py.File(db_name, 'r') as f:
            tmp = f['points'][:]
            tmp = f['values'][:]
        return True
    except:
        return False
    
def load_ic_db(db_name):
    """This function loads the initial conditions database
    from the file specified by the user.

    Args:
        db_name (string): the name of the database

    Returns:
        ic_db (initial_conditions_db_class): the initial conditions database object
    """
    # Create the object
    ic_db = classes_file.InitialConditionsDB()
    # Read the h5py file
    with h5py.File(db_name, 'r') as f:
        points = f['points'][:]
        values = f['values'][:]
    # Assign the data
    ic_db.db_inputs = points
    ic_db.db_outputs = values
    
    return ic_db

def depack_db_to_ic_obj(db_obj):
    """This function depacks the database object(dataframe) to the initial conditions variables
    needed for the ic map.

    Args:
        db_obj (dataframe): the database object
    """
    # Before extracting the data, remove the duplicates
    # based on P, P_dyn, q_target to avoid interpolation problems
    db_obj = db_obj.drop_duplicates(subset=["P", "P_dyn", "q_target"])
    db_obj = db_obj.reset_index(drop=True)
    # Extract the data
    P = db_obj["P"].tolist()
    P_dyn = db_obj["P_dyn"].tolist()
    q_target = db_obj["q_target"].tolist()
    T = db_obj["T"].tolist()
    T_t = db_obj["T_t"].tolist()
    u = db_obj["u"].tolist()
    return P, P_dyn, q_target, T, T_t, u
    
    
def create_ic_db_from_p_and_v(filename, points, values):
    """This function creates the initial conditions database
    file from points and values.

    Args:
        filename (string): the name of the ic map file
        points (numpy array): the points of the database
        values (numpy array): the values of the database
    """
    # Create the ic map file
    f = h5py.File(filename, 'w')
    f.create_dataset('points', data=points)
    f.create_dataset('values', data=values)
    f.close()
    
def create_ic_db(filename, db_obj):
    """This function creates the initial conditions database
    file.

    Args:
        filename (string): the name of the ic map file
        points (numpy array): the points of the database
        values (numpy array): the values of the database
    """
    #Extract db data
    P, P_dyn, q_target, T_0, T_t_0, u_0 = depack_db_to_ic_obj(db_obj)
    # Create the arrays
    P = np.array(P).flatten()
    P_dyn = np.array(P_dyn).flatten()
    q_target = np.array(q_target).flatten()
    T_0 = np.array(T_0).flatten()
    T_t_0 = np.array(T_t_0).flatten()
    u_0 = np.array(u_0).flatten()
    # Create the points and values arrays
    points = np.array([P, P_dyn, q_target]).T
    values = np.array([T_0, T_t_0, u_0]).T
    # Create the ic map file
    create_ic_db_from_p_and_v(filename, points, values)

def concatenate_ic_db(db_obj1, db_obj2):
    """This function concatenates two initial conditions
    database objects.

    Args:
        db_obj1 (initial_conditions_db_class): the first initial conditions database object
        db_obj2 (initial_conditions_db_class): the second initial conditions database object

    Returns:
        ic_db (initial_conditions_db_class): the initial conditions database object
    """
    # Constants:
    program_constants = classes_file.ProgramConstants()  # Program constants
    N = program_constants.IC_DB.N  # Number of decimal digits for the rounding
    # New ic database
    ic_db = classes_file.InitialConditionsDB()
    # Concatenate the data
    points = np.concatenate((db_obj1.db_inputs, db_obj2.db_inputs), axis=0)
    values = np.concatenate((db_obj1.db_outputs, db_obj2.db_outputs), axis=0)
    # Delete the duplicates rows with the same points
    points, indices = np.unique(np.round(points, N), axis=0, return_index=True)
    values = values[indices]
    # Sssign the data
    ic_db.db_inputs = points
    ic_db.db_outputs = values
    # Return the object
    return ic_db

def update_ic_db(ic_obj, db_obj):
    """This function updates the initial conditions database with a new db object.

    Args:
        db_obj (pandas dataframe): the new database object
        ic_obj (initial_conditions_db_class): the initial conditions database object
    """
    # Initialize the new ic database
    new_ic_db = classes_file.InitialConditionsDB()
    # Extract the data
    P, P_dyn, q_target, T, T_t, u = depack_db_to_ic_obj(db_obj)
    # Create the new arrays
    P = np.array(P).flatten()
    P_dyn = np.array(P_dyn).flatten()
    q_target = np.array(q_target).flatten()
    T = np.array(T).flatten()
    T_t = np.array(T_t).flatten()
    u = np.array(u).flatten()
    # Create the new points and values arrays
    new_ic_db.db_inputs = np.array([P, P_dyn, q_target]).T
    new_ic_db.db_outputs = np.array([T, T_t, u]).T
    # Concatenate the data
    new_ic_db = concatenate_ic_db(ic_obj, new_ic_db)
    # Return the new database
    return new_ic_db
    
def interp_ic_db(ic_db, P, P_dyn, q_target, T_w, max_T_relax, multiplication_factor):
    """This function interpolates the initial conditions
    database to retrieve the initial conditions for the
    current case.

    Args:
        ic_db (initial_conditions_db_class): the initial conditions database object
        P (float): the static pressure
        P_dyn (float): the dynamic pressure
        q_target (float): the target heat flux
        T_w (float): the wall temperature
        max_T_relax (float): the maximum temperature allowed
        multiplication_factor (float): the multiplication factor for the initial conditions

    Returns:
        initial_conditions (initials_class): the initial conditions object
        warnings (string): the warnings
    """
    # Constants:
    program_constants = classes_file.ProgramConstants()  # Program constants
    OFFSET_T = program_constants.IC_DB.OFFSET_T  # Offset for the temperature
    OFFSET_T_T = program_constants.IC_DB.OFFSET_T_T  # Offset for the temperature gradient
    MIN_U = program_constants.IC_DB.MIN_U  # Minimum value for the velocity
    # Preliminary operations
    initial_conditions = classes_file.Initials()  # Object with the initial conditions
    int_point = [P, P_dyn, q_target]  # The point to interpolate
    points = ic_db.db_inputs  # The points of the database
    values = ic_db.db_outputs  # The values of the database
    warnings = ""  # The warnings
    # We try to interpolate the data by linear interpolation
    T_0 = scipy_int.griddata(points, values[:,0], int_point, method='linear', fill_value=-1.0)
    T_t_0 = scipy_int.griddata(points, values[:,1], int_point, method='linear', fill_value=-1.0)
    u_0 = scipy_int.griddata(points, values[:,2], int_point, method='linear', fill_value=-1.0)
    # If the linear interpolation fails, extrapolation is used
    if (T_0 == -1.0 or T_t_0 == -1.0 or u_0 == -1.0): 
        warnings += "Linear interpolation failed, nearest interpolation used."
        rfb4 = scipy_int.Rbf(points[:,0], points[:,1], points[:,2], values[:,0], function='thin_plate', smooth=5)
        T_0 = []
        T_0.append(rfb4(int_point[0], int_point[1], int_point[2]))
        
        rfb4 = scipy_int.Rbf(points[:,0], points[:,1], points[:,2], values[:,1], function='thin_plate', smooth=5)
        T_t_0 = []
        T_t_0.append(rfb4(int_point[0], int_point[1], int_point[2]))
        
        rfb4 = scipy_int.Rbf(points[:,0], points[:,1], points[:,2], values[:,2], function='thin_plate', smooth=5)
        u_0 = []
        u_0.append(rfb4(int_point[0], int_point[1], int_point[2]))
        # If extrapolation is out of bounds, nearest interpolation is used
        if(T_0[0] < 0 or T_t_0[0] < 0 or u_0[0] < 0 or T_0[0] > max_T_relax or T_t_0[0] > max_T_relax):
            T_0 = scipy_int.griddata(points, values[:,0], int_point, method='nearest')
            T_t_0 = scipy_int.griddata(points, values[:,1], int_point, method='nearest')
            u_0 = scipy_int.griddata(points, values[:,2], int_point, method='nearest')
            warnings += "Linear interpolation failed, nearest interpolation used.|"
    # I create the object
    T_0 = T_0[0]*multiplication_factor
    if(T_0 < T_w):
        T_0 = T_w + OFFSET_T
    T_t_0 = T_t_0[0]*multiplication_factor
    if(T_t_0 < T_0):
        T_t_0 = T_0 + OFFSET_T_T
    u_0 = u_0[0]*multiplication_factor
    if(u_0 < MIN_U):
        u_0 = MIN_U
    initial_conditions.T_0 = T_0
    initial_conditions.T_t_0 = T_t_0
    initial_conditions.u_0 = u_0
    initial_conditions.P_t_0 = P + P_dyn
    if (warnings == ""):
        warnings = None
    # I return the object
    return initial_conditions, warnings
#.................................................
#   Possible improvements:
#   -create_ic_db_from_p_and_v could use
#    the ic_db object instead of points and values
#.................................................
#   KNOW PROBLEMS: 
#   None
#.................................................