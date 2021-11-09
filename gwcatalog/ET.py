## ET.py
# all functions related to binary neutron stars (BNSs)
# both the distributions and errors are forecasts for the Einstein Telescope (ET)


# imports
from scipy.integrate import quad
import matplotlib.pyplot as plt
from random import gauss
from math import pi
import numpy as np

# local imports
from .auxiliary import GetRandom
from .cosmology import H, dL


# coalescence rate
# required for the normalized redshift distribution function
def r(z):
    if z < 0 or z > 5:
        return 0
    elif z <= 1:
        return (1+2*z)
    elif 1 < z <= 5:
        return (15 - 3*z)/4

# return the normalized redshift distribution function for the BNS events
# from arXiv:1805.08731, page 13
def dist(dL, H, r, events, zmin, zmax):
    # normalizing constant
    N = events * (quad(lambda Z: (4*pi*r(Z)*(dL(Z, H))**2) / (H(Z)*(1+Z)**3), zmin, zmax)[0])**(-1)

    # define our redshift distribution function
    def f(z):
        if z < zmin or z > zmax:
            return 0
        return (4*pi*N*r(z)*(dL(z, H))**2) / (H(z)*(1+z)**3)

    return f


# errors for the luminosity distance
# from arXiv:1805.08731, page 13
def error(z, dL, H):
    return dL(z, H) * ( (0.1449*z - 0.0118*z**2 + 0.0012*z**3)**2 + (0.05*z)**2 )**(0.5)


# generate BNS(s) events
def generate(events=0):
    # check if number of events was provided
    if events == 0:
        raise Exception("specify the number of BNS events")

    # redshift boundaries
    zmin = 0.07
    zmax = 2

    # get distribution function
    f = dist(dL, H, r, events, zmin, zmax)

    # get maximum to use in rejection method
    max = f(1)*1.05

    # get redshift distribution
    min = 0
    redshifts = GetRandom(f, zmin, zmax, min, max, N=events)

    # get luminosity distances and its error
    distances = [dL(z, H) for z in redshifts]
    errors = [error(z, dL, H) for z in redshifts]

    # use a gaussian to distribute events around the theoretical value with its error as standard deviation
    for i in range(0, events):
        distances[i] = gauss(distances[i], errors[i])

    return redshifts, distances, errors


# plot the BNS redshift distribution
def plot_dist(output=None):
    # redshift boundaries (same as above)
    zmin = 0.07
    zmax = 2
    line = np.linspace(zmin, zmax, 1000)

    # get distribution function with 1000 events
    events = 1000
    print(f"Total number of events considered to plot the distribution = {events}")
    f = dist(dL, H, r, events, zmin, zmax)

    # get distribution value
    distribution = []
    for z in line:
        distribution.append(f(z))

    # print distribution area, should match number of dummie events
    area = np.trapz(distribution, x=line)
    print(f"Area under the distribution curve = {area}")

    # plot and show
    plt.plot(line, distribution)
    plt.xlabel("redshift")
    plt.ylabel("probability distribution function")
    plt.grid()

    # output or show
    if output:
        plt.savefig(output, transparent=True)
    else:
        plt.show()

    return


# plot the error as a function of redshift
def plot_error(output=None):
    # manually set redshift boundaries defined in this script
    zmin = 0.07
    zmax = 2
    line = np.linspace(zmin, zmax, 1000)

    # get errors
    errors = []
    for z in line:
        errors.append(error(z, dL, H))

    # plot and show
    plt.plot(line, errors)
    plt.xlabel("redshift")
    plt.ylabel("error")
    plt.grid()

    # output or show
    if output:
        plt.savefig(output, transparent=True)
    else:
        plt.show()

    return
