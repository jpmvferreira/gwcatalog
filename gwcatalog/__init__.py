# generate catalogs
from gwcatalog.LISA import generate as LISA
from gwcatalog.ET import generate as ET
from gwcatalog.GWTC import generate as GWTC
from gwcatalog.LIGO import generate as LIGO

# debug catalogs
from gwcatalog.LISA import plot_dist as LISA_dist
from gwcatalog.LISA import plot_error as LISA_error
from gwcatalog.ET import plot_dist as ET_dist
from gwcatalog.ET import plot_error as ET_error
from gwcatalog.LIGO import plot_dist as LIGO_dist
from gwcatalog.LIGO import plot_error as LIGO_error

# IO functions to save and load catalogs
from gwcatalog.IO import save, load

# plot catalogs
from gwcatalog.plot import plot

# give access to the underlying cosmology
from gwcatalog.cosmology import H, dL

# version
__version__ = "0.0.0"
