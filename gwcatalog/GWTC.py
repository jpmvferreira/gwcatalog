## GWTC.py
# all functions related to estimating the redshift of current GW observations from the GWTC catalog


# imports
from random import gauss
import pandas

# local imports
from .auxiliary import dL_to_redshift
from .cosmology import H, dL


# generate GWTC events
def generate(ideal=False, multiplier=1):
    # get raw data from the GWTC file
    with open(__file__.replace("GWTC.py", "") + "data/GWTC.csv", "r") as file:
        columns = pandas.read_csv(file, comment="#")
        distances_mid = columns["luminosity_distance"]
        distances_lower = columns["luminosity_distance_lower"]
        distances_upper = columns["luminosity_distance_upper"]

    # symmetrize luminosity distance errors and convert Mpc to Gpc
    distances = []
    errors = []
    for i in range(0, len(distances_mid)):
        distance = ( distances_mid[i] + (distances_upper[i] + distances_lower[i])/2 ) / 1000
        error = ( (distances_upper[i] - distances_lower[i])/2 ) / 1000
        distances.append(distance)
        errors.append(multiplier*error)

    # get redshifts from the events luminosity distance
    # assumes that highest redshift is 1 and uses 2000 steps in between z = 0 and z = 1
    redshifts = dL_to_redshift(distances, 0, 1, 2000)

    # generate new luminosity distances based on the real luminosity distances, with a gaussian error
    if not ideal:
        for i in range(0, len(distances)):
            rnd = -1
            while rnd < 0:
                rnd = gauss(distances[i], errors[i])
            distances[i] = round(rnd, 3)

    return redshifts, distances, errors
