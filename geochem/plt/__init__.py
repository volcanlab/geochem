"""
geochem/plt/__init__.py

Geochemical diagrams with Matplotlib
"""

from .tas import tas_diagram, TAS
from .trivar import convert_abc_to_xy, triangle, tridata, AFM, triangle_lineplot
from .spider import spider, spider_norm, spiderplot
from .scatter import scatter
from .harker import harker

#Import common utilities from the main path
from ..utils import closure, calculate_FeOT
from ..preproc import preproc 
from ..parameters import getnames_all, getnames_major, getnames_REE, getnames_trace

#To restric functions imported with *
#__all__ = []

