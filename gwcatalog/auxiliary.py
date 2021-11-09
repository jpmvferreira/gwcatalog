## auxiliary.py
# auxiliary functions defined for convenience to help in internal tasks


# imports
from bisect import bisect_right
from random import uniform
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
def dL_line(min, max, N=1000):
    # protection against invalid arguments
    if (min < 0 or max < 0) or (max < min):
        raise Exception("Please specify a valid interval for redshifts.")

    # create a "solid line" and compute distances for that line
    line = np.linspace(min, max, N)
    distances = [dL(i, H) for i in line]

    return line, distances


# find rightmost value less than or equal to x
def find_le(a, x):
    i = bisect_right(a, x)
    if i:
        return a[i-1]
    raise ValueError


# compute the redshifts given a list of luminosity distances
def dL_to_redshift(distances, zmin, zmax, N):
    # get the luminosity distance line
    line, fiducial_distances = dL_line(zmin, zmax, N)

    # get the redshift for each luminosity distance
    redshifts = []
    for i in range(0, len(distances)):
        index = np.where( np.isclose(fiducial_distances, find_le(fiducial_distances, distances[i])) )
        redshifts.append( round(float(line[index]), 3) )

    return redshifts
