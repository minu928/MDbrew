from ..opener import Opener


class xyzOpener(Opener):
    def __init__(self, path: str) -> None:
        super().__init__(path)
        self.column = ["atom", "x", "y", "z"]
        self.gen_db()

    def _make_one_frame_data(self, file, first_loop_line):
        atom_num = int(first_loop_line.split()[0])
        second_line = file.readline()
        return [file.readline().split() for _ in range(atom_num)]
