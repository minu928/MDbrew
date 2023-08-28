from ..opener import Opener
from ..writer import Writer


def skip_line(file, num):
    for _ in range(num):
        file.readline()


class lmpsOpener(Opener):
    def __init__(self, path: str, *args, **kwrgs) -> None:
        super().__init__(path, *args, **kwrgs)
        self.atom_keyword = "type"
        super().gen_db()

    def _make_one_frame_data(self, file):
        skip_line(file=file, num=3)
        atom_num = int(file.readline().split()[0])
        skip_line(file=file, num=1)
        self.box_size = [
            sum([float(box_length) * ((-1) ** (idx + 1)) for idx, box_length in enumerate(file.readline().split())])
            for _ in range(3)
        ]
        self.column = file.readline().split()[2:]
        self.total_line_num = 9 + atom_num
        return [file.readline().split() for _ in range(atom_num)]
