from .opener import Opener


class xyzOpener(Opener):
    def __init__(self, path: str, is_generator: str = False, what: str = None) -> None:
        super().__init__(path, is_generator, what)
        self.column = ["atom", "x", "y", "z"]
        self.gen_database()

    def _make_one_frame_data(self, file, first_loop_line):
        self.num_atom = int(first_loop_line.split()[0])
        second_line = file.readline()
        return [file.readline().split() for _ in range(self.num_atom)]
