#.................................................
#   THERMODYN.PY, v2.0.0, December 2024, Domenico Lanza.
#.................................................
#   This module is needed to compute the enthalpy 
#   and entropy given the pressure and the temperature.
#.................................................

def enthalpy(mixture_object, P, T):
    """This function returns the enthalpy of the fluid 
    given the pressure and the temperature.

    Args:
        mixture_object (mpp.Mixture): the mixture of the case
        P (float): pressure
        T (float): temperature

    Returns:
        h (float): enthalpy
    """
    # Compute the enthalpy:
    mixture_object.equilibrate(T, P)  # I equilibrate the mixture
    h = mixture_object.mixtureHMass() # I compute the enthalpy
    return h

def entropy(mixture_object, P, T): 
    """This function returns the entropy of the fluid 
    given the pressure and the temperature.

    Args:
        mixture_object (mpp.Mixture): the mixture of the case
        P (float): pressure
        T (float): temperature
    Returns:
        s (float): entropy
    """
    # Compute the entropy:
    mixture_object.equilibrate(T, P)  # I equilibrate the mixture
    s = mixture_object.mixtureSMass()  # I compute the entropy
    return s 
#.................................................
#   Possible improvements:
#   None.
#.................................................
#   KNOW PROBLEMS:
#   None.
#.................................................