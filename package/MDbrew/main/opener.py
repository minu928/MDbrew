import abc


class Opener(object):
    skip_head = 0
    read_mode = "r"
    is_require_gro = False

    def __init__(self, path: str, *args, **kwrgs) -> None:
        self.path = path
        self.column = []
        self.box_size = []
        self._atom_keyword = "atom"

    def gen_db(self):
        self.frame = -1
        self._database = self._generate_database()
        self.next_frame()

    def reset(self):
        self.gen_db()

    @property
    def database(self):
        return self._database

    @property
    def data(self):
        return self._data

    def next_frame(self):
        self._data = next(self._database)

    @abc.abstractmethod
    def _make_one_frame_data(self, file):
        pass

    # Generation database
    def _generate_database(self):
        with open(file=self.path, mode=self.read_mode) as file:
            for _ in range(self.skip_head):
                file.readline()
            while True:
                try:
                    self.frame += 1
                    yield self._make_one_frame_data(file=file)
                except:
                    break
