#.................................................
#   JACOBIAN_MATRIX.PY, v2.0.0, December 2024, Domenico Lanza.
#.................................................
#   This module is needed to compute the Jacobian matrix of the system
#   in order to use the Newton-Raphson's method.
#.................................................
import system_resolution.thermodyn as thermodyn_file  # Module to compute the enthalpy
import system_resolution.barker_effect as barker_effect_file  # Module to compute the Barker's effect
import heat_flux.heat_flux as heat_flux_file  # Module to compute the heat flux

def jacobian_matrix(probes, settings, T, T_t, P, P_t, P_b, q, h, h_t, s, s_t, u, mixture_object):
    """This function returns the Jacobian matrix of the system in order to use 
    the Newton-Raphson's method.

    Args:
        probes (probes_class): Probes of the system
        settings (settings_class): Settings of the program
        T (float): Flow temperature
        T_t (float): Flow total temperature
        P (float): Flow pressure
        P_t (float): Flow total pressure
        P_b (float): Barker's pressure
        q (float): Stagnation heat flux
        h (float): Flow enthalpy
        h_t (float): Flow total enthalpy
        s (float): Flow entropy 
        s_t (float): Flow total entropy 
        u (float): Flow velocity
        mixture_object (mpp.Mixture): mixture of the case

    Returns:
        jac (square matrix, float): The Jacobian matrix
    """
    # Retrieve useful settings:
    jac_diff = settings.jac_diff  # Finite difference for the Jacobian matrix
    barker_type = probes.barker_type  # Type of Barker correction
    #.................................................
    # Derivatives wrt T:
    delta = T*jac_diff  # Temperature increment for the finite difference
    T_star = T + delta  # New temperature for the finite difference
    # Compute new properties:
    h_star = thermodyn_file.enthalpy(mixture_object, P, T_star)
    s_star = thermodyn_file.entropy(mixture_object, P, T_star)
    P_b_star = barker_effect_file.barker_effect(probes, mixture_object, P_t, P, T_star, u)[0]  # Retrieve only the pressure
    # Derivatives:
    dh_dt = (h_star-h)/delta  # Derivative of h(P, T) w.r.t. T
    ds_dt = (s_star-s)/delta  # Derivative of s(P, T) w.r.t. T
    db_dt = (P_b_star-P_b)/delta  # Derivative of P_b(P_t, P, T, u) w.r.t. T
    #.................................................
    # Derivatives wrt u:
    delta = u*jac_diff  # Velocity increment for the finite difference
    u_star = u + delta  # New velocity for the finite difference
    # Compute new properties:
    q_star = heat_flux_file.heat_flux(probes, settings, P_t, T_t, u_star, mixture_object)[0]
    P_b_star = barker_effect_file.barker_effect(probes, mixture_object, P_t, P, T, u_star)[0]
    # Derivatives:
    dq_du = (q_star-q)/delta  # Derivative of q(P_t, T_t, u) w.r.t. u
    db_du = (P_b_star-P_b)/delta  # Derivative of P_b(P_t, P, T, u) w.r.t. u
    #.................................................
    # Derivatives wrt T_t:
    delta = T_t*jac_diff  # Total temperature increment for the finite difference
    T_t_star = T_t + delta  # New total temperature for the finite difference
    # Compute new properties:
    q_star = heat_flux_file.heat_flux(probes, settings, P_t, T_t_star, u, mixture_object)[0]
    h_t_star = thermodyn_file.enthalpy(mixture_object, P_t, T_t_star)
    s_t_star = thermodyn_file.entropy(mixture_object, P_t, T_t_star)
    # Derivatives:
    dq_dtt = (q_star-q)/delta  # Derivative of q(P_t, T_t, u) w.r.t. T_t
    dht_dtt = (h_t_star-h_t)/delta  # Derivative of h_t(P_t, T_t) w.r.t. T_t
    dst_dtt = (s_t_star-s_t)/delta  # Derivative of s_t(P_t, T_t) w.r.t. T_t
    #.................................................
    # Derivatives wrt P_t: (if Barker effect is active)
    if (barker_type != 0):
        delta = P_t*jac_diff  # Total pressure increment for the finite difference
        P_t_star = P_t + delta  # New total pressure for the finite difference
        # Compute new properties:
        q_star = heat_flux_file.heat_flux(probes, settings, P_t_star, T_t, u, mixture_object)[0]
        h_t_star = thermodyn_file.enthalpy(mixture_object, P_t_star, T_t)
        s_t_star = thermodyn_file.entropy(mixture_object, P_t_star, T_t)
        P_b_star = barker_effect_file.barker_effect(probes, mixture_object, P_t_star, P, T, u)[0]  # I retrieve only the pressure
        # Derivatives:
        dq_dpt = (q_star-q)/delta  # Derivative of q(P_t, T_t, u) w.r.t. P_t
        dht_dpt = (h_t_star-h_t)/delta  # Derivative of h_t(P_t, T_t) w.r.t. P_t
        dst_dpt = (s_t_star-s_t)/delta  # Derivative of s_t(P_t, T_t) w.r.t. P_t
        db_dpt = (P_b_star-P_b)/delta  # Derivative of P_b(P_t, P, T, u) w.r.t. P_t
    else:  # Set to zero if Barker effect is not active
        dq_dpt = 0
        dht_dpt = 0
        dst_dpt = 0
        db_dpt = 0
    #.................................................
    # JACOBIAN MATRIX:
    jac = [[0.0 for i in range(4)] for j in range(4)]  # Initialize the Jacobian matrix
    # According to the system of equations:
    jac[0][0] = 0
    jac[0][1] = dq_du
    jac[0][2] = dq_dtt
    jac[1][0] = -dh_dt
    jac[1][1] = -u
    jac[1][2] = dht_dtt
    jac[2][0] = -ds_dt
    jac[2][1] = 0
    jac[2][2] = dst_dtt
    jac[0][3] = dq_dpt
    jac[1][3] = dht_dpt
    jac[2][3] = dst_dpt
    jac[3][0] = db_dt 
    jac[3][1] = db_du
    jac[3][2] = 0
    jac[3][3] = db_dpt
    return jac
#.................................................
#   Possible improvements:
#   - Change to a central finite diffence method
#   - Improve order of the derivatives
#   - Add penality method for Mach number
#.................................................
#   KNOW PROBLEMS:
#   None.
#.................................................