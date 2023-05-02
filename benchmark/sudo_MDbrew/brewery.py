import os
from .brewer import Brewer
from .tool.colorfont import color
from .tool.decorator import color_print
from .filetype.opener import Opener
from .filetype.lmps import lmpsOpener
from .filetype.pdb import pdbOpener
from .filetype.vasp import vaspOpener
from .filetype.xyz import xyzOpener


class Brewery(object):
    __support_opener__ = {"auto": None, "pdb": pdbOpener, "xyz": xyzOpener, "vasp": vaspOpener, "lmps": lmpsOpener}
    __printing_option__ = {"brewery": f" #LOAD  {color.font_yellow}Files      {color.reset}"}

    @color_print(name=__printing_option__["brewery"])
    def __init__(self, path: str, fmt: str = "auto", is_generator: bool = False, what:str = None) -> None:
        self._what = what
        self.is_generator = is_generator
        self.__check_fmt(fmt=fmt)
        self.__check_path(path=path)
        self._opener = self.__set_opener()
        self._brewer = self.__set_brewer()
        self.__load_data()
        self.__load_info()

    def reload(self, what: str = None):
        self._opener = self.__set_opener()
        self._brewer = self.__set_brewer()
        self.__load_data()
        self.__load_info()

    def order(self, what: str = None):
        return Brewery(path=self._path, fmt=self.fmt, is_generator=self.is_generator, what=what)

    def __set_opener(self) -> Opener:
        return self.__support_opener__[self.fmt](path=self._path, is_generator=self.is_generator, what=self._what)

    def __set_brewer(self) -> Brewer:
        return Brewer(opener=self._opener)

    def __load_data(self):
        self._opener.load_database()
        self.database = self._opener.database

    def __load_info(self):
        self.columns = self._opener.column
        self.box_size = self._opener.box_size
        self.frame_num = self._opener.frame_num
        self.atom_num = self._opener.atom_num

    def __check_fmt(self, fmt: str):
        assert fmt in self.__support_opener__.keys(), f"fmt should be in {list(self.__support_opener__.keys())}"
        if fmt == "auto":
            file_name = self._path.split("/")[-1]
            file_fmt = file_name.split(".")[-1]
            self.fmt = file_fmt
        else:
            self.fmt = fmt

    def __check_path(self, path):
        assert os.path.isfile(path=path), f"Check your path || not {path}"
        self._path = path

    def brew(self, ment: str = None, cols: list[str] = None, dtype: str = "float32", **kwrgs):
        brewed_data = self._brewer.brew(ment=ment, cols=cols, dtype=dtype, **kwrgs)
        self.__load_info()
        return brewed_data
