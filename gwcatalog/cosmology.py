## cosmology.py
# default cosmological model: ΛCDM with Ωm = 0.284 and h = 0.7


# imports
from scipy.integrate import quad


# Hubble function
def H(z):
    H0 = 2.2685641027252412e-18  # Hubble constant [s⁻¹]
    return H0*(0.284*(1+z)**3 + 0.717)**0.5


# luminosity distance
def dL(z, H):
    c = 9.715611890800001e-18  # speed of light [Gpc/s]
    return (1+z) * c * quad(lambda Z: 1/H(Z), 0, z)[0]
