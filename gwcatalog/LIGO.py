## LIGO.py
# generate the forecast events for LIGO


# imports
from scipy.interpolate import CubicSpline
from scipy.misc import derivative
import matplotlib.pyplot as plt
from random import gauss
import numpy as np


# local imports
from .auxiliary import dL_to_redshift, GetRandom
from .cosmology import dL, H


# return the luminosity distance distribution
def dLdist():
    # data from figure 2 of arXiv:1901.03321
    # non-normalized luminosity distance probability distribution
    distances = [0.0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.2, 0.21, 0.22, 0.23, 0.24, 0.25, 0.26, 0.27, 0.28, 0.29, 0.3, 0.31, 0.32, 0.33, 0.34, 0.35, 0.36, 0.37, 0.38, 0.39, 0.4, 0.41, 0.42, 0.43, 0.44, 0.45, 0.46, 0.47, 0.48, 0.49, 0.5, 0.51, 0.52, 0.53, 0.54, 0.55, 0.56, 0.57, 0.58, 0.59, 0.6, 0.61, 0.62, 0.63, 0.64, 0.65, 0.66, 0.67, 0.68, 0.69, 0.7, 0.71, 0.72, 0.73, 0.74, 0.75, 0.76, 0.77, 0.78, 0.79, 0.8, 0.81, 0.82, 0.83, 0.84, 0.85, 0.86, 0.87, 0.88, 0.89, 0.9, 0.91, 0.92, 0.93, 0.94, 0.95, 0.96, 0.97, 0.98, 0.99, 1.0]
    probabilities = [0.0, 0.00234, 0.00608, 0.01286, 0.0288, 0.04904, 0.07096, 0.09843, 0.12853, 0.1602, 0.19794, 0.23544, 0.27527, 0.31834, 0.35993, 0.40257, 0.44712, 0.48987, 0.53307, 0.57755, 0.61882, 0.65742, 0.69545, 0.73415, 0.76922, 0.80232, 0.83092, 0.85656, 0.88051, 0.90033, 0.91959, 0.93793, 0.94671, 0.95304, 0.9611, 0.96806, 0.97041, 0.97367, 0.96772, 0.96098, 0.95561, 0.93931, 0.92554, 0.91545, 0.89386, 0.87365, 0.86377, 0.84349, 0.82681, 0.8074, 0.78603, 0.7683, 0.75526, 0.73969, 0.71781, 0.69353, 0.67879, 0.66231, 0.64267, 0.61952, 0.59743, 0.58821, 0.57504, 0.55758, 0.53855, 0.5067, 0.47277, 0.45254, 0.42478, 0.40875, 0.38262, 0.362, 0.33489, 0.31254, 0.29549, 0.2717, 0.24877, 0.22818, 0.20365, 0.18635, 0.17054, 0.15791, 0.14347, 0.1261, 0.11144, 0.09308, 0.07149, 0.05694, 0.04795, 0.04173, 0.0327, 0.02416, 0.01511, 0.00749, 0.00295, 0.0015, 0.0, 0.0, 0.0, 0.0, 0.0]

    # non-normalized probability function
    f = CubicSpline(distances, probabilities)

    # auxiliary variables
    dLmin = min(distances)
    dLmax = max(distances)
    dist_min = min(probabilities)
    dist_max = max(probabilities)
    N = None

    return f, dLmin, dLmax, dist_min, dist_max, N


# return the luminosity distance error (in Gpc!)
def dLerror(dL):
    return 0.5625*dL**2


# return the redshift error
def zerror(z):
    return 0.005*(1+z)


# return the total error for the luminosity distance
# assumed by arXiv:2007.13791
def error(redshift, distance):
    # get the error for the luminosity distance
    distanceerror = dLerror(distance)

    # get the error for the redshift
    redshifterror = zerror(redshift)

    # propagate the redshift error to the luminosity distance
    propagatedredshifterror = derivative(dL, redshift, dx=1e-6, args=(H,)) * redshifterror
    error = (distanceerror**2 + propagatedredshifterror**2)**0.5

    return error


# generate the forecast LIGO events
def generate(events=0, ideal=False):
    # check if number of events was provided
    if events == 0:
        raise Exception("specify the number of forecast LIGO events")

    # get luminosity distances distribution
    distribution = dLdist()

    # get events luminosity distances
    distances = GetRandom(*distribution[:-1], N=events)

    # get redshifts for the events luminosity distance
    # assumes that the highest redshift is 1 and uses 2000 steps in between z = 0 and z = 1
    # although this is certain, it should be a dynamic value...
    redshifts = dL_to_redshift(distances, 0, 1, 2000)

    # get the total error for the luminosity distance
    errors = []
    for i in range(0, len(distances)):
        errors.append(error(redshifts[i], distances[i]))

    # generate new luminosity distances based on the real luminosity distances, with a gaussian error
    if not ideal:
        for i in range(0, len(distances)):
            rnd = -1
            while rnd < 0:
                rnd = gauss(distances[i], errors[i])
            distances[i] = round(rnd, 3)

    return redshifts, distances, errors


# plot the distribution as a function of redshift
def plot_dist(output=None):
    # get luminosity distances distribution
    f, dLmin, dLmax, dist_min, dist_max, N = dLdist()

    # get numerical values
    distances = np.linspace(dLmin, dLmax, 1000)
    probabilities = f(distances)

    # fancy up plot and show
    plt.plot(distances, probabilities)
    plt.gca().axes.yaxis.set_ticklabels([])  # somehow removes ticks without removing grid
    plt.grid()
    plt.xlabel("luminosity distance (Gpc)")
    plt.ylabel("Probability distribution function")

    # output or show
    if output:
        plt.savefig(output, transparent=True)
    else:
        plt.show()

    return


# plot the error as a function of redshift
def plot_error(output=None):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # get luminosity distances distribution
    f, dLmin, dLmax, dist_min, dist_max, N = dLdist()

    # get distance line
    distances = np.linspace(dLmin, dLmax, 1000)

    # get redshift line
    # assumes that the highest redshift is 1 and uses 2000 steps in between z = 0 and z = 1
    # although this is certain, it should be a dynamic value...
    redshifts = dL_to_redshift(distances, 0, 1, 2000)

    # get error for luminosity distance
    dLerrors = [dLerror(i) for i in distances]

    # get the total error for the luminosity distance
    errors = []
    for i in range(0, len(distances)):
        errors.append(error(redshifts[i], distances[i]))

    # plot luminosity distance error
    ax1.plot(distances, dLerrors, label="$\sigma_{d_L}(d_L)$")
    ax1.plot(distances, errors, label="$\sigma(d_L)$")
    ax1.grid()
    ax1.set_xlabel("luminosity distance (Gpc)")
    ax1.set_ylabel("error (Gpc)")
    ax1.legend()

    # get error for redshift
    zerrors = [zerror(i) for i in redshifts]

    # plot redshift error
    ax2.plot(redshifts, zerrors, label="error")
    ax2.grid()
    ax2.set_xlabel("redshift")
    ax2.set_ylabel("error")
    ax2.legend()

    # output or show
    if output:
        plt.savefig(output, transparent=True)
    else:
        plt.show()

    return
