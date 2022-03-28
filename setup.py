from setuptools import setup

with open(f"README.md") as f:
    long_description = f.read()

setup(name="gwcatalog",
      version="1.2.0",
      scripts=["bin/gwc"],
      packages=["gwcatalog"],
      description="Generate catalogs of standard siren events.",
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
      zip_safe=False)
