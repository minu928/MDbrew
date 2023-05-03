from typing import Any
import numpy as np
import pandas as pd
from ..filetype.opener import Opener
from ...tool.colorfont import color
# from ...tool.decorator import color_print


class Brewer(object):
    __printing_option__ = {
        "b_brewing": f" #BREW  {color.font_yellow}Something  {color.reset}",
        "b_coords": f" #BREW  {color.font_yellow}Coords     {color.reset}",
        "b_atominfo": f" #BREW  {color.font_yellow}Atom Info  {color.reset}",
    }

    def __init__(self, opener: Opener, what: str = None) -> None:
        self._what = what
        self._opener = opener
        self.is_generator = self._opener.is_generator
        self.database = self._opener.database
        self.columns = self._opener.column
        self.frame_num = self._opener.frame_num

    def load_system_info(self):
        self.database = self._opener.database
        self.columns = self._opener.column
        self.frame_num = self._opener.frame_num

    def __call__(self, cols: list[str] = None, max_iter: int = None, dtype: str = "float32"):
        do_brewing = self.__define_brewing__(cols=cols, max_iter=max_iter, dtype=dtype)
        self.load_system_info()
        return do_brewing

    def __define_brewing__(self, cols: list[str] = None, max_iter: int = None, dtype: str = "float32"):
        assert (
            cols is None or cols in self.columns or set(cols) <= set(self.columns)
        ), f"cols should be subset of columns, your cols: {cols} || columns: {self.columns}"
        brewing = self.__generative_brewing__ if self.is_generator else self.__iterative_brewing__
        return brewing(cols=cols, max_iter=max_iter, dtype=dtype)

    def __iterative_brewing__(self, cols: list[str] = None, max_iter: int = None, dtype: str = "float32"):
        max_iter = self.frame_num if max_iter is None else max_iter
        flatten_database = np.reshape(self.database[:max_iter], (-1, len(self.columns)))
        flatten_database = self.__brew_database__(data=flatten_database, cols=cols)
        cols_num = len(cols) if type(cols) is list else 1
        return flatten_database.reshape([max_iter, -1, cols_num]).astype(dtype)

    def __generative_brewing__(self, cols: list[str] = None, max_iter: int = None, dtype: str = "float32"):
        yield from (self.__brew_database__(data=data, cols=cols) for data in self.database)

    def __brew_database__(self, data: pd.DataFrame, cols: list[str]):
        data = pd.DataFrame(data=data, columns=self.columns)
        data = data.query(self._what) if self._what is not None else data
        data = data.loc[:, cols] if cols is not None else data
        return data.to_numpy()