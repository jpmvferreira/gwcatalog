## About
A Python package and a CLI that generates catalogs of gravitational wave (GW) events from different astrophysical sources, for different observatories.

Currently generates standard siren mock catalogs for LISA, ET and LIGO. It also gives you access to the (real) events from the GWTC catalog, where the luminosity distance is obtained directly from the gravitational wave and the redshift estimated using ΛCDM by the LIGO/VIRGO/KAGRA collaboration, with symmetric errors.

It also provides ease of access to check the underlying redshift and error distributions, used to generate the mock catalogs.


## Table of contents
- [Installation](#installation)
  - [Dependencies](#dependencies)
  - [Stable version](#stable-version)
  - [Development version](#development-version)
- [Quick start](#quick-start)
  - [LISA mock catalog](#lisa-mock-catalog)
  - [ET mock catalog](#et-mock-catalog)
  - [LIGO mock catalog](#ligo-mock-catalog)
  - [GWTC](#gwtc)
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
You can either use this program as a Python package or as a CLI, where both provide access to the same features. This quick start guide will also show you how to use both.

### LISA mock catalog
The MBHB redshift distribution is provided by the mission specification L6A2M5N2 provided in [[2]](#2), with modifications and errors found in [[1]](#1).

To generate the LISA mock catalog you must select a population of MBHB, either "Pop III", "Delay" or "No Delay", and specify either the number of years or events to generate the catalog.

For example if you wish to generate 4 years worth of Pop III MBHB events measured by LISA:
```python
redshifts, distances, errors = gwc.LISA("Pop III", years=4)
```

The CLI equivalent would be:
```console
$ gwc generate LISA "Pop III" --years 4
```

If instead you would like to generate 15 events of the population No Delay:
```python
redshifts, distances, errors = gwc.LISA("No Delay", events=15)
```

And in the CLI:
```console
$ gwc generate LISA "Pop III" --events 15
```

### ET mock catalog
The BNS redshift and error distribution used to generate the ET mock catalog are provided in [[3]](#3).

In this example we will generate a mock catalog with 1000 events:
```python
redshifts, distances, errors = gwc.ET(events=1000)
```

Being the CLI equivalent:
```console
$ gwc generate ET --events 1000
```

### LIGO mock catalog
The redshift distribution of the LIGO forecats events are given in [[4]](#4), while the error is provided in [[5]](#5).

To generate a mock catalog for LIGO all you need is to specify the number of events, in this case 50:
```python
redshifts, distances, errors = gwc.LIGO(events=50)
```

Being the CLI equivalent:
```console
$ gwc generate LIGO --events 50
```

There is also an added option to generate an ideal catalog, i.e. a catalog where all events lay on top of the theoretical line for the luminosity distance:
```python
redshifts, distances, errors = gwc.LIGO(events=50, ideal=True)
```

And in the CLI:
```console
$ gwc generate LIGO --events 50 --ideal
```


### GWTC
The GWTC (Gravitational Wave Transient Catalog) is a cumulative set of gravitational wave transients maintained by the LIGO/Virgo/KAGRA collaboration, available online at [gw-openscience.org](https://www.gw-openscience.org/eventapi/html/GWTC/).

Here we provide the data found in GWTC-1, GWTC-2 and GWTC-3, where the redshifts, luminosity distances and errors come directly from the database. The error in both redshift and luminosity distance is made symmetric, and the redshift error propagated to the luminosity distance.

To obtain that data simply call the function with no arguments, as the number of events are the ones observed so far by the provided observatories:
```python
redshifts, distances, errors = gwc.GWTC()
```

And in the CLI:
```console
$ gwc generate GWTC
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
This feature is only available in the CLI, to do so, simply point towards a Python script where both `H(z)` and `dL(z, H)` are defined with `-c`, `--cosmology` flag, followed by the desired subcommand (which is omitted here):
```console
$ gwc --cosmology mycosmology.py (...)
```

This is a global flag, which means it should always be present before any of the available subcommands.

Optionally you may add a variable named `description` in the previous file, that should be a string with a descriptive name of the cosmology being used. That string will be printed in the .csv file provided as output, which you will learn about in the next section. This feature is only available in the CLI.

Here's an example for such a script, for ΛCDM, with custom fiducial values:
```python
# imports
from scipy.integrate import quad


# Hubble function
def H(z):
    # Hubble constant
    H0 = 70
    H0 = H0*3.240779289*10**(-20)

    # value for Ωm
    Ωm = 0.3087

    return H0*(Ωm*(1+z)**3 + 1-Ωm)**0.5


# luminosity distance
def dL(z, H):
    c = 9.715611890800001e-18  # speed of light [Gpc/s]
    return (1+z) * c * quad(lambda Z: 1/H(Z), 0, z)[0]


# description
description = "ΛCDM (Ωm = 0.3087, H0 = 67.64 km s⁻¹ Mpc⁻¹)"
```


### Saving and loading catalogs
This package also includes an easy way to save your catalogs to a `.csv` file:
```python
gwc.save(z, dL, error, "sample.csv")
```

Which you can easily import later with:
```python
redshifts, distances, errors = gwc.load("sample.csv")
```

In the CLI you can also provide the output file using the `-o`, `--output` flag, which allows you to save whatever it is that the command returns, if you want to save a LISA mock catalog:
```console
$ gwc --output LISA.csv generate LISA -p "No Delay" -e 15
```

Just the the cosmology flag, the output flag is a global flag, meaning that it should come before any subcommand. The file also provides some comments, which provide information on how the catalog was generated.

### Checking underlying distributions
To understand what's working in the background, you can plot the redshift distribution for each MBHB population:

```python
gwc.MBHB_dist()
```

Being the CLI equivalent:
```console
$ gwc debug LISA --distribution
```

And you can also plot the errors for the MBHBs as a function of redshift:

```python
gwc.MBHB_error()
```

With the CLI equivalent:
```console
$ gwc debug LISA --error
```

Where the same applies for ET and LIGO, all you have to do is replace LISA by ET or LIGO where appropriate. Because GWTC includes real data there is no underlying distribution.


## References
<a id="1">[1]</a>
L. Speri, N. Tamanini, R. R. Caldwell, J. R. Gair, and B. Wang, Testing the quasar hubble diagram with lisa standard sirens, Physical Review D **103**, [10.1103/physrevd.103.083526](https://doi.org/10.1103/physrevd.103.083526) (2021).

<a id="2">[2]</a>
C. Caprini and N. Tamanini, Constraining early and interacting dark energy with gravitational wave standard sirens: the potential of the elisa mission, [Journal of Cosmology and Astroparticle Physics2016(10), 006–006](https://doi.org/10.1088/1475-7516/2016/10/006).

<a id="3">[3]</a>
E. Belgacem, Y. Dirian, S. Foffa, and M. Maggiore, Modified gravitational-wave propagation and standard sirens, Physical Review D 98, [10.1103/physrevd.98.023510](https://doi.org/10.1103/physrevd.98.023510) (2018).

<a id="4">[4]</a>
M. Lagos, M. Fishbach, P. Landry, and D. E. Holz, Standard sirens with a running planck mass, Physical Review D 99, [10.1103/physrevd.99.083504](https://doi.org/10.1103/physrevd.99.083504) (2019).

<a id="5">[5]</a>
T. Baker and I. Harrison, Constraining scalar-tensor modified gravity with gravitational waves and large scale structure surveys, [Journal of Cosmology and Astroparticle Physics 2021 (01), 068–068](https://doi.org/10.1088/1475-7516/2021/01/068).


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
