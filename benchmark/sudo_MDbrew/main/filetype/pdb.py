from ..opener import Opener


class pdbOpener(Opener):
    ending_num_for_pdb = None

    def __init__(self, path: str, *args, **kwrgs) -> None:
        super().__init__(path, *args, **kwrgs)
        self.path = path
        self.skip_head = 2
        self.column = ["type", "id", "atom", "x", "y", "z", "ax", "bx", "residue"]
        super().gen_db()

    def _make_one_frame_data(self, file):
        first__loop_line = file.readline()
        assert "REMARK" in first__loop_line
        second_loop_line = file.readline()
        self.box_size = [float(box_length) for box_length in second_loop_line.split()[1:4]]
        one_frame_data = []
        self.total_line_num = 3
        if self.ending_num_for_pdb is None:
            while True:
                line = file.readline()
                if "END" in line:
                    break
                self.total_line_num += 1
                splited_line = line.split()
                one_frame_data.append(splited_line)
                self.ending_num_for_pdb = int(splited_line[1])
        else:
            self.total_line_num += self.ending_num_for_pdb
            one_frame_data = [file.readline().split() for _ in range(self.ending_num_for_pdb)]
            file.readline()
        return one_frame_data
