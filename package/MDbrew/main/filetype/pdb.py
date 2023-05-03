from .opener import Opener


class pdbOpener(Opener):
    def __init__(self, path: str, is_generator: str = False) -> None:
        super().__init__(path, is_generator)
        self.path = path
        self.skip_head = 2
        self.column = ["type", "id", "atom", "x", "y", "z", "ax", "bx", "resdue"]

    def _make_one_frame_data(self, file, first_loop_line):
        second_loop_line = file.readline()
        self.box_size = [float(box_length) for box_length in second_loop_line.split()[1:4]]
        one_frame_data = []
        while True:
            line = file.readline()
            if "END" in line:
                break
            one_frame_data.append(line.split())
        return one_frame_data
