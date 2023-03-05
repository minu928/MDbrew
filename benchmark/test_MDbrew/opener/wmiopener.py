import numpy as np
from typing import Tuple
from .opener import Opener


# 2nd Generation -> For "WMI-MD"
def _validate_file_extensions(out_file: str, fort77_file: str) -> None:
    assert out_file.endswith(".out"), NameError(f"Invalid out_file extension, expected '*.out', got '{out_file}'")
    assert fort77_file.endswith("fort.77"), NameError(
        f"Invalid fort77_file extension, expected 'fort.77', got '{fort77_file}'"
    )


class WMIOpener(Opener):
    def __init__(self, out_file: str, fort77_file: str) -> None:
        _validate_file_extensions(out_file, fort77_file)
        super().__init__(file_path=out_file)
        self._open_outfile()
        self.N = len(self.type_list)
        self.database = self.open_fort77(path=fort77_file, N=self.N)
        self.frame_number = len(self.database["t"])

    def _open_outfile(self) -> Tuple[np.ndarray, np.ndarray]:
        skip_top_idx = 11
        skip_bot_idx = -15
        target_out_file_lines = self.lines[skip_top_idx:skip_bot_idx:2]
        data = np.loadtxt(target_out_file_lines, usecols=(3, 4), dtype=str)
        type_list = data[:, 0]
        charge_list = data[:, 1].astype(int)
        return type_list, charge_list

    def open_fort77(self, path: str, N: int):
        self.dtype = np.dtype(
            [
                ("pre", bytes, 4),
                ("Nfc", np.int32),
                ("t", np.float64),
                ("Si", np.int32),
                ("box", np.float64, 3),
                ("mid", bytes, 8),
                ("coords", np.float32, (N, 3)),
                ("ter", bytes, 4),
            ]
        )
        try:
            database = np.memmap(path, dtype=self.dtype, mode="r")
        except BrokenPipeError:
            print("An error occurred while opening the fort.77 file")
            raise
        return database

    @property
    def type_list(self) -> np.ndarray:
        if not hasattr(self, "_type_list"):
            self._type_list, self._charge_list = self._open_outfile()
        return self._type_list

    @property
    def charge_list(self) -> np.ndarray:
        if not hasattr(self, "_charge_list"):
            self._type_list, self._charge_list = self._open_outfile()
        return self._charge_list

    def get_database(self, target_type: str = None):
        if target_type is None:
            return (xyz for xyz in self.database["coords"])
        elif target_type in self.type_list:
            select_idxes = np.where(self.type_list == target_type)
            return (xyz[select_idxes] for xyz in self.database["coords"])
        else:
            raise ValueError(f"Atom type '{target_type}' is not present in the system.")

    def get_columns(self):
        return ["type", "x", "y", "z", "charge"]

    def get_system_size(self):
        return self.database["box"]

    def get_time_step(self):
        return self.database["t"] * self.database["Si"]
