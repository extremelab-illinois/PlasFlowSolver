#.................................................
#   EQ_DIFF_SOLVE.PY, v2.0.0, December 2024, Domenico Lanza.
#.................................................
#   This module is needed to solve
#   the differential equations of the model.
#.................................................
def thomas(a, c, e, d): 
    """This function solves a tridiagonal system of equations
    by using the Thomas algorithm.

    Args:
        a (float array): diagonal of the matrix
        c (float array): upper diagonal of the matrix
        e (float array): lower diagonal of the matrix
        d (float array): vector of the solution
    Raises:
        Exception: wrong input size

    Returns:
        x (float array): vector of the solution
    """
    # Preliminary checks:
    n = len(a) # Number of points
    if (len(c) != n-1 or len(e) != n-1 or len(d) != n):  # Check the input length
        raise Exception('ERROR: wrong input size.')
    # Initialization:
    alpha = [0.0]*n  # Diagonal of U
    beta = [0.0]*(n-1)  # Lower diagonal of L
    y = [0.0]*n  # Intermediate variable
    x = [0.0]*n  # Solution
    alpha[0] = a[0] 
    # Coefficients:
    for i in range(0,n-1):
        beta[i] = e[i]/alpha[i]
        alpha[i+1] = a[i+1]-beta[i]*c[i]
    # Forward substitution:
    y[0] = d[0] 
    for i in range(1,n):
        y[i] = d[i] - beta[i-1]*y[i-1]
    # Backward substitution:
    x[n-1] = y[n-1]/alpha[n-1] 
    for i in range(n-2,-1,-1): 
        x[i] = (y[i] - c[i]*x[i+1])/alpha[i]
    return x 

def solver(a, b, d, f_init, f_final):
    """This function solves the differential equation of the model.

    Args:
        a (float array): the a coefficients of the differential equation
        b (float array): the b coefficients of the differential equation
        d (float array): the d coefficients of the differential equation
        f_init (float): the initial condition for eta=0
        f_final (float): the final condition for eta=eta_max
    Raises:
        Exception: wrong input size.

    Returns:
        res (float array): vector of the solution
    """
    # Preliminary checks:
    n = len(a)  # Number of points
    if (len(b) != n or len(d) != n):  # Check the input length
        raise Exception('ERROR: wrong input size,')
    # We have n points, but:
    #   eta = 0 has res = f_init
    #   eta = eta_max has res = f_final
    #   so we have n-2 points to solve for
    ns = n-2  # Number of points to solve for
    # Initialization:
    aa = [0.0]*ns 
    bb = [0.0]*ns 
    cc = [0.0]*ns 
    dd = [0.0]*ns 
    # P.S. In reality the aa and cc vectors have ns-1 points, because they are 
    # the upper and lower diagonals of the matrix
    # Coefficients:
    for i in range(1, ns+1):
        mnp1p1 = a[i+1] + 1.5*b[i+1]
        mnp10 = -2*( a[i+1] + b[i+1] )
        mnp1m1 = a[i+1] + 0.5*b[i+1]
        mnp1al = -( 6*a[i+1] + 2*b[i+1] )
        mnp1be = -( 10*a[i+1] + 2*b[i+1] )
        mnp1 = a[i] + 0.5*b[i]
        mn0 = -2*a[i]
        mnm1 = a[i]-0.5*b[i]
        mnal = b[i]
        mnbe = 2*a[i]
        mnm1p1 = a[i-1] - 0.5*b[i-1]
        mnm10 = 2*( -a[i-1] + b[i-1])
        mnm1m1 = a[i-1] - 1.5*b[i-1]
        mnm1al = 6*a[i-1] - 2*b[i-1]
        mnm1be = -10*a[i-1] + 2*b[i-1]
        # Determinants to eliminate alfa and beta
        delnp1 = mnal*mnp1be - mnp1al*mnbe
        deln = mnp1al*mnm1be - mnm1al*mnp1be
        delnm1 = mnm1al*mnbe - mnal*mnm1be
        # Coefficients of the system
        aa[i-1] = mnm1p1*delnp1 + mnp1*deln + mnp1p1*delnm1
        bb[i-1] = mnm10*delnp1 + mn0*deln + mnp10*delnm1
        cc[i-1] = mnm1m1*delnp1 + mnm1*deln + mnp1m1*delnm1
        dd[i-1] = d[i-1]*delnp1 + d[i]*deln + d[i+1]*delnm1
    # Making the matrix really tridiagonal
    dd[0] -= cc[0]*f_init
    dd[ns-1] -= aa[ns-1]*f_final
    # We solve the system:
    res = [0.0]*n 
    res[0] = f_init  # First point
    res[n-1] = f_final  # Last point
    cc = cc[1:ns]  # Adjust cc vector for Thomas
    aa = aa[0:ns-1]  # Adjust aa vector for Thomas
    res[1:n-1] = thomas(bb,aa,cc,dd)  # Solve with Thomas
    return res
#.................................................
#   Possible improvements:
#   None
#.................................................
#   KNOW PROBLEMS:
#   None.
#.................................................