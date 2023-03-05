from typing import Union
from .opener import *

__all__ = ["OpenerType"]

OpenerType = Union[LAMMPSOpener, DATOpener, WMIOpener]
