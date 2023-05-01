from .openerinterface import OpenerInterface


class lmpsOpener(OpenerInterface):
    def __init__(self, path: str) -> None:
        super().__init__(path)
        self._database = self.gen_database()

    def _make_one_frame_data(self, file, first_loop_line):
        self.skip_line(file = file, num=2)
        self.atom_num = int(file.readline().split()[0])
        self.skip_line(file = file, num=1)
        self.box_size = [sum([abs(float(box_length)) for box_length in file.readline().split()]) for _ in range(3)]
        self.column = file.readline().split()[2:]
        # Data line
        return [file.readline().split() for _ in range(self.atom_num)]

    def skip_line(self, file, num):
        for _ in range(num): file.readline()