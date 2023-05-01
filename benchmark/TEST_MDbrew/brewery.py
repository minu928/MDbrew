import os
import numpy as np
import pandas as pd
from .tool.colorfont import color
from .tool.decorator import color_print
from .filetype.lmps import lmpsOpener
from .filetype.pdb import pdbOpener
from .filetype.vasp import vaspOpener
from .filetype.xyz import xyzOpener


# Extractor of Something
class Brewery(object):
    __support_fmt_opener__ = {"auto": None, "pdb": pdbOpener, "xyz": xyzOpener, "vasp": vaspOpener, "lmps": lmpsOpener}
    __printing_option__ = {
        "opener": f" #LOAD  {color.font_yellow}Files      {color.reset}",
        "b_brewing": f" #BREW  {color.font_yellow}Something  {color.reset}",
        "b_coords": f" #BREW  {color.font_yellow}Coords     {color.reset}",
        "b_atominfo": f" #BREW  {color.font_yellow}Atom Info  {color.reset}",
    }

    def __init__(self, path: str, fmt: str = "auto") -> None:
        self.__check_fmt(fmt=fmt)
        self.__check_path(path=path)
        self.__load_opener(path=path)

    @color_print(name=__printing_option__["opener"])
    def __load_opener(self, path):
        self._opener = self.__support_fmt_opener__[self.fmt](path=path)
        self.database = self._opener.database
        self.columns = self._opener.column
        self.box_size = self._opener.box_size
        self.frame_num = self._opener.frame_num

    def __check_fmt(self, fmt: str):
        assert fmt in self.__support_fmt_opener__, f"fmt should be in {list(self.__support_fmt_opener__.keys())}"
        self.fmt = fmt

    def __check_path(self, path):
        assert os.path.isfile(path=path), f"Check your path || not {path}"
        if self.fmt == "auto":
            file_name = path.split("/")[-1]
            file_fmt = file_name.split(".")[-1]
            self.fmt = file_fmt

    def query(self, ment: str = None):
        for data in self.database:
            df_data = pd.DataFrame(data=data, columns=self.columns)
            yield df_data.query(ment) if ment is not None else df_data

    @color_print(name=__printing_option__["b_brewing"])
    def brew(self, ment: str = None, cols: list[str] = None, max_iter: int = None, dtype: str = "float32"):
        return self.__brewing__(ment=ment, cols=cols, max_iter=max_iter, dtype=dtype)

    @color_print(name=__printing_option__["b_coords"])
    def brew_coords(self, ment: str = None, xyz_list: list[str] = None, max_iter: int = None, dtype: str = "float32"):
        xyz_list = ["x", "y", "z"] if xyz_list is None else xyz_list
        return self.__brewing__(ment=ment, cols=xyz_list, max_iter=max_iter, dtype=dtype)

    @color_print(name=__printing_option__["b_atominfo"])
    def brew_atom_info(self, cols: str = ["atom"], max_iter: int = 1, dtype: str = "str"):
        return np.unique(self.__brewing__(ment=None, cols=cols, max_iter=max_iter, dtype=dtype), return_counts=True)

    def __brewing__(self, ment: str = None, cols: list[str] = None, max_iter: int = None, dtype: str = "float32"):
        max_iter = self.frame_num if max_iter is None else max_iter
        assert max_iter <= self.frame_num, f"max_iter is larger than {self.frame_num}, not {max_iter}"
        assert set(cols) <= set(
            self.columns
        ), f"cols should be subset of columns, your cols: {cols} || columns: {self.columns}"
        flatten_database = np.reshape(self.database[:max_iter], (-1, len(self.columns)))
        flatten_database = pd.DataFrame(data=flatten_database, columns=self.columns)
        flatten_database = flatten_database.query(ment) if ment is not None else flatten_database
        flatten_database = flatten_database.loc[:, cols].to_numpy(dtype=dtype)
        return flatten_database.reshape([max_iter, -1, len(cols)])
