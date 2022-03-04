## plot.py
# catalog plotting functions

# imports
import matplotlib.pyplot as plt

# local imports
from .auxiliary import dL_line


# plot a given mock catalog [redshifts:list, distances:list, errors:list, label:str]
def plot(*args, theoretical=None, output=None):
    # custom colors that match the ones i use in getdist
    colors = ["#006FED", "#E03424", "#008000", "#9c5500", "#9224e0", "#ed00e6", "#f2e400", "#00f2e4", "#6fd95f"]

    # number of catalogs
    N = len(args) // 4

    zmax = 0
    for i in range(0, N):
        redshifts = args[4*i]
        distances = args[4*i + 1]
        errors = args[4*i + 2]
        label = args[4*i + 3]

        # plot the events
        markers, caps, bars = plt.errorbar(redshifts, distances, yerr=errors, fmt=".", markersize=7.5, color=colors[i], ecolor=colors[i], elinewidth=1, capsize=2, label=label, zorder=3.5)

        # loop through bars and caps and set the alpha value
        [bar.set_alpha(0.4) for bar in bars]
        [cap.set_alpha(0.4) for cap in caps]

        # get maximum redshift for fancy plotting
        if max(redshifts) > zmax:
            zmax = max(redshifts)

    # plot luminosity distance theoretical line
    if theoretical:
        line, distances = dL_line(0, zmax*1.05)
        if type(theoretical) == str:
            label = theoretical
        else:
            label = ""
        plt.plot(line, distances, label=label, color="black", zorder=2.5, alpha=0.75)

    # format and show
    plt.xlabel("z")
    plt.ylabel("$d_L$ (Gpc)")
    plt.grid(alpha=0.5, zorder=0.5)
    plt.legend()

    # output or show
    if output:
        plt.savefig(output, transparent=True)
    else:
        plt.show()
