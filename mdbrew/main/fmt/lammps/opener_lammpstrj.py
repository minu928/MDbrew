from mdbrew.main.interface import OpenerInterface


def skip_line(file, num):
    for _ in range(num):
        file.readline()


class lammpstrjOpener(OpenerInterface):
    fmt: str = "lammpstrj"
    is_require_atomdict = True

    def __init__(self, path: str, *args, **kwrgs) -> None:
        super().__init__(path, *args, **kwrgs)
        self.atom_keyword = "type"

    def _make_one_frame_data(self, file):
        skip_line(file=file, num=3)
        atom_num = int(file.readline().split()[0])
        skip_line(file=file, num=1)
        self.box_size = [float(line.split()[1]) - float(line.split()[0]) for line in (file.readline() for _ in range(3))]
        self.column = file.readline().split()[2:]
        self.total_line_num = 9 + atom_num
        return [file.readline().split() for _ in range(atom_num)]
