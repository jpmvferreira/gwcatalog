## IO.py
# input/output functions


# imports
import pandas
import sys
import os


# export catalog to file
def save(redshifts, distances, errors, filename, info=""):
    # output to file or stdout
    if filename != sys.stdout:
        file = open(filename, "w")
    else:
        file = filename

    # information header
    if info:
        print(info, file=file)

    # variables and respective units
    print("# units: none, Gpc, Gpc", file=file)
    print("redshift,luminosity_distance,error", file=file)

    # sort events by ascending order, using the 'sort' terminal utility, in a temp file made by 'mktemp'
    filename = os.popen("mktemp --suffix=.csv -t gwc-XXXXXXXXXX").read().replace("\n", "")
    with open(filename, "w") as tmpfile:
        for i in range(0, len(redshifts)):
            tmpfile.write(f"{redshifts[i]},{distances[i]},{errors[i]}\n")
    print(os.popen(f"sort -n {filename}").read(), file=file)
    os.system(f"rm {filename}")

    if filename != sys.stdout:
        file.close()

    pass


# import catalog from file
def load(filename):
    with open(filename, "r") as file:
        columns = pandas.read_csv(file, comment="#")
        redshifts = columns["redshift"].tolist()
        distances = columns["luminosity_distance"].tolist()
        errors = columns["error"].tolist()

    return redshifts, distances, errors
