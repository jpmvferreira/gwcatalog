## IO.py
# input/output functions


# imports
import pandas
import sys


# export catalog to file
def save(redshifts, distances, errors, filename, info=""):
    # output to file or stdout
    if filename != sys.stdout:
        file = open(filename, "w")
    else:
        file = filename

    # header
    if info:
        file.write(info + "\n")
    file.write("# units: none, Gpc, Gpc\n")

    # body
    file.write("redshift,luminosity_distance,error\n")
    for i in range(0, len(redshifts)):
        file.write(f"{redshifts[i]},{distances[i]},{errors[i]}\n")

    pass


# import catalog from file
def load(filename):
    with open(filename, "r") as file:
        columns = pandas.read_csv(file, comment="#")
        redshifts = columns["redshift"].tolist()
        distances = columns["luminosity_distance"].tolist()
        errors = columns["error"].tolist()

    return redshifts, distances, errors
