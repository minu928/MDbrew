from ..opener import Opener


class vaspOpener(Opener):
    def __init__(self, path: str, *args, **kwrgs) -> None:
        super().__init__(path, *args, **kwrgs)
        self.skip_head = 7
        self.column = ["atom", "x", "y", "z"]
        self._set_box_and_atom(path=path)
        super().gen_db()

    def _make_one_frame_data(self, file):
        first_loop_line = file.readline()
        step = first_loop_line.split()[-1]
        num_atom = sum(self.atom_kind_num)
        database = []
        c_atom_num = 0
        pointer = 0
        for _ in range(num_atom):
            if c_atom_num >= self.atom_kind_num[pointer]:
                pointer += 1
                c_atom_num = 0
            c_atom_num += 1
            line = [self.atom_kind[pointer]]
            line.extend(file.readline().split())
            database.append(line)
        return database

    def _set_box_and_atom(self, path):
        with open(path, "r") as raw_file:
            for i in range(2):
                raw_file.readline()
            for i in range(3):
                line = raw_file.readline().split()
                box_size = float(line[i])
                self.box_size.append(box_size)
            self.atom_kind = raw_file.readline().split()
            self.atom_kind_num = [int(data) for data in raw_file.readline().split()]
