from typing import Union
from .brew.opener import Opener, LAMMPSOpener, DatOpener, WMIopener

__all__ = ["OpenerType", "NumericType"]

OpenerType = Union[Opener, LAMMPSOpener, DatOpener, WMIopener]
NumericType = Union[float, int]
