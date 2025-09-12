"""
@file out_properties.py

@brief Collect and organize final flow properties for output.

Copyright (C) 2023-2025 The Board of Trustees of the University of Illinois.
All rights reserved.

This file is part of PlasFlowSolver: a data reduction model for ICP wind tunnels.

PlasFlowSolver is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

PlasFlowSolver is distributed in the hope that it will be useful, 
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with PlasFlowSolver.  If not, see 
<http://www.gnu.org/licenses/>.
"""

#.................................................
#   OUT_PROPERTIES.PY, v2.0.0, December 2024, Domenico Lanza.
#.................................................
#   This module is needed to compute and
#   organize the final flow properties in 
#   order to output them.
#.................................................
from utils.classes import OutProperties

def append_error_case(
    has_converged_out, rho_out, T_out, h_out, u_out, a_out, M_out, T_t_out,
    h_t_out, P_t_out, Re_out, Kn_out, warnings_out, res_out, type_error
    ):
    """This function appends the error case to the output vectors.
    
    Args and Returns:
        has_converged_out (list): variable to store if the iteration has converged
        rho_out (list): free stream density
        T_out (list): free stream temperature
        h_out (list): free stream enthalpy
        u_out (list): free stream velocity
        a_out (list): free stream sound speed
        M_out (list): free stream Mach number
        T_t_out (list): total temperature
        h_t_out (list): total enthalpy
        P_t_out (list): total pressure
        Re_out (list): Pitot Reynolds number
        Kn_out (list): free stream Knudsen number
        warnings_out (list): warnings
        res_out (list): final convergence criteria
    """
    rho_out.append(-1)
    T_out.append(-1)
    h_out.append(-1)
    u_out.append(-1)
    a_out.append(-1)
    M_out.append(-1)
    T_t_out.append(-1)
    h_t_out.append(-1)
    P_t_out.append(-1)
    Re_out.append(-1)
    Kn_out.append(-1)
    res_out.append(-1)
    if (type_error == 0):
        has_converged_out.append("Error: invalid data")
        warnings_out.append("Error: invalid data")
    elif (type_error == 1):
        has_converged_out.append("Error detected during the computation.")
        warnings_out.append("Error detected during the computation.")
    else:
        raise ValueError("Error: invalid error type.")
    
    return (
        has_converged_out, rho_out, T_out, h_out, u_out, a_out, M_out, T_t_out,
        h_t_out, P_t_out, Re_out, Kn_out, warnings_out, res_out
    )

def append_output_case(
    rho_out, T_out, h_out, u_out, a_out, M_out, T_t_out,
    h_t_out, P_t_out, Re_out, Kn_out, warnings_out, res_out,
    rho, T, h, u, a, M, T_t, h_t, P_t, Re, Kn, warnings, res
    ):
    """This function appends the output case to the output vectors.
    
    Args and Returns:
        rho_out (list): free stream density
        T_out (list): free stream temperature
        h_out (list): free stream enthalpy
        u_out (list): free stream velocity
        a_out (list): free stream sound speed
        M_out (list): free stream Mach number
        T_t_out (list): total temperature
        h_t_out (list): total enthalpy
        P_t_out (list): total pressure
        Re_out (list): Pitot Reynolds number
        Kn_out (list): free stream Knudsen number
        warnings_out (list): warnings
        res_out (list): final convergence criteria
        rho (float): free stream density
        T (float): free stream temperature
        h (float): free stream enthalpy
        u (float): free stream velocity
        a (float): free stream sound speed
        M (float): free stream Mach number
        T_t (float): total temperature
        h_t (float): total enthalpy
        P_t (float): total pressure
        Re (float): Pitot Reynolds number
        Kn (float): free stream Knudsen number
        warnings (str): warnings
        res (float): final convergence criteria
        """
    rho_out.append(rho)
    T_out.append(T)
    h_out.append(h)
    u_out.append(u)
    a_out.append(a)
    M_out.append(M)
    T_t_out.append(T_t)
    h_t_out.append(h_t)
    P_t_out.append(P_t)
    Re_out.append(Re)
    Kn_out.append(Kn)
    warnings_out.append(warnings)
    res_out.append(res)
    return (
        rho_out, T_out, h_out, u_out, a_out, M_out, T_t_out,
        h_t_out, P_t_out, Re_out, Kn_out, warnings_out, res_out
    )

def initialize_output_vectors():
    """This function initializes the output vectors.
    
    Returns:
        has_converged_out (list): variable to store if the iteration has converged
        rho_out (list): free stream density
        T_out (list): free stream temperature
        h_out (list): free stream enthalpy
        u_out (list): free stream velocity
        a_out (list): free stream sound speed
        M_out (list): free stream Mach number
        T_t_out (list): total temperature
        h_t_out (list): total enthalpy
        P_t_out (list): total pressure
        Re_out (list): Pitot Reynolds number
        Kn_out (list): free stream Knudsen number
        warnings_out (list): warnings
        res_out (list): final convergence criteria
        species_names_out (dict): dictionary to store the names of the species to be written on the output file
        species_Y_out (dict): dictionary to store the mass fractions of the species to be written on the output file
        run_time_vect (list): vector to store the run time of each case
    """
    # Initialize the output vectors
    has_converged_out = []  # Variable to store if the iteration has converged
    rho_out = []  # Free stream density
    T_out = []  # Free stream temperature
    h_out = []  # Free stream enthalpy
    u_out = []  # Free stream velocity
    a_out = []  # Free stream sound speed
    M_out = []  # Free stream Mach number
    T_t_out = []  # Total temperature
    h_t_out = []  # Total enthalpy
    P_t_out = []  # Total pressure
    Re_out = []  # Pitot Reynolds number
    Kn_out = []  # Free stream Knudsen number
    warnings_out = []  # Warnings 
    res_out = []  # Final convergence criteria 
    species_names_out = {}  # Dictionary to store the names of the species to be written on the output file
    species_Y_out = {}  # Dictionary to store the mass fractions of the species to be written on the output file
    run_time_vect = []  # Vector to store the run time of each case
    return (
        has_converged_out, rho_out, T_out, h_out, u_out, a_out, M_out, T_t_out, 
        h_t_out, P_t_out, Re_out, Kn_out, warnings_out, res_out,
        species_names_out, species_Y_out, run_time_vect
    )

def enthalpy_shift(mixture_object, P):
    """This function computes the enthalpy shift.

    Args:
        mixture_object (mpp.Mixture): the mixture object
        P (float): pressure

    Returns:
        h0 (float): enthalpy shift
    """
    # Constants:
    T0 = 298.15  # Reference temperature
    # Computation:
    mixture_object.equilibrate(T0, P)
    h0 = mixture_object.mixtureHMinusH0Mass()
    return h0

def out_properties(mixture_object, T, P, u):
    """This function computes the final properties of the gas.

    Args:
        mixture_object (mpp.Mixture): the mixture object
        T (float): temperature
        P (float): pressure
        u (float): velocity
    Returns:
        rho (float): density
        a (float): sound speed
        M (float): mach number
        h (float): enthalpy
        h_t (float): total enthalpy
        mfp (float): mean free path
    """
    # Compute enthalpy shift
    h0 = enthalpy_shift(mixture_object, P)
    # Compute properties
    mixture_object.equilibrate(T, P) 
    rho = mixture_object.density() 
    a = mixture_object.equilibriumSoundSpeed() 
    M = u/a 
    h = mixture_object.mixtureHMass() + h0
    h_t = h + 0.5*pow(u,2)
    mfp = mixture_object.meanFreePath()
    return rho, a, M, h, h_t, mfp

def mass_fraction_composition(mixture_object, T, P):
    """This function computes the mass fraction composition of the gas.

    Args:
        mixture_object (mpp.Mixture): the mixture object
        T (float): temperature
        P (float): pressure

    Returns:
        species_names (list): list of species names 
        species_Y (list): list of mass fractions
    """
    # Variables:
    species_names = []
    species_Y = []
    # Computation:
    mixture_object.equilibrate(T, P)  # Equilibrate the mixture
    n_species = mixture_object.nSpecies()  # Number of species
    for i in range(n_species):
        species_names.append(mixture_object.speciesName(i))  # Append species name
    species_Y = mixture_object.Y()  # Retrieve mass fractions
    # Return:
    return species_names, species_Y

def return_out_object(
    has_converged_out, rho_out, T_out, h_out, u_out, a_out, M_out, T_t_out,
    h_t_out, P_t_out, Re_out, Kn_out, warnings_out, res_out,
    species_names_out, species_Y_out
    ):
    """This function returns the output object.

    Args:
        has_converged_out (list): variable to store if the iteration has converged
        rho_out (list): free stream density
        T_out (list): free stream temperature
        h_out (list): free stream enthalpy
        u_out (list): free stream velocity
        a_out (list): free stream sound speed
        M_out (list): free stream Mach number
        T_t_out (list): total temperature
        h_t_out (list): total enthalpy
        P_t_out (list): total pressure
        Re_out (list): Pitot Reynolds number
        Kn_out (list): free stream Knudsen number
        warnings_out (list): warnings
        res_out (list): final convergence criteria
        species_names_out (dict): dictionary to store the names of the species to be written on the output file
        species_Y_out (dict): dictionary to store the mass fractions of the species to be written on the output file

    Returns:
        out_object (dict): output object
    """
    # Initialize the output object
    out_object = OutProperties()
    # Assign the values
    out_object.has_converged_out = has_converged_out
    out_object.rho_out = rho_out
    out_object.T_out = T_out
    out_object.h_out = h_out
    out_object.u_out = u_out
    out_object.a_out = a_out
    out_object.M_out = M_out
    out_object.T_t_out = T_t_out
    out_object.h_t_out = h_t_out
    out_object.P_t_out = P_t_out
    out_object.Re_out = Re_out
    out_object.warnings_out = warnings_out
    out_object.res_out = res_out
    out_object.Kn_out = Kn_out
    out_object.species_names_out = species_names_out
    out_object.species_Y_out = species_Y_out
    return out_object
#.................................................
#   Possible improvements:
#   - Add more options for enthalpy shift
#.................................................
#   KNOW PROBLEMS:
#   -None
#.................................................