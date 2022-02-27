## GWTC.py
# all functions related to estimating the redshift of current GW observations from the GWTC catalog


# imports
from scipy.misc import derivative
from random import gauss
import pandas

# local imports
from .cosmology import H, dL


# generate GWTC events
def generate():
    # get raw data from the GWTC file
    with open(__file__.replace("GWTC.py", "") + "data/GWTC.csv", "r") as file:
        columns = pandas.read_csv(file, comment="#")
        distances_mid = columns["luminosity_distance"]
        distances_lower = columns["luminosity_distance_lower"]
        distances_upper = columns["luminosity_distance_upper"]
        redshifts_mid = columns["redshift"]
        redshifts_lower = columns["redshift_lower"]
        redshifts_upper = columns["redshift_upper"]

    # symmetrize luminosity distance errors and convert Mpc to Gpc
    distances = []
    disterrors = []
    for i in range(0, len(distances_mid)):
        distance = ( distances_mid[i] + (distances_upper[i] + distances_lower[i])/2 ) / 1000
        disterror = ( (distances_upper[i] - distances_lower[i])/2 ) / 1000
        distances.append(distance)
        disterrors.append(disterror)

    # symmetrize the redshift error
    redshifts = []
    rederrors = []
    for i in range(0, len(redshifts_mid)):
        redshift = ( redshifts_mid[i] + (redshifts_upper[i] + redshifts_lower[i])/2 )
        rederror = ( (redshifts_upper[i] - redshifts_lower[i])/2 )
        redshifts.append(redshift)
        rederrors.append(rederror)

    # propagate the redshift error to the luminosity distance
    errors = []
    for i in range(0, len(redshifts_mid)):
        propagatedredshifterror = derivative(dL, redshifts[i], dx=1e-6, args=(H,)) * rederrors[i]
        errors.append((disterrors[i]**2 + propagatedredshifterror**2)**0.5)

    return redshifts, distances, errors
