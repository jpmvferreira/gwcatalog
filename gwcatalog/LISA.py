## LISA.py
# all functions related to LISA


# imports
from math import pi, sqrt, atan, floor
import matplotlib.pyplot as plt
from random import gauss
import numpy as np

# local imports
from .auxiliary import GetRandom, dL_line
from .cosmology import H, dL


# redshift distribution for the MBHB events for the L6A2M5N2 LISA mission over 5 years duration time
# from arXiv:1607.08755, middle plot of figure 9 in page 21
# modified to include no events at low redshifts (z < 0.1)
def dist(population):
    # redshift limits
    z_min = 0.1
    z_max = 9

    # Pop III
    if population == "Pop III":
        dist = [2.012, 7.002, 8.169, 5.412, 3.300, 1.590, 0.624, 0.141, 0.000]

    # Delay
    elif population == "Delay":
        dist = [0.926, 4.085, 5.976, 5.131, 4.769, 2.656, 1.710, 0.644, 0.362]

    # No Delay
    elif population == "No Delay":
        dist = [3.682, 10.28, 9.316, 7.646, 4.909, 2.817, 1.187, 0.362, 0.161]

    # get total number of events
    N = sum(dist)

    # normalize distribution
    dist = [i/N for i in dist]

    # get minimum and maximum of redshift distribution
    dist_min = min(dist)
    dist_max = max(dist)

    # define our redshift distribution function
    def f(z):
        if z < 0.1 or z >= 9:
            return 0
        return dist[floor(z)]

    return (f, z_min, z_max, dist_min, dist_max, N)


# errors for the luminosity distance
# from arXiv:2010.09049, page 6
def sigma_lens(z, dL, H):
    return 0.066 * ((1-(1+z)**(-0.25))/0.25)**(1.8) * dL(z, H)

def F_delens(z):
    return 1 - 2*0.3/pi * atan(z/0.073)

def sigma_delens(z, dL, H):
    return sigma_lens(z, dL, H) * F_delens(z)

def sigma_v(z, dL, H):
    rms = 1.6203896*10**(-20)   # [Gpc/s]
    c = 9.7156118908*10**(-18)  # speed of light [Gpc/s]
    return ( ( 1 + (c*(1+z)**2)/(H(z)*dL(z, H)) ) * rms/c ) * dL(z, H)

def sigma_LISA(z, dL, H):
    return 0.05 * (dL(z, H)**2)/36.6

def sigma_photo(z, dL, H):
    c = 9.7156118908*10**(-18)  # speed of light [Gpc/s]
    if z < 2:
        return 0
    return (dL(z, H)/(1+z) + c*(1+z)/H(z)) * 0.03*(1+z)

def error(z, dL, H):
    return sqrt(sigma_delens(z, dL, H)**2 + sigma_v(z, dL, H)**2 + sigma_LISA(z, dL, H)**2 + sigma_photo(z, dL, H)**2)


# generate LISA event(s)
def generate(population=None, events=0, years=0):
    # protection against invalid arguments
    if not population:
        raise Exception("The population of MBHB must be provided, available populations are: 'Pop III', 'Delay' and 'No Delay'")
    if population not in ["Pop III", "Delay", "No Delay"]:
        raise Exception("Population not available, available populations are: 'Pop III', 'Delay' and 'No Delay'")
    if events == 0 and years == 0:
        raise Exception("Please specify the number of events or years to generate the mock catalog.")
    if events != 0 and years != 0:
        raise Exception("Both number of events and years were specified, please pick one.")

    # get distribution for the standard sirens
    distribution = dist(population)

    # get number of events
    if events != 0:
        N = events
    elif years != 0:
        N = int(distribution[-1] * years/5)

    # get redshifts and the distance and error for each event
    redshifts = GetRandom(*distribution[:-1], N=N)
    distances = [dL(z, H) for z in redshifts]
    errors = [error(z, dL, H) for z in redshifts]

    # use a gaussian to distribute events around the theoretical line with its error as standard deviation
    for i in range(0, N):
        distances[i] = gauss(distances[i], errors[i])

    return redshifts, distances, errors


# plot all MBHB redshift distributions
# reproduces the middle plot of figure 9, in page 21, from arXiv:1607.08755, with no events in z < 0.1
def plot_dist(output=None):
    populations = ["Pop III", "Delay", "No Delay"]
    colors = ["red", "blue", "green"]

    for population, color in zip(populations, colors):
        f, z_min, z_max, min, max, N = dist(population)

        line = np.linspace(z_min, z_max, 1000).tolist()

        events = [f(i) for i in line]

        print(f"Sum of all events for population {population} in 5 years is {N}")

        plt.plot(line, events, color="dark" + color, zorder=2.5, label=population)
        plt.grid(alpha=0.5, zorder=0.5)
        plt.xticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

        plt.legend()

        plt.ylabel("probability density function")
        plt.xlabel("redshift")

    # output or show
    if output:
        plt.savefig(output, transparent=True)
    else:
        plt.show()

    return


# plot the error as a function of redshift
# reproduces figure 3 from arXiv:2010.09049
def plot_error(output=None):
    # get luminosity distance theoretical line
    line, distances = dL_line(0, 10)

    # start from redshift z = 0.1
    distances = distances[10:]
    line = line[10:]

    # generate lists for all sources of error
    total = []
    photo = []
    LISA = []
    v = []
    lens = []
    delens = []
    for i in line:
        total.append(error(i, dL, H))
        photo.append(sigma_photo(i, dL, H))
        LISA.append(sigma_LISA(i, dL, H))
        v.append(sigma_v(i, dL, H))
        lens.append(sigma_lens(i, dL, H))
        delens.append(sigma_delens(i, dL, H))

    # plot all errors divided by the theoretical luminosity distance
    plt.plot(line, [i/j for i, j in zip(total, distances)], linestyle="dashed", color="black" ,label="$\sigma/d_L$")
    plt.plot(line, [i/j for i, j in zip(photo, distances)], color="green", label="$\sigma_{photo}/d_L$")
    plt.plot(line, [i/j for i, j in zip(LISA, distances)], color="blue", label="$\sigma_{LISA}/d_L$")
    plt.plot(line, [i/j for i, j in zip(v, distances)], color="orange", label="$\sigma_v/d_L$")
    plt.plot(line, [i/j for i, j in zip(lens, distances)], linestyle="dotted", color="red", label="$\sigma_{lens}/d_L$")
    plt.plot(line, [i/j for i, j in zip(delens, distances)], color="red", label="$\sigma_{delens}/d_L$")

    # fancy up the plot
    plt.yticks([0, 0.05, 0.10, 0.15, 0.20])
    plt.xscale("log")
    plt.xlabel("redshift")
    plt.ylabel("error")
    plt.legend()
    plt.grid(alpha=0.5, zorder=0.5)

    # output or show
    if output:
        plt.savefig(output, transparent=True)
    else:
        plt.show()

    return
