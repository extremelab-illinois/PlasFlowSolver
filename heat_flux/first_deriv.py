#.................................................
#   FIRST_DERIV, v2.0.0, December 2024, Domenico Lanza.
#.................................................
#   This module is needed to compute the first derivative of a function,
#   using the finite difference method.
#.................................................
def first_deriv_array(f, dx, order):
    """This function computes the first derivative of a function using the finite difference method.

    Args:
        f (array): function to derive
        dx (float): step for the finite difference method
        order (int): order of the finite difference method
    Returns:
        df (array): first derivative of f
    """
    # Check which order we can use
    n = len(f)
    if (len(f) <= 2):  # Array too short for a 2nd order derivative
        raise Exception("Error: the array is too short to compute the central finite derivative.")
    elif (len(f) == 3 or len(f) == 4):
        ord = 2  # Maximum order usable
    else:
        ord = 4  # Maximum order usable
    if (order < ord):  # Change the order if the user requires a lower one 
        ord = order 
    # Initialization
    df = [0.0]*n 
    # Compute the derivative
    match (ord): 
        case 2:  # 2nd order finite difference method
            df[0] = (-3*f[0] + 4*f[1] - f[2])/(2*dx)  # Forward difference at the first point
            df[n-1] = (3*f[n-1] - 4*f[n-2] + f[n-3])/(2*dx)  # Backward difference at the last point
            for i in range(1, n-1):  # Central difference for the other points
                df[i] = (f[i+1] - f[i-1])/(2*dx)
        case 4:  # 4th order finite difference method
            df[0] = (-25*f[0] + 48*f[1] - 36*f[2] + 16*f[3] - 3*f[4])/(12*dx)  # Forward difference at the first point
            df[1] = (-3*f[0] - 10*f[1] + 18*f[2] - 6*f[3] + f[4])/(12*dx)  # Forward difference at the second point
            df[n-1] = (25*f[n-1] - 48*f[n-2] + 36*f[n-3] - 16*f[n-4] + 3*f[n-5])/(12*dx)  # Backward difference at the last point
            df[n-2] = (3*f[n-1] + 10*f[n-2] - 18*f[n-3] + 6*f[n-4] - f[n-5])/(12*dx)  # Backward difference at the second last point
            for i in range(2, n-2):  # Central difference for the other points
                df[i] = (f[i-2] - 8*f[i-1] + 8*f[i+1] - f[i+2])/(12*dx)
        case _: 
            raise Exception("Error: order not yet implemented")
    return df 
#.................................................
#   Possible improvements:
#   - Add more finite difference methods, to improve the precision.
#.................................................
#   KNOW PROBLEMS:
#   None.
#.................................................