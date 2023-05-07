from ..opener import Opener


class lmpsOpener(Opener):
    def __init__(self, path: str, *args, **kwrgs) -> None:
        super().__init__(path, *args, **kwrgs)
        self._atom_keyword = "type"
        super().gen_db()

    def _make_one_frame_data(self, file):
        self.skip_line(file=file, num=3)
        atom_num = int(file.readline().split()[0])
        self.skip_line(file=file, num=1)
        self.box_size = [sum([abs(float(box_length)) for box_length in file.readline().split()]) for _ in range(3)]
        self.column = file.readline().split()[2:]
        return [self.str2float_list(file.readline().split()) for _ in range(atom_num)]

    def skip_line(self, file, num):
        for _ in range(num):
            file.readline()

    def str2float_list(self, str_list):
        return [float(data) for data in str_list]
