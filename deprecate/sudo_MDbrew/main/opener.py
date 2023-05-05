import abc


class Opener(object):
    def __init__(self, path: str, is_generator: str = False) -> None:
        self.path = path
        self.skip_head = 0
        self.column = []
        self.box_size = []
        self.frame_num = -1
        self._database = None
        self.is_generator = is_generator
        self._atom_keyword = "atom"

    def reset(self):
        self.__init__(path=self.path, is_generator=self.is_generator)

    @property
    def database(self):
        if self._database is None:
            self.make_database()
        return self._database

    def make_database(self):
        if self.is_generator:
            self._load_info()
            self._database = self._generate_database()
        else:
            self._database = self._iterate_database()

    @abc.abstractmethod
    def _make_one_frame_data(self, file, first_loop_line):
        pass

    # Iteration database
    def _iterate_database(self):
        database = []
        with open(file=self.path, mode="r") as file:
            for _ in range(self.skip_head):
                file.readline()
            while True:
                line = file.readline()
                if not line:
                    break
                database.append(self._make_one_frame_data(file=file, first_loop_line=line))
        self.frame_num = len(database)
        return database

    # Generation database
    def _generate_database(self):
        with open(file=self.path, mode="r") as file:
            for _ in range(self.skip_head):
                file.readline()
            while True:
                line = file.readline()
                if not line:
                    break
                self.frame_num += 1
                yield self._make_one_frame_data(file=file, first_loop_line=line)

    def _load_info(self):
        with open(file=self.path, mode="r") as file:
            for _ in range(self.skip_head):
                file.readline()
            line = file.readline()
            self._make_one_frame_data(file=file, first_loop_line=line)
