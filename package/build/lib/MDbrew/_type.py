from typing import Union
from .brew.opener import Opener, LAMMPSOpener, DatOpener

__all__ = ["OpenerType", "NumericType"]

OpenerType = Union[Opener, LAMMPSOpener, DatOpener]
NumericType = Union[float, int]
