from .tools import timeCount

# 1st Generation
class Opener(object):
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        self.lines = self._get_lines()

    # Open the file and delete all empty line
    def _get_lines(self) -> list[str]:
        with open(self.file_path) as file:
            lines = file.readlines()
        lines = list(map(lambda line: line.strip(), lines))
        return lines

    # split data in line with overall lines
    def _split_data_in_lines(self, lines: list[str]) -> list[float]:
        return [self.__str_to_float(line=line.split(" ")) for line in lines]

    # Change data string to float
    def __str_to_float(self, line) -> list[float]:
        try:
            line = list(map(lambda string: float(string), line))
        except:
            print(line)
            raise Exception("We cannot change string to float in each data")
        return line

    # # find the idx list of start point
    def _find_idxlist_by_word(self, word: str) -> list[int]:
        return [idx for idx, line in enumerate(self.lines) if word in line]

    # find the first idx
    def _find_idx_by_word(self, word: str) -> int:
        for idx, line in enumerate(self.lines):
            if word in line:
                return idx


# 2nd Generation -> For "dump.lammpstrj"
class DumpOpener(Opener):
    def __init__(self, file_path: str, target_info: list[str] = None):
        """Dump Opener

        Open the file, dump.lammpstrj and Get Database

        Args:
            file_path   (str)       :   file path of dump.lammpstrj
            target_info (list[str]) :   List with string, target_line = "id", target_word = "NUMBER"

        Example:
            >>> data        = DumpOpener(file_path)
            >>> database    = data.get_database
            >>> columns     = data.get_columns
            >>> system_size = data.get_system_size
            >>> time_step   = data.get_time_step
        """
        print("TEST VERSION")
        super().__init__(file_path)
        target_info = self.__check_target_info(target_info)
        self.target_line = target_info[0]
        self.target_word = target_info[1]
        self.system_num: int = int(
            self.lines[super()._find_idx_by_word(self.target_word) + 1]
        )
        self.start_idx_list: list[int] = super()._find_idxlist_by_word(self.target_line)

    # Get the database from a, b
    @timeCount
    def get_database(self) -> list:
        database: list = []
        for idx in self.start_idx_list:
            start_idx: int = idx + 1
            end_idx: int = start_idx + self.system_num
            data = self.lines[start_idx:end_idx]
            data = super()._split_data_in_lines(lines=data)
            database.append(data)
        return database

    # Find the columns data in lines
    @timeCount
    def get_columns(self, erase_appendix: int = 2) -> list[str]:
        column_idx: int = self.start_idx_list[0]
        return self.lines[column_idx].split(" ")[erase_appendix:]

    # find the system size
    @timeCount
    def get_system_size(self, dim: int = 3, word: str = "BOX") -> list[float]:
        size_idx = super()._find_idx_by_word(word=word) + 1
        system_size = self.lines[size_idx : size_idx + dim]
        system_size = super()._split_data_in_lines(lines=system_size)
        return system_size

    # find the time step
    @timeCount
    def get_time_step(self, word: str = "TIMESTEP") -> list[float]:
        time_step_idxlist = super()._find_idxlist_by_word(word=word)
        time_step_list = [int(self.lines[idx + 1]) for idx in time_step_idxlist]
        return time_step_list

    # Check target_information
    def __check_target_info(self, target_info: list[str]) -> list[str]:
        if target_info == None:
            return ["id", "NUMBER"]
        else:
            assert len(target_info) != 2
            return target_info
