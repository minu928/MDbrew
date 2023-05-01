import os
import numpy as np
import pandas as pd
from .tool.colorfont import ColorFont
from .tool.deco import color_print
from .filetype.lmps import lmpsOpener
from .filetype.pdb import pdbOpener
from .filetype.vasp import vaspOpener
from .filetype.xyz import xyzOpener


color = ColorFont()

# Extractor of Something
class Brewery(object):
    __support_fmt_opener__ = {"auto": None, "pdb": pdbOpener, "xyz": xyzOpener, "vasp": vaspOpener, "lmps": lmpsOpener}
    __dtype__ = "float64"
    __printing_option = {
        "opener": f" #LOAD  {color.font_yellow}Opener{color.reset}",
        "brew": f" #BREW  {color.font_yellow}DATA{color.reset}",
    }

    def __init__(self, path: str, ordered: bool = True, fmt: str = "auto") -> None:
        self.check_fmt(fmt=fmt)
        self.check_path(path=path)
        self.load_opener(path=path)

    @color_print(name=__printing_option["opener"])
    def load_opener(self, path):
        self._opener = self.__support_fmt_opener__[self.fmt](path=path)
        self.database = self._opener.database
        self.columns = self._opener.column
        self.box_size = self._opener.box_size
        self.frame_num = self._opener.frame_num
        self.dim = 3

    def check_fmt(self, fmt: str):
        assert fmt in self.__support_fmt_opener__, f"fmt should be in {list(self.__support_fmt_opener__.keys())}"
        self.fmt = fmt

    def check_path(self, path):
        assert os.path.isfile(path=path), f"Check your path || not {path}"
        if self.fmt == "auto":
            file_name = path.split("/")[-1]
            file_fmt = file_name.split(".")[-1]
            self.fmt = file_fmt

    def query(self, ment: str = None):
        for data in self.database:
            df_data = pd.DataFrame(data=data, columns=self.columns)
            yield df_data.query(ment) if ment is not None else df_data

    @color_print(name=__printing_option["brew"])
    def brew(self, ment: str = None, max_iter: str = None, xyz_list: list[str] = None):
        max_iter = self.frame_num if max_iter is None else max_iter
        assert max_iter <= self.frame_num, f"max_iter is larger than {self.frame_num}, not {max_iter}"
        
        xyz_list = ["x", "y", "z"] if xyz_list is None else xyz_list
        assert xyz_list[0] in self.columns, f"Check your xyz_list in argument, not xyz_list = {xyz_list}"
        
        flatten_database = np.reshape(self.database, (-1, len(self.columns)))
        flatten_database = pd.DataFrame(data=flatten_database, columns=self.columns)
        flatten_database = flatten_database.query(ment) if ment is not None else flatten_database
        flatten_position = flatten_database.loc[:, xyz_list].to_numpy(dtype=self.__dtype__)
        flatten_position = flatten_position.reshape([self.frame_num, -1, self.dim])
        return flatten_position