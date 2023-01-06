from typing import Union
from .brew.opener import Opener, LAMMPSOpener, GromacsOpener

__all__ = ["OpenerType", "NumericType"]

OpenerType = Union[Opener, LAMMPSOpener, GromacsOpener]
NumericType = Union[float, int]