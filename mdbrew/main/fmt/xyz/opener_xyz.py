from mdbrew.main.interface import OpenerInterface


class xyzOpener(OpenerInterface):
    fmt: str = "xyz"

    def __init__(self, path: str, *args, **kwrgs) -> None:
        super().__init__(path, *args, **kwrgs)
        self.column = ["atom", "x", "y", "z"]
        super().gen_db()

    def _make_one_frame_data(self, file):
        first_loop_line = file.readline()
        atom_num = int(first_loop_line.strip())
        file.readline()
        self.total_line_num = atom_num + 2
        return [file.readline().split() for _ in range(atom_num)]
