from ..opener import Opener


class xyzOpener(Opener):
    def __init__(self, path: str, is_generator: str = False) -> None:
        super().__init__(path, is_generator)
        self.column = ["atom", "x", "y", "z"]

    def _make_one_frame_data(self, file, first_loop_line):
        atom_num = int(first_loop_line.split()[0])
        second_line = file.readline()
        return [file.readline().split() for _ in range(atom_num)]
