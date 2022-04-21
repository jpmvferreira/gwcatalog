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

    # header
    if info:
        print(info + "\n", file=file)
    print("# units: none, Gpc, Gpc\n", file=file)

    # name of variables
    print("redshift,luminosity_distance,error", file=file)

    # sort events by ascending order using the 'sort' terminal utility and print them
    with open("/tmp/gwc-unsorted.csv", "w") as tmpfile:
        for i in range(0, len(redshifts)):
            tmpfile.write(f"{redshifts[i]},{distances[i]},{errors[i]}\n")
    print(os.popen("sort -n /tmp/gwc-unsorted.csv").read(), file=file)
    os.system("rm /tmp/gwc-unsorted.csv")

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
