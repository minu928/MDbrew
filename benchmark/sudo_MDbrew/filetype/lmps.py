from .opener import Opener


class lmpsOpener(Opener):
    def __init__(self, path: str, is_generator: str = False, what: str = None) -> None:
        super().__init__(path, is_generator, what)

    def _make_one_frame_data(self, file, first_loop_line):
        self.skip_line(file=file, num=2)
        self.atom_num = int(file.readline().split()[0])
        self.skip_line(file=file, num=1)
        self.box_size = [sum([abs(float(box_length)) for box_length in file.readline().split()]) for _ in range(3)]
        self.column = file.readline().split()[2:]
        if self._atom is None:
            return [self.str2float_list(file.readline().split()) for _ in range(self.atom_num)]
        else:
            database = []
            for _ in range(self.atom_num):
                line = file.readline().split()
                if line[1] == str(self._atom):
                    database.append(self.str2float_list(line))
            self.atom_num = len(database)
            return database

    def skip_line(self, file, num):
        for _ in range(num):
            file.readline()

    def str2float_list(self, str_list):
        return [float(data) for data in str_list]
