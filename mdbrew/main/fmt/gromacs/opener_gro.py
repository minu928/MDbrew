from mdbrew.main.interface.opener import OpenerInterface


GRO_COLUMNS = ["resid", "atom", "id", "x", "y", "z", "vx", "vy", "vz"]


def _read_gro_file(gro, idx: int = 3):
    with open(file=gro, mode="r") as file:
        database, box_line = _make_gro_data(file=file, idx=idx)
        return database


def _make_gro_data(file, idx: int = 3):
    title = file.readline()
    num_atom = int(file.readline().strip())
    data = [file.readline().split()[:idx] for _ in range(num_atom)]
    box_line = file.readline()
    return data, box_line


class groOpener(OpenerInterface):
    fmt: str = "gro"

    def __init__(self, path: str, *args, **kwrgs) -> None:
        super().__init__(path, *args, **kwrgs)
        self.column = GRO_COLUMNS

    def _make_one_frame_data(self, file):
        read_data = _make_gro_data(file=file, idx=len(self.column))
        self.box_size = [float(box) for box in read_data[1].split()]
        return read_data[0]
