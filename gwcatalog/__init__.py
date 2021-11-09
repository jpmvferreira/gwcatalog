# generate catalogs
from gwcatalog.MBHB import generate as MBHB
from gwcatalog.BNS import generate as BNS
from gwcatalog.GWTC import generate as GWTC
from gwcatalog.LIGO import generate as LIGO

# debug catalogs
from gwcatalog.MBHB import plot_dist as MBHB_dist
from gwcatalog.MBHB import plot_error as MBHB_error
from gwcatalog.BNS import plot_dist as BNS_dist
from gwcatalog.BNS import plot_error as BNS_error
from gwcatalog.LIGO import plot_dist as LIGO_dist
from gwcatalog.LIGO import plot_error as LIGO_error

# IO functions to save and load catalogs
from gwcatalog.IO import save, load

# plot catalogs
from gwcatalog.plot import plot

# give access to the underlying cosmology
from gwcatalog.cosmology import H, dL
