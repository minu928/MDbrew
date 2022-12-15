from typing import Union
from .brew.opener import Opener, LAMMPSOpener, GromacsOpener

OpenerType = Union[Opener, LAMMPSOpener, GromacsOpener]
