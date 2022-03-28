## auxiliary.py
# auxiliary functions defined for convenience to help in internal tasks


# imports
from scipy.optimize import fsolve
from random import uniform, gauss
import numpy as np
import sys
import os

# local imports
from .cosmology import H, dL


# get N randomly generated events from a given distribution, using rejection
def GetRandom(distribution, x_min, x_max, y_min, y_max, N=1):
    counter = 0
    events = []

    while counter < N:
        x = uniform(x_min, x_max)
        y = uniform(y_min, y_max)

        if y < distribution(x):
            events.append(x)
            counter += 1

    return events


# get the theoretical line for luminosity distance
def dL_line(zmin, zmax, N=1000):
    # protection against invalid arguments
    if (zmin < 0 or zmax < 0) or (zmax < zmin):
        raise Exception("Please specify a valid redshifts interval.")

    # create a "solid line" and compute distances for that line
    line = np.linspace(zmin, zmax, N)
    distances = [dL(i, H) for i in line]

    return line, distances

# convert luminosity distance to redshift
def dL_to_redshift(distance, z0=0):
    # auxiliary function to solve using scipy
    def func(z, distance, H):
        return distance - dL(z, H)

    # compute the redshift for the provided luminosity distance
    redshift = fsolve(func, z0, args=(distance, H))[0]

    return redshift


# distribute the events around the most likely value using a gaussian distribution, with protection against negative values
def distribute(distances, errors):
    for i in range(0, len(distances)):
        newdistance = -1
        while newdistance < 0:
            newdistance = gauss(distances[i], errors[i])
        distances[i] = newdistance

    return distances, errors
