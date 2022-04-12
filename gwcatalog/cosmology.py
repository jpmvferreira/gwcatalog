## cosmology.py
# default cosmological model: ΛCDM with Ωm = 0.315 and H0 = 67.4


# imports
from scipy.integrate import quad


# Hubble function
def H(z):
    # provide the value for H0 in units of (km/s)/Mpc and convert it so s⁻¹
    H0 = 67.4
    H0 = H0*3.240779289*10**(-20)

    # value for Ωm
    Ωm = 0.315

    return H0*(Ωm*(1+z)**3 + 1-Ωm)**0.5


# luminosity distance
def dL(z, H):
    c = 9.715611890800001e-18  # speed of light [Gpc/s]
    return (1+z) * c * quad(lambda Z: 1/H(Z), 0, z)[0]
