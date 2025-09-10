#.................................................
#   HEAT_FLUX_HF_LAW0_PROPERTIES.PY, v2.0.0, December 2024, Domenico Lanza.
#.................................................
#   This module is needed to compute the 
#   flow properties in the heat flux model with hf_law=0
#.................................................

def heat_flux_hf_law0_edge(P_e,T_e,mixture):
    """This function computes the flow edge 
    properties for the mixture.

    Args:
        P_e (float): The edge pressure
        T_e (float): The edge temperature
        mixture (mpp.Mixture): The mixture object

    Returns:
        rho_e (float): The edge density
        mu_e (float): The edge viscosity
    """
    
    # Computation:
    mixture.equilibrate(T_e, P_e)  # Equilibrate the mixture
    rho_e = mixture.density() # Density
    mu_e = mixture.viscosity()  # Viscosity
    return rho_e, mu_e

def heat_flux_hf_law0_wall(P_w, T_w, mixture):
    """This function computes the flow wall 
    properties for the mixture.

    Args:
        P_w (float): The wall pressure
        T_w (float): The wall temperature
        mixture (mpp.Mixture): The mixture object

    Returns:
        rho_w (float): The wall density
        lambda_eq_wall (float): The wall thermal conductivity
    """
    # Computation:
    mixture.equilibrate(T_w, P_w)  # Equilibrate the mixture
    rho_w = mixture.density()  # Density
    lambda_eq_wall = mixture.equilibriumThermalConductivity()  # Thermal conductivity
    return rho_w, lambda_eq_wall 

def heat_flux_hf_law0_flow(P, T, mixture):
    """This function computes the flow properties inside 
    the boundary layer.

    Args:
        P (float): Pressure
        T (float): Temperature
        mixture (mpp.Mixture): The mixture object

    Returns:
        rho (float): The density
        cp (float): The specific heat
        mu (float): The viscosity
        lambda_eq (float): The thermal conductivity
    """
    # Computation:
    mixture.equilibrate(T, P)  # Equilibrate the mixture
    rho = mixture.density()  # Density
    cp = mixture.mixtureEquilibriumCpMass()  # Specific heat at constant pressur
    mu = mixture.viscosity()  # Viscosity
    lambda_eq = mixture.equilibriumThermalConductivity()  # Thermal conductivity
    return rho, cp, mu, lambda_eq 
#.................................................
#   Possible improvements:
#   None.
#.................................................
#   KNOW PROBLEMS:
#   None.
#.................................................