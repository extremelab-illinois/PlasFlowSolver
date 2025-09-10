#.................................................
#   CONTINUITY.PY, v2.0.0, December 2024, Domenico Lanza.
#.................................................
#   This module is needed to solve the continuity equation: dV/deta=-F
#.................................................
def continuity(deta, y): 
    """This function solves the continuity equation: dV/deta=-F
    by using a Simpson numerical integration.

    Args:
        deta (float): step for the numerical integration
        y (array): function to integrate

    Returns:
        V (float): integral of y (array)
    """
    # Initialization
    V = [] 
    # Integration
    V.append(0)  # Boundary condition
    # Simpson rule:
    V.append( (17*y[0]+42*y[1]-16*y[2]+6*y[3]-y[4])*deta/48 )
    for i in range(2,len(y)):
        V.append(V[i-2]+(y[i-2]+4*y[i-1]+y[i])*deta/3) 
    return V
#.................................................
#   Possible improvements:
#   -Implement a more efficient integration method
#.................................................
#   KNOW PROBLEMS:
#   None.
#.................................................