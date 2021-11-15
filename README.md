## About
A Python package and a CLI that generates catalogs of gravitational wave (GW) events from different astrophysical sources, for different observatories.


## Table of contents
- [Installation](#installation)
  - [Dependencies](#dependencies)
  - [Stable version](#stable-version)
  - [Development version](#development-version)
- [Quick start](#quick-start)
  - [Generating a MBHB catalog](#generating-a-mbhb-catalog)
  - [Generating a BNS catalog](#generating-a-bns-catalog)
  - [Plotting catalogs](#plotting-catalogs)
  - [Changing default cosmological model](#changing-default-cosmological-model)
  - [Saving and loading catalogs](#saving-and-loading-catalogs)
  - [Checking underlying distributions](#checking-underlying-distributions)
- [References](#references)
- [Credits](#credits)
- [Contributing](#contributing)
- [Release cycle](#release-cycle)
- [License](#license)


## Installation
To avoid conflicts the usage of virtual environments is recommended.

### Dependencies
This package requires the usage of Python version 3, as well as the following packages:

- [Numpy](https://numpy.org/)
- [Scipy](https://www.scipy.org/)
- [Matplotlib](https://matplotlib.org/)
- [Pandas](https://pandas.pydata.org/)

Dependencies are automatically resolved by `pip`.

### Stable version
A stable version is not yet available, look below on how to install this package.

### Development version
To get the latest commits then you can install this package directly from the development branch:
```console
$ pip install -e git+https://github.com/jpmvferreira/gwcatalog.git@dev#egg=gwcatalog
```

If instead you wish to make changes to the source code, start by cloning the development branch locally followed by an installation in editable mode:
```console
$ git clone -b dev https://github.com/jpmvferreira/gwcatalog
$ pip install -e gwcatalog
```


## Quick start
You can use this program as a standard Python package or as a CLI, where both pack the same features.

This quick start guide will show you how to use both.

### Generating a MBHB catalog
To generate the catalog you must specifiy: either the number of years or the number of events, and the population of black holes binaries (Pop III, Delay, No Delay). The redshift distribution is provided by the mission specification L6A2M5N2 provided in [[2]](#2), with modifications and errors found in [[1]](#1).

For example if you wish to generate 4 years worth of Pop III MBHB events:

```python
redshifts, distances, errors = gwc.MBHB("Pop III", years=4)
```

The CLI equivalent would be:
```console
$ gwc generate MBHB "Pop III" --years 4
```

If instead you would like to get 15 events of population No Delay:

```python
redshifts, distances, errors = gwc.MBHB("No Delay", events=15)
```

And in the CLI:
```console
$ gwc generate MBHB "Pop III" --events 15
```

### Generating a BNS catalog
The distribution used to generate the BNS events is provided by [[3]](#3). For the BNS catalog you only need to specify the number of events. In this example we will generate a catalog with 1000 events:
```python
redshifts, distances, errors = gwc.BNS(events=1000)
```

Or the CLI equivalent:
```console
$ gwc generate BNS --events 1000
```

### Plotting catalogs
If you are inside a Python script, you can plot your catalog with:

```python
gwc.plot(redshifts, distances, errors, "catalog1")
```

Where "catalog1" is the label you want to show in the legends of your plot.

You can actually provide more than one catalog, as long as the number of arguments and the order remains the same. So if you have anoter catalog with variables `redshift2`, `distances2` and `errors2` and you name it "catalog2", you can have them both in the same plot with:
```python
gwc.plot(redshifts, distances, errors, "catalog1", redshifts2, distances2, errors2, "catalog2")
```

This also works in the CLI, given that the catalogs are stored in different files. Assuming that you have `catalog1.csv` and `catalog2.csv` you can plot them both with:
```console
$ gwc plot --input catalog1.csv catalog2.csv
```

If you want to change their labels in the CLI, the equivalent of providing a name in the Python script, you can do so with:
```console
$ gwc plot --input catalog1.csv catalog2.csv --legend "catalog 1" "catalog 2"
```

### Changing default cosmological model
If you want to generate your samples with something other that ΛCDM, which is the default when generating both the MBHB and BNS events, then you can redefine the default hubble function using [monkey patching](https://en.wikipedia.org/wiki/Monkey_patch#Examples):
```python
# your custom Hubble and luminosity distance functions here
def H(z):
  (...)

def dL(z, H):
  (...)

# monkey patch the Hubble and luminosity distance functions
gwc.H = H
gwc.dL = dL
```

Now you can generate a catalog the same as before, however this time it will make use of your Hubble and luminosity distances functions.

In the CLI simply point towards a Python script where both `H(z)` and `dL(z, H)` are defined with `-c`, `--cosmology` flag, followed by the desired subcommand (which is omitted here):
```console
$ gwc --cosmology mycosmology.py (...)
```

This is a global flag, which means it should always be present before any of the available subcommands.

Optionally you may add a variable named `description` in the previous file, that should be a string with a descriptive name of the cosmology being used. That string will be printed in the .csv file provided as output, which you will learn about in the next section. This feature is only available in the CLI.


### Saving and loading catalogs
This package also includes an easy way to save your catalogs to a `.csv` file:
```python
gwc.save(z, dL, error, "sample.csv")
```

Which you can easily import later with:
```python
redshifts, distances, errors = gwc.load("sample.csv")
```

In the CLI you can also provide the output file using the `-o`, `--output` flag, which allows you to save whatever it is that the command returns, if you want to save a MBHB catalog which you just generated:
```console
$ gwc --output MBHB.csv generate MBHB -p "No Delay" -e 15
```

Just the the cosmology flag, the output flag is a global flag, meaning that it should come before any subcommand.

### Checking underlying distributions
To understand what's working in the background, you can plot the redshift distribution for each MBHB population:

```python
gwc.MBHB_dist()
```

Being the CLI equivalent:
```console
$ gwc debug MBHB --distribution
```

And you can also plot the errors for the MBHBs as a function of redshift:

```python
gwc.MBHB_error()
```

With the CLI equivalent:
```console
$ gwc debug MBHB --error
```

Where the same applies for the BNSs, all you have to do is replace MBHB by BNS where appropriate.


## References
<a id="1">[1]</a>
L. Speri, N. Tamanini, R. R. Caldwell, J. R. Gair, and B. Wang, Testing the quasar hubble diagram with lisa standard sirens, Physical Review D **103**, [10.1103/physrevd.103.083526](https://doi.org/10.1103/physrevd.103.083526) (2021).

<a id="2">[2]</a>
C. Caprini and N. Tamanini, Constraining early and interacting dark energy with gravitational wave standard sirens: the potential of the elisa mission, [Journal of Cosmology and Astroparticle Physics2016(10), 006–006](https://doi.org/10.1088/1475-7516/2016/10/006).

<a id="3">[3]</a>
E. Belgacem, Y. Dirian, S. Foffa, and M. Maggiore, Modified gravitational-wave propagation and standard sirens, Physical Review D 98, [10.1103/physrevd.98.023510](https://doi.org/10.1103/physrevd.98.023510) (2018).


## Credits
This was developed by myself. You can contact me in the following ways:
- Personal email: [jose@jpferreira.me](mailto:jose@jpferreira.me) - [[PGP key](https://pastebin.com/REkhQKg2)]
- Institutional email: [joseferreira@alunos.fc.ul.pt](mailto:joseferreira@alunos.fc.ul.pt) - [[PGP key](https://pastebin.com/rfBpi8jc)]


## Contributing
Any discussion, suggestions or bug reports are always welcome. If you wish to contribute, do not hesitate to open up an issue in the issue section of this repository, or even send me an e-mail.


## Release cycle
All versions will have the format X.Y.Z, with the first one being 1.0.0, which will be released as soon as I think both the code and documentation are good enough to be shared.

Each time that there is an update which does not modify the program behavior (e.g.: documentation, packaging) it will increment Z (e.g.: 1.0.0 -> 1.0.1).

Each time that there is an update which modifies the program behavior (e.g.: adding features, fixing bugs) it will increment Y and reset Z (e.g.: 1.0.1 -> 1.1.0).

Each time that there is an update which is not backwards compatible (e.g.: removing features, fundamental change on how the program is used) it will increment X and reset both Y and Z (e.g.: 1.1.2 -> 2.0.0).

In this repository you will find branches for the stable version (master) and the development version (dev). All modifications are done in the development branch and, after being tested, are included in the stable version, with the appropriate version bump.

This means that, were you wish to contribute, pull requests should be targeted towards the dev branch.


## License
[MIT](./LICENSE.md)
