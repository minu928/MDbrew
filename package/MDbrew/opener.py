# 1st Generation
class Opener(object):
    def __init__(self, file_path) -> None:
        self.file_path = file_path

    # Open the file and delete all empty line
    def get_lines(self) -> list[str]:
        with open(self.file_path) as file:
            lines = file.readlines()
        lines = list(map(lambda line: line.strip(), lines))
        while "" in lines:
            lines.remove("")
        return lines

    # Seprate the data in lines
    def seperate_data_in_lines(self, lines: list[str]) -> list[float]:
        for idx, line in enumerate(lines):
            line_data = line.split(" ")
            lines[idx] = self.__change_str_to_float(line=line_data)
        return lines

    # Change data string to float
    def __change_str_to_float(self, line) -> list[float]:
        try:
            line = list(map(lambda string: float(string), line))
        except:
            print(line)
            raise Exception("We cannot change string to float in each data")
        return line


# 2nd Generation -> For "dump.lammpstrj"
class DumpOpener(Opener):
    from .tools import timeCount

    def __init__(self, file_path, target_info: list[str] = None) -> None:
        """Dump Opener

        Open the file, dump.lammpstrj and Get Database

        Args:
            file_path   (str)       :   file path of dump.lammpstrj
            target_info (list[str]) :   List with string, 0 = target_line, 1 = target_word

        """
        super().__init__(file_path)
        self.lines: list = super().get_lines()
        self.target_info = self.set_target_info(target_info=target_info)
        self.target_line: str = self.target_info[0]
        self.target_word: str = self.target_info[1]
        self.system_num: int = self.__get_system_num()
        self.start_idx_list: list[int] = self.__find_word_idx_list(
            word=self.target_line
        )

    # Get the database from a, b
    @timeCount
    def get_database(self) -> list:
        database: list = []
        for idx in self.start_idx_list:
            start_idx: int = idx + 1
            end_idx: int = start_idx + self.system_num
            lines = self.lines[start_idx:end_idx]
            lines = super().seperate_data_in_lines(lines=lines)
            database.append(lines)
        return database

    # Find the columns data in lines
    @timeCount
    def get_columns(self) -> list[str]:
        for line in self.lines:
            if self.target_line in line:
                columns = line.split(" ")
                columns = self.__remove_other(columns)
                return columns
        return []

    # find the system size
    @timeCount
    def get_system_size(self, dim=3, word="BOX") -> list[float]:
        size_idx = self.__find_word_idx(word=word) + 1
        system_size = self.lines[size_idx : size_idx + dim]
        system_size = super().seperate_data_in_lines(lines=system_size)
        return system_size

    # find the time step
    @timeCount
    def get_time_step(self) -> list[float]:
        time_step_idx_list = self.__find_word_idx_list(word="TIMESTEP")
        time_step_list = [int(self.lines[idx + 1]) for idx in time_step_idx_list]
        return time_step_list

    # Remove the word, ITEM:
    def __remove_other(self, line: list[str]) -> list[str]:
        if "ITEM:" in line:
            return line[2:]
        else:
            return line

    # find the idx list of start point
    def __find_word_idx_list(self, word: str) -> list[int]:
        idx_list = []
        for idx, line in enumerate(self.lines):
            if word in line:
                idx_list.append(idx)
        return idx_list

    # find the first idx
    def __find_word_idx(self, word: str) -> int:
        for idx, line in enumerate(self.lines):
            if word in line:
                return idx

    # Fine the system num
    def __get_system_num(self) -> int:
        for idx, line in enumerate(self.lines):
            if self.target_word in line:
                system_num = self.lines[idx + 1]
                system_num = int(system_num)
                return system_num
        return 0

    # Set target_information
    def set_target_info(self, target_info):
        if target_info == None:
            return ["id", "NUMBER"]
        else:
            assert len(target_info) != 2
            return target_info
