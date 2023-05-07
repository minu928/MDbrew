import os
import numpy as np
import pandas as pd
from .opener import Opener
from .filetype.lmps import lmpsOpener
from .filetype.pdb import pdbOpener
from .filetype.vasp import vaspOpener
from .filetype.xyz import xyzOpener
from .filetype.trr import trrOpener
from ..tool.colorfont import color
from ..tool.decorator import color_print_verbose


class Brewery(object):
    __support_opener__: dict["str":Opener] = {
        "auto": None,
        "pdb": pdbOpener,
        "xyz": xyzOpener,
        "vasp": vaspOpener,
        "lmps": lmpsOpener,
        "trr": trrOpener,
    }
    __print_option__ = {
        "brewery": f" #OPEN  {color.font_yellow}Brewery {color.reset}",
        "b_brewing": f" #BREW  {color.font_yellow}Some...  {color.reset}",
        "b_coords": f" #BREW  {color.font_yellow}Coords     {color.reset}",
        "b_atominfo": f" #BREW  {color.font_yellow}Atom Info  {color.reset}",
    }

    def __init__(self, trj_file: str, fmt: str = "auto", *args, **kwrgs):
        self._what = kwrgs.pop("what", None)
        self._path = self._check_path(path=trj_file, **kwrgs)
        self._fmt = self._check_fmt(fmt=fmt)
        self._opener = self._init_opener(**kwrgs)
        self._set_atom_info(verbose=kwrgs.pop("verbose", True))
        self._data = None
        self._coords = None

    def __str__(self) -> str:
        LINE_WIDTH = 60
        sep_line = "=" * LINE_WIDTH
        print("")
        print(sep_line)
        print("||" + " " * 23 + " INFO " + " " * 27 + "||")
        print(sep_line)
        print(f"\t[  ATOM  ]:  KIND  ->   {tuple(self.atom_kind)}")
        print(f"\t[  ATOM  ]:  NUMB  ->   {tuple(self.atom_info[-1])}")
        print(f"\t[   BOX  ]:  SHAPE ->   {np.array(self.box_size).shape}")
        print(f"\t[ COORDS ]:  SHAPE ->   {self.coords.shape}")
        print(f"\t[ FRAMES ]:   NOW  ->   {self.frame:4d}")
        print(sep_line)
        return f"\t    @CopyRight by  {color.font_blue}minu928@snu.ac.kr{color.reset}\n"

    @property
    def box_size(self):
        return self._opener.box_size

    @box_size.setter
    def box_size(self, box_size):
        self._opener.box_size = box_size

    @property
    def columns(self):
        return self._opener.column

    @columns.setter
    def columns(self, colums):
        self._opener.column = colums

    @property
    def coords(self):
        return self.brew(cols=["x", "y", "z"], verbose=False)

    @property
    def data(self):
        return self._opener.data

    @property
    def frame(self):
        return self._opener.frame

    @property
    def next_frame(self):
        self._opener.next_frame()

    @color_print_verbose(name=__print_option__["b_brewing"])
    def brew(self, cols: list[str], what: str = None, dtype: str = "float32", verbose: bool = True):
        data = pd.DataFrame(data=self.data, columns=self.columns)
        data = data.query(self._what) if self._what is not None else data
        data = data.query(what) if what is not None else data
        data = data.loc[:, cols] if cols is not None else data
        return data.to_numpy().astype(dtype=dtype)

    def reset(self):
        self._opener.reset()

    def order(self, what: str = None):
        return Brewery(trj_file=self._path, fmt=self._fmt, what=what)

    @color_print_verbose(name=__print_option__["brewery"])
    def _set_atom_info(self, verbose: bool = True):
        atom_brew_data = self.brew(cols=self._opener._atom_keyword, dtype=str, verbose=False)
        self.atom_info = np.unique(atom_brew_data, return_counts=True)
        self.atom_kind = self.atom_info[0]
        self.atom_num = np.sum(self.atom_info[1])

    def _init_opener(self, **kwrgs) -> Opener:
        trj_opener: Opener = self.__support_opener__[self._fmt]
        if trj_opener.is_require_gro:
            gro_file = kwrgs.pop("gro_file", None)
            assert gro_file is not None, f"{self._fmt} format require gro file, plz input with gro_file='some_gro'"
            return trj_opener(path=self._path, gro=gro_file)
        else:
            return trj_opener(path=self._path)

    def _check_fmt(self, fmt: str):
        fmt_list = list(self.__support_opener__.keys())
        assert fmt in fmt_list, f"fmt should be in {fmt_list}"
        if fmt == "auto":
            file_name = self._path.split("/")[-1]
            fmt = file_name.split(".")[-1]
        return fmt

    def _check_path(self, path, **kwrgs):
        path = os.path.join(os.getcwd(), path)
        assert os.path.isfile(path=path), f"Check your path || not {path}"
        return path

    def frange(self, __start: int = 0, __end: int = None, __step: int = 1):
        self.reset()
        assert __start >= 0, ValueError("Frame start idx should be positive")
        i = 0
        while i < __start:
            max_frame = i
            try:
                self.next_frame
                i += 1
            except:
                raise ValueError(f"start idx should be lower than {max_frame}")
        while True:
            try:
                if self.frame == __end:
                    break
                if not (self.frame - __start) % __step:
                    yield self.frame
                self.next_frame
            except:
                break
