## SNIa.py
# all functions related to generating mock catalogs of SNIa


# imports
from math import floor, log, sqrt
import matplotlib.pyplot as plt
from random import gauss
import numpy as np

# local imports
from .auxiliary import GetRandom, dL_line, distribute
from .cosmology import H, dL


# redshift distribution of SNIa events measured by lSST DDF
# taken from figure 12 of arXiv:1409.8562
def dist():
    # redshift bounds
    zmin = 0.1
    zmax = 1

    # redshift probability distribution
    dist = [64, 258, 480, 758, 1049, 1369, 1683, 2009, 1130]

    # probability distribution bounds
    dmin = 0
    dmax = max(dist)

    # number of expected events (for 2 years worth of observation)
    N = sum(dist)

    # define the redshift probability distribution function
    def f(z):
        if z < zmin or z >= zmax:
            return 0
        return dist[floor(z*10)-1]

    return (f, zmin, zmax, dmin, dmax, N)


# return the error for the luminosity distance
def error(z, dL, H):
    # get the error in μ at redshift z
    # eq (A.1) of arXiv:2007.14335
    muerror = sqrt((gauss(0, 0.01)*z)**2 + 0.01**2 + 0.025**2 + 0.12**2)

    # propagate the error to the luminosity distance
    dLerror = (log(10)/5) * dL(z, H) * muerror

    return dLerror


# generate SNIa mock catalogs
def generate(events=0, redshifts=[], ideal=False):
    # specify either events or redshifts
    if bool(events) + bool(redshifts) != 1:
        raise Exception("Specify either the number of events or redshifts")

    # get the redshift distribution function, minimums/maximums and number of events for that distribution
    f, zmin, zmax, dmin, dmax, N = dist()

    # get luminosity distance and error for specific redshifts
    if redshifts:
        # protect against out of bound redshifts
        if min(redshifts) < zmin or max(redshifts) > zmax:
            raise Exception(f"Redshift limits are out of bounds. Lowest and highest redshift are z={zmin} and z={zmax} correspondingly")

        distances = [dL(z, H) for z in redshifts]
        errors = [error(z, dL, H) for z in redshifts]

    # generate events according to the redshift distribution
    else:
        N = events

        # get redshifts and the distance and error for each event
        redshifts = GetRandom(f, zmin, zmax, dmin, dmax, N=N)
        distances = [dL(z, H) for z in redshifts]
        errors = [error(z, dL, H) for z in redshifts]

    # distribute the events around the most likely value using a gaussian distribution
    if not ideal:
        distances, errors = distribute(distances, errors)

    return redshifts, distances, errors

# reproduces underlying SNIa redshift distribution
# replicates the line corresponding to LSST DDF in fig. 12 from arXiv:1409.8562
def plot_dist(output=None):
    # get distribution
    f, zmin, zmax, dmin, dmax, N = dist()

    # get values
    line = np.linspace(zmin, zmax, num=1000)
    value = [f(i) for i in line]

    # plot and customize
    plt.plot(line, value, label="LSST DDF")
    plt.title("LSST DDF in fig. 12 from arXiv:1409.8562")
    plt.grid(alpha=0.5, zorder=0.5)
    plt.legend()
    plt.ylabel("probability density function")
    plt.xlabel("redshift")

    # output or show
    if output:
        plt.savefig(output, transparent=True)
    else:
        plt.show()

    return


# shows a mock catalog of SNIa in μ vs z plane
# replicates (disregarding statistical fluctuations) fig. 11 of arXiv:2007.14335

# !! ESTA AQUI ALGUM ERRO PORQUE OS LIMITES NAO SAO OS MESMOS !!
def plot_example(output=None):
    # get distribution
    f, zmin, zmax, dmin, dmax, N = dist()

    # generate catalog in μ
    redshifts = GetRandom(f, zmin, zmax, dmin, dmax, N=N)
    mus = [5*log(dL(z, H), 10) + 40 for z in redshifts]
    muerrors = [sqrt((gauss(0, 0.01)*z)**2 + 0.01**2 + 0.025**2 + 0.12**2) for z in redshifts]

    # distribute the errors around the most likely value using a gaussian distribution
    mus = [gauss(i, j) for i, j in zip(mus, muerrors)]

    # theoretical line
    redshift_theoretical = np.linspace(0.1, 1, num=250)
    mu_theoretical = [5*log(dL(i, H), 10) + 40 for i in redshift_theoretical]

    # plot and show
    plt.plot(redshift_theoretical, mu_theoretical, color="grey", zorder=3.5)
    plt.title("replicates (disregarding statistical fluctuations) fig. 11 of arXiv:2007.14335", fontsize=10)
    plt.errorbar(redshifts, mus, yerr=muerrors, color="blue", fmt='.', ecolor="lightblue", elinewidth=1, capsize=0, markersize=1)
    plt.xlim([0.1, 1])
    plt.grid(alpha=0.5)
    plt.xlabel("$z$")
    plt.ylabel("$\mu(z)$")
    plt.show()

    return
