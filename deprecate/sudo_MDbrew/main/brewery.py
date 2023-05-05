import os
import numpy as np
from .brewer import Brewer
from .opener import Opener
from .filetype.lmps import lmpsOpener
from .filetype.pdb import pdbOpener
from .filetype.vasp import vaspOpener
from .filetype.xyz import xyzOpener
from ..tool.colorfont import color
from ..tool.decorator import color_print


class Brewery(object):
    __support_opener__ = {"auto": None, "pdb": pdbOpener, "xyz": xyzOpener, "vasp": vaspOpener, "lmps": lmpsOpener}
    __printing_option__ = {"brewery": f" #OPEN  {color.font_yellow}Brewery {color.reset}"}

    def __init__(self, path: str, fmt: str = "auto", is_generator: bool = True, what: str = None, verbose: bool = True):
        self._what = what
        self._verbose = verbose
        self.is_generator = is_generator
        self.__check_path(path=path)
        self.__check_fmt(fmt=fmt)
        self.__load_opener()
        self.__set_atom_info()
        self._coords = None

    def __str__(self) -> str:
        LINE_WIDTH = 60
        sep_line = "=" * LINE_WIDTH
        print("")
        print(sep_line)
        print("||" + " " * 23 + " INFO " + " " * 27 + "||")
        print(sep_line)
        print(f"\t[  ATOM  ] : KIND  ->  {tuple(self.atom_kind)}")
        print(f"\t[  ATOM  ] : NUMB  ->  {tuple(self.atom_info[-1])}")
        print(f"\t[  CELL  ] : SHAPE ->  {np.array(self.box_size).shape}")
        print(f"\t[ FRAMES ] : NUMB  ->   {self.frame}")
        print(sep_line)
        return f"\t @CopyRight by  {color.font_blue}minu928@snu.ac.kr{color.reset}\n"

    @property
    def frame(self):
        frame = self._opener.frame_num
        return frame if frame >= 0 else 0

    @property
    def coords(self, cols: list[str] = None, max_iter: int = None, dtype: str = "float32"):
        if self._coords is None:
            xyz_list = ["x", "y", "z"] if cols is None else cols
            self._coords = self.brew(cols=xyz_list, max_iter=max_iter, dtype=dtype)
        return self._coords

    @property
    def brew(self, cols: list[str] = None, dtype: str = "float32", **kwrgs):
        return self._brewer

    def reset(self):
        self._opener.reset()
        self._coords = None

    def order(self, what: str = None):
        return Brewery(path=self._path, fmt=self.fmt, is_generator=self.is_generator, what=what)

    def reorder(self, verbose: bool = False):
        return Brewery(path=self._path, fmt=self.fmt, is_generator=self.is_generator, what=self._what, verbose=verbose)

    def __set_atom_info(self):
        one_brewing = self.brew(cols=self._opener._atom_keyword, max_iter=1, dtype="str")
        one_brewing = next(one_brewing) if self.is_generator else one_brewing
        self.atom_info = np.unique(one_brewing, return_counts=True)
        self.atom_kind = self.atom_info[0]
        self.atom_num = np.sum(self.atom_info[1])
        self.reset() if self.is_generator else None

    def __set_opener(self) -> Opener:
        return self.__support_opener__[self.fmt](path=self._path, is_generator=self.is_generator)

    def __set_brewer(self) -> Brewer:
        return Brewer(opener=self._opener, what=self._what)

    def __check_fmt(self, fmt: str):
        assert fmt in self.__support_opener__.keys(), f"fmt should be in {list(self.__support_opener__.keys())}"
        if fmt == "auto":
            file_name = self._path.split("/")[-1]
            file_fmt = file_name.split(".")[-1]
            self.fmt = file_fmt
        else:
            self.fmt = fmt

    def __check_path(self, path):
        path = os.path.join(os.getcwd(), path)
        assert os.path.isfile(path=path), f"Check your path || not {path}"
        self._path = path

    def __load_opener(self):
        self.__load_opener_with_verbose() if self._verbose else self.__load_opener_and_brewer()

    @color_print(name=__printing_option__["brewery"])
    def __load_opener_with_verbose(self):
        self.__load_opener_and_brewer()

    def __load_opener_and_brewer(self):
        self._opener = self.__set_opener()
        self._brewer = self.__set_brewer()
        self._coords = None
        self.columns = self._opener.column
        self.box_size = self._opener.box_size
