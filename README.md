## About
A Python package and a CLI that generates catalogs of standard sirens events, which currently supports the following sources:
- GWTC real data
- LIGO forecasts
- LISA forecasts
- ET forecasts


## Table of contents
- [Installation](#installation)
  - [Dependencies](#dependencies)
  - [Stable version](#stable-version)
  - [Development version](#development-version)
  - [Post installation](#post-installation)
- [Generating Catalogs](#generating-catalogs)
  - [GWTC](#gwtc)
  - [LIGO](#ligo)
  - [LISA](#lisa)
  - [ET](#et)
- [Other Features](#other-features)
  - [Saving and loading catalogs](#saving-and-loading-catalogs)
  - [Plotting catalogs](#plotting-catalogs)
  - [Changing default cosmological model](#changing-default-cosmological-model)
  - [Debug](#debug)
- [Citation](#credits)
- [Feedback](#feedback)
- [Release cycle](#release-cycle)
- [License](#license)
- [References](#references)


## Installation
To avoid conflicts the usage of virtual environments is recommended.

### Dependencies
This program requires Python version 3, as well as the following packages:
- [Numpy](https://numpy.org/)
- [Scipy](https://www.scipy.org/)
- [Matplotlib](https://matplotlib.org/)
- [Pandas](https://pandas.pydata.org/)

Dependencies are automatically resolved by `pip`.

### Stable version
This program can be installed directly from PyPI with:
```console
$ pip install gwcatalog
```

### Development version
If you wish to use this program updated to the latests commits, you can install this package directly from the development branch present in this repository:
```console
$ pip install -e git+https://github.com/jpmvferreira/gwcatalog.git@dev#egg=gwcatalog
```

If instead you wish to make changes to the source code as you are using the program, start by cloning the development branch locally, followed by an installation in editable mode:
```console
$ git clone -b dev https://github.com/jpmvferreira/gwcatalog
$ pip install -e gwcatalog
```

### Post installation
You can either use this program as a Python package or as a CLI.

To ensure that the Python package is operational, import it as:
```python
import gwcatalog as gwc
```

To ensure that the terminal version is working, call the program `gwc` with the help flag:
```console
# gwc --help
```


## Generating Catalogs
In this section we will show you how you can use this program to generate catalogs of standard siren events, both in Python and in the CLI.

### GWTC
The Gravitational Wave Transient Catalog (GWTC) is a cumulative set of gravitational wave transients maintained by the LIGO/Virgo/KAGRA collaboration, available online at [gw-openscience.org](https://www.gw-openscience.org/eventapi/html/GWTC/).

Here we provide the data found in GWTC-1, GWTC-2 and GWTC-3, with the redshifts, luminosity distances and errors coming directly from the previously mentioned database, symmetrizing both the redshift and luminosity distance error and then propagate the redshift error to the luminosity distance.

These are not necessarily standard siren events, however they can be used for testing purposes.

To obtain that data simply call the function with no arguments:
```python
redshifts, distances, errors = gwc.GWTC()
```

And in the CLI:
```console
$ gwc generate GWTC
```


### LIGO
Although currently operational, here we will focus our efforts on generating forecast events for the Laser Interferometer Gravitational-Wave Observatory (LIGO).

The redshift distribution is given in [[4]](#4), while the error for each measurement is provided in [[5]](#5).

To generate a mock catalog for LIGO all you need is to specify the number of events.

If, for example, you wish to generate a mock catalog consisting of 50 events:
```python
redshifts, distances, errors = gwc.LIGO(events=50)
```

Being the CLI equivalent:
```console
$ gwc generate LIGO --events 50
```

Instead of specifying the events, you can also provide a list of redshifts which you would like your catalog to have. Naturally, this will ignore the underlying redshift distribution. To create a catalog with user specified redshifts:
```python
redshifts, distances, errors = gwc.LIGO(redshifts=[0.1, 0.125, 0.15, 0.175])
```

And in the CLI:
```console
$ gwc generate LIGO --redshifts '[0.1, 0.125, 0.15, 0.175]'
```

There is also an added option to generate an ideal catalog, i.e. a catalog where all events lay on top of the theoretical line for the luminosity distance:
```python
redshifts, distances, errors = gwc.LIGO(events=50, ideal=True)
```

Or in the CLI:
```console
$ gwc generate LIGO --events 50 --ideal
```


### LISA
In this subsection we will generate standard sirens mock catalogs for the Laser Interferometer Space Antenna (LISA).

The redshift distribution is provided in [[2]](#2), which corresponds to the mission specification L6A2M5N2, with modifications and errors as outlined in [[1]](#1).

To generate the LISA mock catalog you must specify two things: A population of massive black hole binaries (MBHB), either "Pop III", "Delay" or "No Delay", and specify either mission lifetime in years or the number of observed events.

For example if you wish to generate the result of a 4 year mission lifetime of population "Pop III" events:
```python
redshifts, distances, errors = gwc.LISA(population="Pop III", years=4)
```

The CLI equivalent would be:
```console
$ gwc generate LISA --population "Pop III" --years 4
```

If instead you would like to generate 15 events of the population "No Delay":
```python
redshifts, distances, errors = gwc.LISA(population="No Delay", events=15)
```

Or in the CLI:
```console
$ gwc generate LISA --population "No Delay" --events 15
```

You can also ignore the underlying redshift distribution and specify the redshift for all events:
```python
redshifts, distances, errors = gwc.LISA(population="No Delay", redshifts=[1, 2, 3, 4, 5, 6, 7, 8])
```

Or in the CLI:
```console
$ gwc generate LISA --population "No Delay" --redshifts '[1, 2, 3, 4, 5, 6, 7, 8, 9]'
```

You also have the option to generate an ideal catalog, where all events lay on top of the theoretical luminosity distance:
```python
redshifts, distances, errors = gwc.LISA(population="No Delay", events=15, ideal=True)
```

Or in the CLI:
```console
$ gwc generate LISA --population "No Delay" --events 15 --ideal
```


### ET
Here we will show how to generate a mock catalog for the Einstein Telescope (ET).

Both the redshift distribution and error distribution used to generate the mock catalogs are provided in [[3]](#3).

To generate a mock catalog for the ET the only requirement is to provide the number of events you wish to have in your catalog.

For example, if you wish to generate a mock catalog with 1000 events:
```python
redshifts, distances, errors = gwc.ET(events=1000)
```

Being the CLI equivalent:
```console
$ gwc generate ET --events 1000
```

You can also decide to specify the redshift for each event:
```python
redshifts, distances, errors = gwc.ET(redshifts=[0.5, 1, 1.5])
```

Where in the CLI you have:
```console
$ gwc generate ET --redshifts '[0.5, 1, 1.5]'
```

And you can also have an ideal catalog, where the events lay on top of the theoretical line for the luminosity distance:
```python
redshifts, distances, errors = gwc.ET(events=1000, ideal=True)
```

Which in the CLI is:
```console
$ gwc generate ET --events 1000 --ideal
```


## Other Features
Here we list other features which are available in this package, developed in order to facilitate common operations.


### Saving and loading catalogs
This package also includes an easy way to save your catalogs to a `.csv` file:
```python
gwc.save(redshifts, distances, errors, "catalog.csv")
```

Which you can easily import later with:
```python
redshifts, distances, errors = gwc.load("catalog.csv")
```

In the CLI you can also provide the output file using the `-o`, `--output` flag, which allows you to save whatever it is that the command returns, if you want to save a LISA mock catalog:
```console
$ gwc --output catalog.csv generate LISA --population "No Delay" --events 15
```

The output flag is a global flag, meaning that it should come before any subcommand.


### Plotting catalogs
If you are inside a Python script, you can plot your catalog, along with its label, which in this case is "catalog1", with:
```python
gwc.plot(redshifts, distances, errors, "catalog1")
```

The CLI equivalent, where the data is stored in `catalog1.csv`:
```console
$ gwc plot --input catalog1.csv --legend "catalog 1"
```

You can provide more than one catalog, as long as the number of arguments and the order remains the same. So if you have another catalog with variables `redshift2`, `distances2` and `errors2`, and you would like to label it as "catalog2", you can have them both in the same plot with:
```python
gwc.plot(redshifts, distances, errors, "catalog1", redshifts2, distances2, errors2, "catalog2")
```

Being the CLI equivalent, where both catalog are stored as files:
```console
$ gwc plot --input catalog1.csv catalog2.csv --legend "catalog 1" "catalog 2"
```

You can also plot the theoretical line of the default cosmological model, with a custom label that supports LaTeX (e.g.: "$\LambdaCDM$"):
```python
gwc.plot(redshifts, distances, errors, "catalog1", theoretical="$\LambdaCDM$")
```

And in the CLI
```console
$ gwc plot --input catalog1.csv --legend "catalog 1" --theoretical "$\LambdaCDM$"
```


### Changing default cosmological model
Allows you to use a custom cosmological model when generating your samples.

This feature is only available in the CLI.

To do so, write a Python script that defines two functions, both `H(z)` and `dL(z, H)`, and then using the `-c`, `--cosmology` flag, point it towards the previously mentioned Python script.

For example, if you wish to use a custom cosmology, defined in `mycosmology.py`, to generate 1000 events for ET:
```console
$ gwc --cosmology mycosmology.py generate ET --events 1000
```

This is a global flag, which means it should always be present before any of the available subcommands.

Optionally, you may add a variable named `description` to the previous file, that should be a string with a descriptive name of the cosmological model being used, which will be printed in the header of the generated catalogs and kept for future reference.


### Debug
For the sake of transparency, ease of use to check the underlying distributions is provided to the end user.

For LISA, you can plot the probability redshift distribution with:
```python
gwc.LISA_dist()
```

Being the CLI equivalent:
```console
$ gwc debug LISA --distribution
```

And the error as a function of redshift with:
```python
gwc.LISA_error()
```

With the CLI equivalent:
```console
$ gwc debug LISA --error
```

The same pattern applies for the ET and LIGO, where all you have to do is replace LISA by ET or LIGO, according to your wish, where appropriate.

Because GWTC includes real data there is no underlying distribution, only the data pulled directly from the GWTC catalog source.


## Citation
This program was developed in the context of [arXiv:2203.13788](https://arxiv.org/abs/2203.13788). Although it is completely independent from it, if you used any of the contents available in this repository, or found it useful in any way, you can cite it using the following BibTeX entry:
```
@misc{Ferreira2022,
  doi = {10.48550/ARXIV.2203.13788},
  url = {https://arxiv.org/abs/2203.13788},
  author = {Ferreira, Jos\'e and Barreiro, Tiago and Mimoso, Jos\'e and Nunes, Nelson J.},
  title = {Forecasting F(Q) cosmology with $\Lambda$CDM background using standard sirens},
  publisher = {arXiv},
  year = {2022},
}
```


## Feedback
Any discussion, suggestions, pull requests or bug reports are always welcome. Feel free to use this issue section in this repository for everything else, or even send me an email at:
- Personal email: [jose@jpferreira.me](mailto:jose@jpferreira.me) - [[PGP key](https://pastebin.com/raw/REkhQKg2)]
- Institutional email: [jpmferreira@fc.ul.pt](mailto:jpmferreira@fc.ul.pt) - [[PGP key](https://pastebin.com/raw/AK2trPBw)]

If you wish to submit you code, pull requests should be targeted towards the dev branch.


## Release cycle
All versions will have the format X.Y.Z, with the first one being 1.0.0, which will be released as soon as I think that both the code and the documentation are good enough to be shared.

Each time that there is an update which does not modify the program behavior (e.g.: documentation, packaging) it will increment Z (e.g.: 1.0.0 -> 1.0.1).

Each time that there is an update which modifies the program behavior (e.g.: adding features, fixing bugs) it will increment Y and reset Z (e.g.: 1.0.1 -> 1.1.0).

Each time that there is an update which is not backwards compatible (e.g.: removing features, fundamental change on how the program is used) it will increment X and reset both Y and Z (e.g.: 1.1.2 -> 2.0.0).

In this repository you will find two branches: the stable branch (master) and the development branch (dev). All modifications are done in the development branch and, after being properly tested, are merged in the stable branch, with the appropriate version bump.


## License
All of the contents provided in this repository are available under the MIT license.

For further information, refer to the file [LICENSE.md](./LICENSE.md) provided in this repository.


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
