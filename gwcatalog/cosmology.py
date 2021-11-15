## cosmology.py
# default cosmological model: ΛCDM with Ωm = 0.284 and h = 0.7


# imports
from scipy.integrate import quad


# Hubble function
def H(z):
    # option 1: using c/H0 = (2.9979 Gpc)/h and providing the value for h
    h = 0.7
    H0 = 299792458*h/(2.9979*3.085678*10**25)

    # option 2: providing the value for H0 in units of [(km/s)/Mpc]
    #H0 = 70
    #H0 = H0*3.240779289*10**(-20)

    # option 3: providing the value for H0 directly in [s⁻¹]
    #H0 = 2.2685641027252412e-18

    # value for Ωm
    Ωm = 0.284

    return H0*(Ωm*(1+z)**3 + 1-Ωm)**0.5


# luminosity distance
def dL(z, H):
    c = 9.715611890800001e-18  # speed of light [Gpc/s]
    return (1+z) * c * quad(lambda Z: 1/H(Z), 0, z)[0]
