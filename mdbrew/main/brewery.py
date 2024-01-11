import numpy as np
import pandas as pd
from mdbrew.main.interface import get_opener, get_writer
from mdbrew.tool.colorfont import color
from mdbrew.tool.decorator import color_tqdm
from mdbrew.tool.path import check_path


DEFAULT_DATA_TYPES = {
    "x": float,
    "y": float,
    "z": float,
    "fx": float,
    "fy": float,
    "fz": float,
    "vx": float,
    "vy": float,
    "vz": float,
    "id": int,
    "atom": str,
    "element": str,
    "resid": str,
    "type":str,
}


class Brewery:
    def __init__(self, trj_file: str, fmt: str = "auto", auto_load: bool = True, *args, **kwrgs):
        self._what = kwrgs.pop("what", None)
        self._path = check_path(path=trj_file, **kwrgs)
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
            self.update_atom_info()
        return self._atom_info

    @property
    def atom_kind(self):
        if not hasattr(self, "_atom_kind"):
            self.update_atom_info()
        return self._atom_kind

    @property
    def atom_num(self):
        if not hasattr(self, "_atom_num"):
            self.update_atom_info()
        return self._atom_num

    @property
    def atoms(self):
        return self.brew(cols=self.opener.atom_keyword, dtype=str)

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
        return self.brew(cols=["x", "y", "z"], dtype=float)

    @property
    def velocities(self):
        return self.brew(cols=["vx", "vy", "vz"], dtype=float)

    @property
    def forces(self):
        return self.brew(cols=["fx", "fy", "fz"], dtype=float)

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

    @property
    def data_types(self):
        if not hasattr(self, "_data_types"):
            self._data_types = {col: DEFAULT_DATA_TYPES.get(col, str) for col in self.columns}
        return self._data_types

    def update_data(self):
        self._data = pd.DataFrame(data=self.opener.data, columns=self.columns).astype(self.data_types)
        if self._what is not None:
            self._data.query(self._what, inplace=True)
        assert len(self._data), "Data is empty"

    def update_atom_info(self):
        atom_brew_data = self.brew(cols=self.opener.atom_keyword, dtype=str)
        self._atom_info = np.unique(atom_brew_data, return_counts=True)
        self._atom_kind = self.atom_info[0]
        self._atom_num = np.sum(self.atom_info[1])

    def next_frame(self):
        self.opener.next_frame()
        self.update_data()

    def move_frame(self, num: int):
        self.opener.move_frame(num=int(num))
        self.update_data()

    def brew(self, cols=None, what: str = None, dtype: str = None):
        data = self.data
        data = data.query(what) if what is not None else data
        data = data.loc[:, cols] if cols is not None else data
        return data.to_numpy(dtype=dtype)

    def order(self, what: str = None):
        return Brewery(trj_file=self._path, fmt=self.fmt, what=what, **self._kwrgs)

    def reorder(self):
        return Brewery(trj_file=self._path, fmt=self.fmt, what=self._what, **self._kwrgs)

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
            self.reset()  # Reset the database

    def reset(self):
        self.move_frame(0)

    def write(self, fmt: str, save_path: str, start: int = 0, end: int = None, step: int = 1, scaling: float = 1.0, **kwrgs):
        fmt = fmt.lower()
        _writer = get_writer(fmt=fmt)(save_path, brewery=self, scaling=scaling, **kwrgs)
        _writer.write(start=start, end=end, step=step)

    def _match_fmt_with_opener(self, fmt, **kwrgs):
        if fmt == "auto":
            fmt = self._path.split("/")[-1].split(".")[-1].lower()
        trj_opener = get_opener(fmt=fmt)
        if trj_opener.is_require_gro:
            gro_file = kwrgs.pop("gro", None)
            assert gro_file is not None, f"{fmt} require gro file, plz input with 'gro=path_of_gro'"
            return trj_opener(path=self._path, gro=gro_file)
        return trj_opener(path=self._path)
