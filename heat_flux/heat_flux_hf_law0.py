#.................................................
#   HEAT_FLUX_HF_LAW0.PY, v2.0.0, December 2024, Domenico Lanza.
#.................................................
#   This module is needed to compute the 
#   heat flux for the exact heat flux law, hf_law=0,
#   solving the boundary layer equations.
#.................................................
import math  # Library for mathematical operations
import numpy as np  # Library for numerical operations
import heat_flux.heat_flux_hf_law0_properties as heat_flux_hf_law0_properties_file  # Module to compute the properties of the flow
import heat_flux.continuity as continuity_file  # Module with the function to solve the continuity equation
import heat_flux.first_deriv as first_deriv_file  # Module with the function to compute the first derivative of functions
import heat_flux.eq_diff_solve as eq_diff_solve_file  # Module with the function to solve differential equations
from utils.classes import ProgramConstants

def f(eta):
    """Function to compute the f starting profile for the boundary layer.
    Hartree's profile is used.
    Args:
        eta (float): the eta value

    Returns:
        float: the f value
    """
    return 0.007005 * eta**3 - 0.114439 * eta**2 + 0.598555 * eta


def stretched_eta(eta_new, eta_max):
    """Function to compute the stretched eta value.
    
    Args:
        eta_new (float): the new eta value
        eta_max (float): the maximum eta value
        
    Returns:
        float: the stretched eta value
    """
    return (eta_new / eta_max) * 6  # Scale the eta value


def reset_vars(deta, T_e, T_w, N_p, eta_max):
    """Function to reset the x, y, z arrays
    for the heat flux computation.

    Args:
        deta (float): the step of eta
        T_e (float): the edge temperature
        T_w (float): the wall temperature
        N_p (integer): the number of points for the boundary layer eta discretization

    Returns:
        x (list, float): the eta array
        y (list, float): the F array
        z (list, float): the g array
    """
    # Initialization:
    x = []  # Array with the eta discretization
    y = []  # Array with the F values
    z = []  # Array with the g values
    # Computing the arrays:
    for i in range(N_p):
        eta = i * deta  # Eta i-th value
        x.append(eta)
        stretched_eta_i = stretched_eta(eta, eta_max)  # Stretched eta
        f_i = f(stretched_eta_i)  # f_i-th value
        y.append(f_i)
        g_i = min(1, f_i+T_w/T_e*(eta_max-eta)/eta_max)  # g_i-th value
        z.append(g_i)
    return x, y, z

def properties_across_BL(T_e, P_e, mu_e, rho_e, z, N_p, mixture_object, max_T_relax):
    """Function to compute the properties across the boundary layer.

    Args:
        T_e (float): the edge temperature
        P_e (float): the edge pressure
        mu_e (float): the edge viscosity
        rho_e (float): the edge density
        z (list, float): the eta array
        N_p (integer): the number of points for the boundary layer eta discretization
        mixture_object (mpp.Mixture): the mixture object
        max_T_relax (float): the maximum value for the temperature used for relaxation

    Returns:
        l_0 (list, float): the l_0 array
        rr (list, float): the rr array
        chi (list, float): the kpr array
        C_p (list, float): the C_p array
        redo (boolean): the variable to understand if we need to redo the computation
    """
    # Initialization:
    l_0 = []  # Vector to store the l_0 values, l_0 = rho*mu/(rho_e*mu_e)
    rr = []  # Vector to store the rr values, rr = rho_e/rho
    chi = []  # Vector to store the kpr values, kpr=lambda*rho/(rho_e*mu_e)
    C_p = []  # Vector to store the C_p values
    redo = False  # Flag to understand if we need to redo the computation
    # Computation:
    for i in range(0, N_p):
        T = T_e*z[i]  # Current temperature
        if (T <= 4 or np.isnan(T) or T > max_T_relax):  # This should never happen, redo the computation
            redo = True
            return l_0, rr, chi, C_p, redo
        # Compute the properties:
        rho, C_p_i, mu, lambda_eq = heat_flux_hf_law0_properties_file.heat_flux_hf_law0_flow(P_e, T, mixture_object)
        l_0_i = rho*mu/(rho_e*mu_e)
        l_0.append(l_0_i)
        rr_i = rho_e/rho 
        rr.append(rr_i)
        chi_i = lambda_eq*rho/(rho_e*mu_e) 
        chi.append(chi_i) 
        C_p.append(C_p_i) 
    return l_0, rr, chi, C_p, redo

def heat_flux(probes, settings, P_e, T_e, u, mixture_object):
    """Function to compute the stagnation heat flux for 
    the hflaw=0 case.

    Args:
        probes (probes_class) : the probes object containing the probe properties
        settings (settings_class) : the settings object containing the program settings
        P_e (float) : the edge pressure, which is the total pressure in this case
        T_e (float) : the total temperature, which is the total temperature in this case
        u (float) : the freestream velocity
        mixture_object (mpp.Mixture) : the mixture object
    
    Raises:
        ValueError: if the temperature is negative, nan or greater than the max temperature

    Returns:
        q (float): the stagnation heat flux
    """
    # Constants:
    program_constants = ProgramConstants()
    ORDER = program_constants.HeatFlux.ORDER  # Order of the central finite difference
    # Filename for the use_prev_ite variable
    USE_PREV_ITE_FILENAME = program_constants.TemporaryFiles.USE_PREV_ITE_FILENAME  
    X_VAR_FILENAME = program_constants.TemporaryFiles.X_VAR_FILENAME  # Filename for the x variable
    Y_VAR_FILENAME = program_constants.TemporaryFiles.Y_VAR_FILENAME  # Filename for the y variable
    Z_VAR_FILENAME = program_constants.TemporaryFiles.Z_VAR_FILENAME  # Filename for the z variable
    # Extract variables:
    beta = probes.stag_var * u / probes.R_m  # Velocity gradient
    eta_max = settings.eta_max  # Maximum value for the boundary layer eta
    hf_conv = settings.hf_conv  # Convergence criteria for the heat flux
    log_warning_hf = settings.log_warning_hf  # Log warning for when the heat flux does not converge
    max_iter = settings.max_hf_iter  # Maximum number of iterations for the heat flux
    max_T_relax = settings.max_T_relax  # Maximum value for the temperature used for relaxation
    N_p = settings.N_p  # Number of points for the boundary layer eta discretization
    T_w = probes.T_w  # Probe wall temperature
    use_prev_ite = settings.use_prev_ite  # Variable to understand if we need to use the previous iteration
    #.................................................
    #START OF THE CODE:
    bad_convergence = False  # Flag for heat flux convergence
    deta = eta_max/(N_p-1)  # Discretization step
    # Check if the heat flux has been computed previously
    if (use_prev_ite == True): 
        hf_first_comp = np.loadtxt(USE_PREV_ITE_FILENAME, dtype=int)  # This file exist for sure
    else:
        hf_first_comp = 0
    if (hf_first_comp == 0):  # Compute starting solution
        x, y, z = reset_vars(deta, T_e, T_w, N_p, eta_max)
    else:  # Read the previous solution
        x = np.loadtxt(X_VAR_FILENAME)  # Array to store the eta values
        y = np.loadtxt(Y_VAR_FILENAME)  # Array to store the F values of the boundary layer
        z = np.loadtxt(Z_VAR_FILENAME)  # Array to store the g values of the boundary layer
        x = x.tolist() 
        y = y.tolist() 
        z = z.tolist()
    # Compute the edge properties:
    rho_e, mu_e = heat_flux_hf_law0_properties_file.heat_flux_hf_law0_edge(P_e, T_e, mixture_object)
    # Compute the wall properties:
    rho_w, lambda_eq_wall = heat_flux_hf_law0_properties_file.heat_flux_hf_law0_wall(P_e, T_w, mixture_object)  
    # Start the convergence loop
    iter = 0
    already_reset = False  # Flag to understand if we already reset the boundary layer variables
    while (iter < max_iter):
        iter += 1
        # Compute useful properties across the boundary layer:
        l_0, rr, chi, C_p, redo = properties_across_BL(T_e, P_e, mu_e, rho_e, z, N_p, mixture_object, max_T_relax)
        if (redo == True):  # We need to redo the computation
            if (already_reset == True):  # If we already reset the BL variables, we stop the computation
                raise ValueError("ERROR: T<=0, nan or T>T_max, resetting BL vars...FAILED")
            print("ERROR: T<=0, nan or T>T_max, resetting BL vars...")
            # Reset the boundary layer variables
            x, y, z = reset_vars(deta, T_e, T_w, N_p, eta_max)
            # Compute the properties across the boundary layer again
            l_0, rr, chi, C_p, redo = properties_across_BL(T_e, P_e, mu_e, rho_e, z, N_p, mixture_object, max_T_relax)
            if (redo == True):  # The reset failed
                raise ValueError("ERROR: T<=0, nan or T>T_max, resetting BL vars...FAILED")
            already_reset = True
        # Continuity equation:
        aa = []
        for i in range(0, N_p):
            aa.append(-y[i])  # Coefficients for the continuity equation
        V = continuity_file.continuity(deta, aa)  # Slve the continuity equation
        # MOMENTUM EQUATION:
        dl_0 = first_deriv_file.first_deriv_array(l_0, deta, ORDER)  # Compute dl_0/deta
        # Reset the aa, bb and dd vectors
        aa = [] 
        bb = [] 
        dd = [] 
        # Coefficients for the linear equation to solve:
        for i in range(0, N_p):
            aa.append( l_0[i]/pow(deta,2) )
            bb.append( (dl_0[i]-V[i])/deta ) 
            dd.append( 0.5*(pow(y[i],2)-rr[i]) )
        f_init = 0  # Initial condition for eta=0
        f_final = 1  # Final condition for eta=eta_max
        new_f = eq_diff_solve_file.solver(aa, bb, dd, f_init, f_final)  # Solve it
        # ENERGY EQUATION:
        dchi = first_deriv_file.first_deriv_array(chi, deta, ORDER)  # Compute dchi/deta
        # Reset the aa, bb and dd vectors
        aa = [] 
        bb = [] 
        dd = [] 
        # Coefficients for the linear equation to solve:
        for i in range(0, N_p):
            aa.append( chi[i]/C_p[i]/pow(deta,2) )
            bb.append( (dchi[i]/C_p[i]-V[i])/deta )
            dd.append(0)
        g_init = T_w/T_e  # Initial condition for eta=0
        g_final = 1  # Final condition for eta=eta_max
        new_g = eq_diff_solve_file.solver(aa,bb,dd, g_init, g_final)  # Slve it
        stop = True 
        # CONVERGENCE CHECK: for each point, I check if the residuals are below the convergence criteria
        res = 0
        for i in range(0, N_p):
            if( abs(new_f[i]-y[i]) > hf_conv or abs(new_g[i]-z[i]) > hf_conv ):  
                res = max(res, abs(new_f[i]-y[i]), abs(new_g[i]-z[i])) 
                stop = False  # Do not stop the loop
                break
        if(stop or iter >= max_iter):  # If we converged or we reached the maximum number of iterations
            if(stop == False and log_warning_hf == True):
                print("Warning: a heat flux computation did not converge for the current iteration.")
                print("The maximum residual is: " + str(res))
                bad_convergence = True
            break  # Stop the loop
        # If we did not converge, we need to update the x,y,z arrays
        w = 0.5  # Relaxation factor
        for i in range(0, N_p):
            y[i] = (1-w)*y[i]+w*new_f[i]
            z[i] = (1-w)*z[i]+w*new_g[i]
    # HEAT FLUX COMPUTATION:
    dg_v = first_deriv_file.first_deriv_array(z, deta, ORDER)  # Compute dg/deta
    # Take the value of dg on the wall, eta=0
    dg = dg_v[0] 
    # Compute the heat flux
    q = math.sqrt(2/(rho_e*mu_e))*dg*T_e*rho_w*lambda_eq_wall 
    q = q*math.sqrt(beta)  #beta=stagvar*u/Rm, velocity gradient
    if (use_prev_ite==True and stop==True):  
        # If we converged and we want to use this solution as starting solution
        # for the next heat flux computation in this case, we save it
        np.savetxt(X_VAR_FILENAME, x) 
        np.savetxt(Y_VAR_FILENAME, y) 
        np.savetxt(Z_VAR_FILENAME, z)
        if (hf_first_comp == 0):  # Update the hf_first_comp variable
            hf_first_comp = np.array([1])
            np.savetxt(USE_PREV_ITE_FILENAME, hf_first_comp, fmt = "%1.1u")
    return q, bad_convergence
#.................................................
#   Possible improvements:
#   - Make the central finite derivative order variable
#   - Improve the diff eq algorithm
#   - Dynamic relaxation factor
#   - Better starting profile
#   - The reset for failed computations could be improved
#.................................................
#   KNOW PROBLEMS:
#   None.
#.................................................