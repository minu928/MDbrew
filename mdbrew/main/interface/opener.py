from typing import Dict, Type
from abc import abstractmethod, abstractproperty, ABCMeta


class OpenerInterface(metaclass=ABCMeta):
    skip_head = 0
    read_mode = "r"
    is_require_gro = False
    total_line_num = 0

    def __init__(self, path: str, *args, **kwrgs) -> None:
        self.path = path
        self.column = []
        self.box_size = []
        self.atom_keyword = "atom"

    def __init_subclass__(cls) -> None:
        name = cls.fmt.lower()
        opener_programs[name] = cls

    @property
    def database(self):
        if not hasattr(self, "_database"):
            self._database = self.generate_database()
        return self._database

    @property
    def data(self):
        if not hasattr(self, "_data"):
            self._data = next(self.database)
        return self._data

    @abstractproperty
    def fmt(self) -> str:
        pass

    def next_frame(self):
        self._data = next(self._database)

    def move_frame(self, num):
        total_skip_line = self.total_line_num * num
        self.skip_head += total_skip_line
        self._database = self.generate_database(frame_num=num)
        self._data = next(self._database)
        self.skip_head -= total_skip_line

    # Generation database
    def generate_database(self, frame_num: int = 0):
        self.frame = frame_num - 1
        with open(file=self.path, mode=self.read_mode) as file:
            self._skip_the_line(file=file)
            while True:
                try:
                    self.frame += 1
                    yield self._make_one_frame_data(file=file)
                except:
                    break

    @abstractmethod
    def _make_one_frame_data(self, file):
        pass

    def _skip_the_line(self, file):
        if self.read_mode == "r":
            for _ in range(self.skip_head):
                file.readline()
        elif self.read_mode == "rb":
            file.read(self.skip_head)
        else:
            raise ValueError("plz input correct read mode")


opener_programs: Dict[str, Type[OpenerInterface]] = {}
