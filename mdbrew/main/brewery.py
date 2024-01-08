import os
import numpy as np
import pandas as pd
from mdbrew.main.interface import get_opener, get_writer
from mdbrew.tool.colorfont import color
from mdbrew.tool.decorator import color_print_verbose, color_tqdm


def _check_path(path, **kwrgs):
    path = os.path.join(os.getcwd(), path)
    assert os.path.isfile(path=path), f"Check your path || not {path}"
    return path


__print_option__ = {
    "brewery": f" #OPEN  {color.font_yellow}Brewery {color.reset}",
    "b_brewing": f" #BREW  {color.font_yellow}Some...  {color.reset}",
    "b_coords": f" #BREW  {color.font_yellow}Coords     {color.reset}",
    "b_atominfo": f" #BREW  {color.font_yellow}Atom Info  {color.reset}",
}


class Brewery(object):
    def __init__(self, trj_file: str, fmt: str = "auto", auto_load: bool = True, *args, **kwrgs):
        self._what = kwrgs.pop("what", None)
        self._verbose = kwrgs.pop("verbose", False)
        self._path = _check_path(path=trj_file, **kwrgs)
        self.opener = self._match_fmt_with_opener(fmt=fmt, **kwrgs)
        self._kwrgs = kwrgs
        if auto_load:
            self.update_data()

    def __str__(self) -> str:
        LINE_WIDTH = 60
        sep_line = "=" * LINE_WIDTH
        print("")
        print(sep_line)
        print("||" + " " * 23 + " INFO " + " " * 27 + "||")
        print(sep_line)
        print(f"\t[  ATOM  ]:  KIND  ->   {tuple(self.atom_kind)}")
        print(f"\t[  ATOM  ]:  NUMB  ->   {tuple(self.atom_info[-1])}")
        print(f"\t[  BOX   ]:  SHAPE ->   {np.array(self.box_size).shape}")
        print(f"\t[ COORDS ]:  SHAPE ->   {self.coords.shape}")
        print(f"\t[ FRAMES ]:   NOW  ->   {self.frame:4d}")
        print(sep_line)
        return f"\t    @CopyRight by  {color.font_blue}minu928@snu.ac.kr{color.reset}\n"

    @property
    def atom_info(self):
        if not hasattr(self, "_atom_info"):
            self._set_atom_info()
        return self._atom_info

    @property
    def atom_kind(self):
        if not hasattr(self, "_atom_kind"):
            self._set_atom_info()
        return self._atom_kind

    @property
    def atom_num(self):
        if not hasattr(self, "_atom_num"):
            self._set_atom_info()
        return self._atom_num

    @property
    def box_size(self):
        return np.array(self.opener.box_size)

    @box_size.setter
    def box_size(self, box_size):
        self.opener.box_size = box_size

    @property
    def columns(self):
        return self.opener.column

    @columns.setter
    def columns(self, columns):
        self.opener.column = columns

    @property
    def coords(self):
        return self.brew(cols=["x", "y", "z"], dtype=float, verbose=False)

    @property
    def velocities(self):
        return self.brew(cols=["vx", "vy", "vz"], dtype=float, verbose=False)

    @property
    def forces(self):
        return self.brew(cols=["fx", "fy", "fz"], dtype=float, verbose=False)

    @property
    def data(self):
        if not hasattr(self, "_data"):
            self.update_data()
        return self._data

    @data.setter
    def data(self, data):
        self._data = data

    @property
    def frame(self):
        return self.opener.frame

    @property
    def fmt(self):
        return self.opener.fmt

    def update_data(self):
        self._data = pd.DataFrame(data=self.opener.data, columns=self.columns)
        self._data["id"] = self._data["id"].astype(int)
        self._data["x"] = self._data["x"].astype(float)
        self._data["y"] = self._data["y"].astype(float)
        self._data["z"] = self._data["z"].astype(float)
        if self._what is not None:
            self._data.query(self._what, inplace=True)
        assert len(self._data), "Data is empty"

    def next_frame(self):
        self.opener.next_frame()
        self.update_data()

    def move_frame(self, num: int):
        self.opener.move_frame(num=int(num))
        self.update_data()

    @color_print_verbose(name=__print_option__["b_brewing"])
    def brew(self, cols=None, what: str = None, dtype: str = str, verbose: bool = False):
        data = self.data
        data = data.query(what) if what is not None else data
        data = data.loc[:, cols] if cols is not None else data
        return data.to_numpy(dtype=dtype)

    def reset(self):
        self.opener.reset()

    def order(self, what: str = None, verbose: bool = False):
        return Brewery(trj_file=self._path, fmt=self.fmt, what=what, verbose=verbose, **self._kwrgs)

    def reorder(self):
        return Brewery(trj_file=self._path, fmt=self.fmt, what=self._what, verbose=False, **self._kwrgs)

    @color_tqdm(name="FRAME")
    def frange(self, start: int = 0, end: int = None, step: int = 1, verbose: bool = False):
        assert end is None or start < end, "start should be lower than end"
        self.opener.move_frame(num=int(start))
        try:
            while self.frame != end:
                if (self.frame - start) % step == 0:
                    yield self.frame
                self.next_frame()
        except StopIteration:
            pass
        finally:
            self.move_frame(0)  # Reset the database

    def write(self, fmt: str, save_path: str, start: int = 0, end: int = None, step: int = 1, **kwrgs):
        fmt = fmt.lower()
        _writer = get_writer(fmt=fmt)(save_path, brewery=self, **kwrgs)
        _writer.write(start=start, end=end, step=step)

    @color_print_verbose(name=__print_option__["brewery"])
    def _set_atom_info(self, verbose: bool = True):
        atom_brew_data = self.brew(cols=self.opener.atom_keyword, dtype=str, verbose=False)
        self._atom_info = np.unique(atom_brew_data, return_counts=True)
        self._atom_kind = self.atom_info[0]
        self._atom_num = np.sum(self.atom_info[1])

    def _match_fmt_with_opener(self, fmt, **kwrgs):
        if fmt == "auto":
            fmt = self._path.split(os.path.sep)[-1].split(".")[-1].lower()
        trj_opener = get_opener(fmt=fmt)
        if trj_opener.is_require_gro:
            gro_file = kwrgs.pop("gro", None)
            assert gro_file is not None, f"{fmt} require gro file, plz input with 'gro=path_of_gro'"
            return trj_opener(path=self._path, gro=gro_file)
        return trj_opener(path=self._path)
