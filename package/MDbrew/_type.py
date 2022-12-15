from typing import Union
from .brew.opener import Opener, LAMMPSOpener, GromacsOpener

__all__ = ["OpenerType"]

OpenerType = Union[Opener, LAMMPSOpener, GromacsOpener]
