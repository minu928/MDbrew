from ..opener import Opener


class pdbOpener(Opener):
    def __init__(self, path: str, *args, **kwrgs) -> None:
        super().__init__(path, *args, **kwrgs)
        self.path = path
        self.skip_head = 2
        self.column = ["type", "id", "atom", "x", "y", "z", "ax", "bx", "residue"]
        super().gen_db()

    def _make_one_frame_data(self, file):
        first__loop_line = file.readline()
        second_loop_line = file.readline()
        self.box_size = [float(box_length) for box_length in second_loop_line.split()[1:4]]
        one_frame_data = []
        self.total_line_num = 3
        while True:
            line = file.readline()
            if "END" in line:
                break
            self.total_line_num += 1
            one_frame_data.append(line.split())
        return one_frame_data
