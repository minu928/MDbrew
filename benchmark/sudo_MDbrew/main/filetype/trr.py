import struct
import numpy as np
from ..opener import Opener

from .gro import GRO_COLUMNS, _read_gro_file

GRO_IDX = 3

FLOAT_SIZE = struct.calcsize("f")
DOUBLE_SIZE = struct.calcsize("d")
DIM = 3
COLUMNS = (
    "ir_size",
    "e_size",
    "box_size",
    "virial_size",
    "pressure_size",
    "top_size",
    "sym_size",
    "x_size",
    "v_size",
    "f_size",
    "natoms",
    "step",
    "nre",
    "time",
    "lambda",
)


def unpack_fmt_and_read_line(file, fmt):
    size = struct.calcsize(fmt)
    data = file.read(size)
    data = struct.unpack(fmt, data)
    return data


def check_double(columns_info):
    key_order = ("box_size", "x_size", "v_size", "f_size")
    size = 0
    for key in key_order:
        if columns_info[key] != 0:
            if key == "box_size":
                size = int(columns_info[key] / DIM**2)
                break
            else:
                size = int(columns_info[key] / (columns_info["natoms"] * DIM))
                break
    assert size in [FLOAT_SIZE, DOUBLE_SIZE], ValueError(f"Could not determine size! || {size}")
    return size == DOUBLE_SIZE


class trrOpener(Opener):
    is_require_gro = True
    read_mode = "rb"

    def __init__(self, path: str, *args, **kwrgs) -> None:
        super().__init__(path, *args, **kwrgs)
        self._arrow = ">"
        self._dim = DIM
        self._gro_data = _read_gro_file(gro=kwrgs.pop("gro"), idx=GRO_IDX)
        super().gen_db()

    # Abstract data
    def _make_one_frame_data(self, file):
        self.columns_info = self._make_columns(file=file)
        self.system_data, self.motion_data = self._make_database(file=file)
        self.box_size = np.diagonal(self.system_data["box"])
        self.column = self._transform_columns()
        return self._transform_database(self.motion_data)

    def _make_columns(self, file):
        info = unpack_fmt_and_read_line(file=file, fmt=f"{self._arrow}1i")
        tnum = unpack_fmt_and_read_line(file=file, fmt=f"{self._arrow}2i")
        vers = unpack_fmt_and_read_line(file=file, fmt=f"{self._arrow}{tnum[0]-1}s")
        version = vers[0].split(b"\0", 1)[0].decode("utf-8")
        assert info[0] == 1993, "I can not open this file"
        assert version == "GMX_trn_file", ValueError("Unkown format")
        column_data = unpack_fmt_and_read_line(file=file, fmt=f"{self._arrow}13i")
        columns_info = {COLUMNS[idx]: data for idx, data in enumerate(column_data)}
        self._is_double = check_double(columns_info=columns_info)
        num_fmt = f"{self._arrow}2d" if self._is_double else f"{self._arrow}2f"
        num = unpack_fmt_and_read_line(file=file, fmt=num_fmt)
        columns_info["time"] = num[0]
        columns_info["lambda"] = num[1]
        return columns_info

    def _transform_columns(self):
        column_dict = {"x_size": "", "v_size": "v", "f_size": "f"}
        xyz_list = ["x", "y", "z"]
        columns = GRO_COLUMNS[:GRO_IDX]
        for key, word in column_dict.items():
            if self.columns_info[key]:
                for xyz in xyz_list[: self._dim]:
                    columns.append(word + xyz)
        return columns

    def _make_database(self, file):
        system_data = {}
        motion_data = {}
        for key in ("box", "virial", "pressure"):
            column_key = f"{key}_size"
            if self.columns_info[column_key] != 0:
                system_data[key] = self._read_main_data(file=file, idx=self._dim)

        for key in ("x", "v", "f"):
            column_key = f"{key}_size"
            if self.columns_info[column_key] != 0:
                motion_data[key] = self._read_main_data(file=file, idx=self.columns_info["natoms"])

        return system_data, motion_data

    def _transform_database(self, motion_data: dict):
        gro_data = self._gro_data
        val_data = np.hstack([val for key, val in motion_data.items()])
        return np.hstack([gro_data, val_data])

    def _read_main_data(self, file, idx):
        fmt = f"{self._arrow}{idx * self._dim}"
        fmt += "d" if self._is_double else "f"
        data = unpack_fmt_and_read_line(file=file, fmt=fmt)
        return np.array(data).reshape([idx, self._dim])
