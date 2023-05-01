from typing import Union
from .filetype.lmps import lmpsOpener
from .filetype.pdb import pdbOpener
from .filetype.vasp import vaspOpener
from .filetype.xyz import xyzOpener

__all__ = ["OpenerType"]

OpenerType = Union[lmpsOpener, pdbOpener, vaspOpener, xyzOpener]
