from abc import abstractmethod


class Opener(object):
    skip_head = 0
    read_mode = "r"
    is_require_gro = False
    total_line_num = 0

    def __init__(self, path: str, *args, **kwrgs) -> None:
        self.path = path
        self.column = []
        self.box_size = []
        self._atom_keyword = "atom"

    @property
    def database(self):
        return self._database

    @property
    def data(self):
        return self._data

    def _skip_the_line(self, file):
        if self.read_mode == "r":
            for _ in range(self.skip_head):
                file.readline()
        elif self.read_mode == "rb":
            file.read(self.skip_head)
        else:
            raise ValueError("plz input correct read mode")

    @abstractmethod
    def _make_one_frame_data(self, file):
        pass

    # Generation database
    def _generate_database(self):
        with open(file=self.path, mode=self.read_mode) as file:
            self._skip_the_line(file=file)
            while True:
                try:
                    self.frame += 1
                    yield self._make_one_frame_data(file=file)
                except:
                    break

    def gen_db(self, frame=0):
        self.frame = frame - 1
        self._database = self._generate_database()
        self.next_frame()

    def reset(self):
        self.gen_db()

    def skip_frame(self, num):
        total_skip_line = self.total_line_num * num
        self.skip_head += total_skip_line
        self.gen_db(frame=num)
        self.skip_head -= total_skip_line

    def next_frame(self):
        self._data = next(self._database)