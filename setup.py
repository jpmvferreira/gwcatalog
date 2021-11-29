from setuptools import setup

with open(f"README.md") as f:
    long_description = f.read()

setup(name="gwcatalog",
      version="0.0.0",
      description="A Python package and a CLI that generates catalogs of gravitational wave (GW) events from different astrophysical sources, for different observatories.",
      long_description=long_description,
      long_description_content_type="text/markdown",
      install_requires=[
        "numpy",
        "scipy",
        "matplotlib",
        "pandas",
      ],
      url="https://github.com/jpmvferreira/gwcatalog",
      author="José Ferreira",
      author_email="jose@jpferreira.me",
      license="MIT",
      scripts=["bin/gwc"],
      zip_safe=False)
