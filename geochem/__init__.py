#geochem/__init__.py
"""
GeoChemistry

----
Note: To use this package in a different directory, if you did not set PYTHONPATH, then add:
  import sys
  sys.path.append('/path-to-module/geochem') #add the directory where this module is located

"""
__version__ = '0.5.0'
__author__  = 'Jose Luis Palma, jose@udec.cl'

from .parameters import getnames_all, getnames_major, getnames_REE, getnames_trace

from .utils import closure, calculate_FeOT
from .preproc import preproc, preproc_calculate_feot, preproc_make_numeric_columns, preproc_strip_whitespace

# Specific functions that could run directly from the root package
#from .plt.tas import TAS

__all__ = [
    # Metadata
    '__version__', '__author__',
    # Submodules
    'plt', 'coda',
    # from parameters
    'getnames_all', 'getnames_major', 'getnames_REE', 'getnames_trace',
    # from utils
    'closure', 'calculate_FeOT',
    # from preproc
    'preproc', 'preproc_calculate_feot', 'preproc_make_numeric_columns', 'preproc_strip_whitespace',
]

