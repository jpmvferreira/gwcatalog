## ET.py
# all functions related to generating forecast catalogs for the ET (Einstein Telescope)


# imports
from scipy.integrate import quad
import matplotlib.pyplot as plt
from scipy.optimize import fmin
from math import pi
import numpy as np

# local imports
from .auxiliary import GetRandom, distribute
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
def dist(dL, H, r):
    # redshift boundaries for the ET
    zmin = 0.07
    zmax = 2

    # normalizing constant
    N = (quad(lambda Z: (4*pi*r(Z)*(dL(Z, H))**2) / (H(Z)*(1+Z)**3), zmin, zmax)[0])**(-1)

    # redshift distribution function
    def f(z):
        if z < zmin or z > zmax:
            return 0
        return (4*pi*N*r(z)*(dL(z, H))**2) / (H(z)*(1+z)**3)

    # get the minimum and the maximum of the distribution
    dmax = fmin(lambda Z: -f(Z), 1.5, disp=False)[0]*1.05
    dmin = 0

    return (f, zmin, zmax, dmin, dmax)


# errors for the luminosity distance
# from arXiv:1805.08731, page 13
def error(z, dL, H):
    return dL(z, H) * ( (0.1449*z - 0.0118*z**2 + 0.0012*z**3)**2 + (0.05*z)**2 )**(0.5)


# generate the forecast ET events
def generate(events=0, redshifts=[], ideal=False):
    # specify either events or redshifts
    if bool(events) + bool(redshifts) != 1:
        raise Exception("Specify either the number of events or their redshifts")

    # get redshift distribution function
    f, zmin, zmax, dmin, dmax = dist(dL, H, r)

    # get luminosity distance and error for specific redshifts
    if redshifts:
        # protect against out of bound redshifts
        if min(redshifts) < zmin or max(redshifts) > zmax:
            raise Exception(f"Redshift limits are out of bounds. Lowest and highest redshift for the ET are z={zmin} and z={zmax} correspondingly")

        distances = [dL(z, H) for z in redshifts]
        errors = [error(z, dL, H) for z in redshifts]

    # generate events according to the redshift distribution
    else:
        # get the redshifts for the events
        redshifts = GetRandom(f, zmin, zmax, dmin, dmax, N=events)

        # get luminosity distance and the error for each event
        distances = [dL(z, H) for z in redshifts]
        errors = [error(z, dL, H) for z in redshifts]

    # distribute the events around the most likely value using a gaussian distribution
    if not ideal:
        distances, errors = distribute(distances, errors)

    return redshifts, distances, errors


# plot the BNS redshift distribution
def plot_dist(output=None):
    # redshift boundaries (same as above)
    zmin = 0.07
    zmax = 2
    line = np.linspace(zmin, zmax, 1000)

    # get redshift distribution
    f, zmin, zmax, dmin, dmax = dist(dL, H, r)

    # obtain distribution considering N = 1000 event normalization
    events = 1000
    distribution = []
    for z in line:
        distribution.append(events*f(z))

    # print distribution area, should match number of dummie events
    print(f"Total number of events considered to plot the distribution = {events}")
    area = np.trapz(distribution, x=line)
    print(f"Area under the distribution curve = {area}")

    # plot and show
    plt.title("Replicating figure 8 from arXiv:1805.08731")
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
    # get redshift boundaries
    f, zmin, zmax, dmin, dmax = dist(dL, H, r)

    # draw a line
    line = np.linspace(zmin, zmax, 1000)

    # get errors
    errors = [error(z, dL, H) for z in line]

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
