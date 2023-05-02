import numpy as np
import pandas as pd
from .filetype.opener import Opener
from .tool.colorfont import color
from .tool.decorator import color_print


class Brewer:
    __printing_option__ = {
        "b_brewing": f" #BREW  {color.font_yellow}Something  {color.reset}",
        "b_coords": f" #BREW  {color.font_yellow}Coords     {color.reset}",
        "b_atominfo": f" #BREW  {color.font_yellow}Atom Info  {color.reset}",
    }
    _what = None

    def __init__(self, opener: Opener) -> None:
        self._opener = opener
        self.is_generator = self._opener.is_generator
        self.__load_data()
        self.__load_info()

    def __load_data(self):
        self.database = self._opener.database

    def __load_info(self):
        self._opener.load_database()
        self.columns = self._opener.column
        self.box_size = self._opener.box_size
        self.frame_num = self._opener.frame_num
        self.atom_num = self._opener.atom_num

    def brew_quick(self, ment: str = None):
        for data in self.database:
            df_data = pd.DataFrame(data=data, columns=self.columns)
            yield df_data.query(ment) if ment is not None else df_data

    @color_print(name=__printing_option__["b_brewing"])
    def brew(self, ment: str = None, cols: list[str] = None, max_iter: int = None, dtype: str = "float32"):
        assert cols is not None, "Please input cols"
        return self.__define_brewing__(ment=ment, cols=cols, max_iter=max_iter, dtype=dtype)

    @color_print(name=__printing_option__["b_coords"])
    def brew_coords(self, ment: str = None, cols: list[str] = None, max_iter: int = None, dtype: str = "float32"):
        xyz_list = ["x", "y", "z"] if cols is None else cols
        return self.__define_brewing__(ment=ment, cols=xyz_list, max_iter=max_iter, dtype=dtype)

    @color_print(name=__printing_option__["b_atominfo"])
    def brew_atom_info(self, cols: str = ["atom"], max_iter: int = 1, dtype: str = "str"):
        return np.unique(
            self.__define_brewing__(ment=None, cols=cols, max_iter=max_iter, dtype=dtype), return_counts=True
        )

    def __define_brewing__(self, *args, **kwrgs):
        if self.is_generator:
            return self.__brewing_generator__(*args, **kwrgs)
        else:
            return self.__brewing__(*args, **kwrgs)

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

    def __brewing_generator__(
        self, ment: str = None, cols: list[str] = None, max_iter: int = None, dtype: str = "float32"
    ):
        assert set(cols) <= set(
            self.columns
        ), f"cols should be subset of columns, your cols: {cols} || columns: {self.columns}"
        for data in self.database:
            data = pd.DataFrame(data=data, columns=self.columns)
            data = data.query(ment) if ment is not None else data
            data = data.loc[:, cols].to_numpy(dtype=dtype)
            yield data
