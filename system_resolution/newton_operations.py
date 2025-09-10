#.................................................
#   NEWTON_OPERATIONS.PY, v2.0.0, December 2024, Domenico Lanza.
#.................................................
#   This module is needed to perform some operations
#   for the Newton-Raphson's method.
#.................................................
import random  # Standard library for random operations
import math  # Standard library for mathematical operations
import system_resolution.thermodyn as thermodyn_file  # Thermodynamic functions
import system_resolution.barker_effect as barker_effect_file  # Barker effect functions
import heat_flux.heat_flux as heat_flux_file  # Heat flux functions
from utils.classes import ProgramConstants

def under_relaxation(settings_object, probes_object, T_star, u_star, T_t_star, P_t_star, T, u, T_t, P_t, d_vars):
    """ This function is used to relax the new values of the variables
    if they are too low or too high after a Newton-Raphson's iteration.

    Args:
        settings_object: An object containing the settings of the simulation.
        probes_object: An object containing the probes of the simulation.
        T_star: The new value of the temperature.
        u_star: The new value of the velocity.
        T_t_star: The new value of the temperature of the turbine.
        P_t_star: The new value of the pressure of the turbine.
        T: The current value of the temperature.
        u: The current value of the velocity.
        T_t: The current value of the temperature of the turbine.
        P_t: The current value of the pressure of the turbine.
        d_vars: The increments of the variables.
    Returns:
        T_star: The relaxed value of the temperature.
        u_star: The relaxed value of the velocity.
        T_t_star: The relaxed value of the temperature of the turbine.
        P_t_star: The relaxed value of the pressure of the turbine.
    """
    # Relaxation factor:
    relax = 1.0
    # If the new valus are too low, relax them:
    while ( (T_star < settings_object.min_T_relax) or (u_star < 0) or 
            (T_t_star < settings_object.min_T_relax) or (P_t_star < 0) or 
            (T_t_star < probes_object.T_w) ): 
        relax = relax/2  # Halve the relaxation factor
        # New values:
        T_star = T + d_vars[0]*relax
        u_star = u + d_vars[1]*relax
        T_t_star = T_t + d_vars[2]*relax
        if (probes_object.barker_type != 0):
            P_t_star = P_t + d_vars[3]*relax
    # If the new values are too high, we relax them:
    while ( (T_star > settings_object.max_T_relax) or (T_t_star > settings_object.max_T_relax)):
        relax = relax/2  # Halve the relaxation factor
        # New values:
        T_star = T + d_vars[0]*relax
        u_star = u + d_vars[1]*relax
        T_t_star = T_t + d_vars[2]*relax
        if (probes_object.barker_type != 0):
            P_t_star = P_t + d_vars[3]*relax
    return T_star, u_star, T_t_star, P_t_star

def dynamic_jacobian_diff(cnv, cnv_old, cnv_ref, res, settings_object, probes_object, T, u, T_t, P_t, P, q_target, P_stag, mixture_object, h, h_t, s, s_t, P_b):
    """The goal of this function is to dynamically change the Jacobian step
    to avoid situations in which the Newton-Raphson's method gets stuck.
    """
    # Constants:
    program_constants = ProgramConstants()
    DCNV_PERCENT = program_constants.DynJac.DCNV_PERCENT  # Percentage difference of the convergence
    JAC_DIFF_MAX = program_constants.DynJac.JAC_DIFF_MAX  # Maximum Jacobian step
    JAC_DIFF_INCREASE = program_constants.DynJac.JAC_DIFF_INCREASE  # Jacobian step increase factor
    VARS_INCREASE = program_constants.DynJac.VARS_INCREASE  # Variables increase factor
    OFFSET_T_T = program_constants.DynJac.OFFSET_T_T  # Offset for the temperature of the turbine
    # Initialize:
    cnv_new = cnv
    # Compute the percentage difference of the convergence:
    dcnv_perc = abs(cnv_old - cnv)/cnv_old
    if (dcnv_perc < DCNV_PERCENT and settings_object.jac_diff < JAC_DIFF_MAX):
        # Increase the Jacobian step:
        settings_object.jac_diff *= JAC_DIFF_INCREASE
        print("New residual: " + str(cnv) + "is too close to the old residual.")
        print("Jac_diff increased to " + str(settings_object.jac_diff))
        # Move the variables a little bit to unstuck the Newton-Raphson's method:
        T += T*VARS_INCREASE*random.choice([1,-1])
        u += u*VARS_INCREASE*random.choice([1,-1])
        T_t += T_t*VARS_INCREASE*random.choice([1,-1])
        if (probes_object.barker_type != 0):
            P_t += P_t*VARS_INCREASE*random.choice([1,-1])
        # Check if the variables are too low or too high:
        if (T < settings_object.min_T_relax):
            T = settings_object.min_T_relax
        if(T_t>settings_object.max_T_relax):
            T_t = settings_object.max_T_relax - OFFSET_T_T
        # Recompute residuals:
        try:
            q = heat_flux_file.heat_flux(probes_object, settings_object, P_t, T_t, u, mixture_object)[0]  # Heat flux
        except Exception as e:
            raise Exception("Error encountered during the heat flux computation: "+str(e))
        h = thermodyn_file.enthalpy(mixture_object, P, T)  # Free stream enthalpy
        h_t = thermodyn_file.enthalpy(mixture_object, P_t, T_t)  # Total enthalpy
        s = thermodyn_file.entropy(mixture_object,P,T)  # Free stream entropy
        s_t = thermodyn_file.entropy(mixture_object,P_t,T_t)  # Total entropy
        P_b = barker_effect_file.barker_effect(probes_object, mixture_object, P_t, P, T, u)[0]  # Barker effect
        res = []
        res.append(-(q-q_target))  # Heat flux residual
        res.append(-(h_t-(h+0.5*pow(u,2))))  # Enthalpy residual
        res.append(-(s_t-s))  # Entropy residual
        res.append(-(P_b-P_stag))  # Barker effect residual
        cnv_new = 0
        for i in range(len(res)):
            cnv_new += pow(res[i],2)
        cnv_new = math.sqrt(cnv_new)/cnv_ref
    return cnv_new, res, settings_object, T, u, T_t, P_t, h, h_t, s, s_t, P_b
#.................................................
#   Possible improvements:
#   - Improve relaxation scheme.
#   - Improve dynamic Jacobian step.
#.................................................
#   KNOW PROBLEMS:
#   None.
#.................................................