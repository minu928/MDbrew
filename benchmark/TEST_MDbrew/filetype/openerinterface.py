import abc

class OpenerInterface(object):
    def __init__(self, path: str) -> None:
        self.path = path
        self.skip_head = 0
        self.column = []
        self.box_size = []
        self.frame_num = 0
        self.atom_num = 0
        self._database = None
    
    @property
    def database(self):
        return self._database

    @abc.abstractmethod
    def _make_one_frame_data(self, file, first_loop_line):
        pass

    def gen_database(self):
        database = []
        process = 0
        with open(file=self.path, mode="r") as file:
            for _ in range(self.skip_head):
                file.readline()
            while True:
                line = file.readline()
                if not line:
                    break
                database.append(self._make_one_frame_data(file=file, first_loop_line=line))
                process += 1
        self.frame_num = len(database)
        self._database = database
        return database
