## auxiliary.py
# auxiliary functions defined for convenience to help in internal tasks


# imports
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
def dL_line(min, max, N=1000):
    # protection against invalid arguments
    if (min < 0 or max < 0) or (max < min):
        raise Exception("Please specify a valid interval for redshifts.")

    # create a "solid line" and compute distances for that line
    line = np.linspace(min, max, N)
    distances = [dL(i, H) for i in line]

    return line, distances


# distribute the events around the most likely value using a gaussian distribution, with protection against negative values
def distribute(distances, errors):
    for i in range(0, len(distances)):
        newdistance = -1
        while newdistance < 0:
            newdistance = gauss(distances[i], errors[i])
        distances[i] = newdistance

    return distances, errors
