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


# 2nd Generation -> For "data.lammps"
class DataOpener(Opener):
    def __init__(self, file_path, target_info: list) -> None:
        super().__init__(file_path=file_path)
        self.lines = super().get_lines()
        self.target_line = target_info[0]
        self.target_word = target_info[1]
        self.target_column = target_info[2]

        self.system_num = self.__get_target_word_num()

    # main function
    def get_database(self) -> list:
        """Get Database

        function for get the full data

        Returns:
            list : full data of Instatance
        """
        idx_first_line = self.__find_index() + 1
        idx_last_line = idx_first_line + self.system_num
        lines = self.lines[idx_first_line:idx_last_line]
        lines = super().seperate_data_in_lines(lines=lines)
        print(f"{self.target_line} data is generated !! ")
        return lines

    # Find out the # of atoms, bonds, angles, dihedrals, impropes, ...
    def __get_target_word_num(self):
        for line in self.lines:
            if self.target_word in line:
                num = line.split(" ")
                return int(num[0])
        return 0

    # Find the index of target_line for check the starting point of target data in lines
    def __find_index(self) -> int:
        for idx, line in enumerate(self.lines):
            if self.target_line in line:
                return idx
        print(f"{self.target_word} is not included in the {self.file_path}")
        return 0

    # User can attach this data for get the column
    def get_columns(self) -> list:
        return self.target_column


class _TargetInfo:
    # Class for send the information about target (atoms, velocity, bonds, angles, ...)
    def __init__(self, target_line, target_word, target_column) -> None:
        self.target_line = target_line
        self.target_word = target_word
        self.target_column = target_column

    # Send the information about targe
    def _get_target_info(self):
        return [self.target_line, self.target_word, self.target_column]


# Below Class is for System
class Atoms(DataOpener, _TargetInfo):
    def __init__(self, file_path) -> None:
        _TargetInfo.__init__(
            self,
            target_line="Atoms",
            target_word="atoms",
            target_column=[
                "id",
                "molecule-tag",
                "atom-type",
                "q",
                "x",
                "y",
                "z",
                "nx",
                "ny",
                "nz",
            ],
        )
        DataOpener.__init__(
            self, file_path=file_path, target_info=_TargetInfo._get_target_info(self)
        )


class Velocity(DataOpener, _TargetInfo):
    def __init__(self, file_path) -> None:
        _TargetInfo.__init__(
            self,
            target_line="Velocities",
            target_word="atoms",
            target_column=["id", "vx", "vy", "vz"],
        )
        DataOpener.__init__(
            self, file_path=file_path, target_info=_TargetInfo._get_target_info(self)
        )


class Bonds(DataOpener, _TargetInfo):
    def __init__(self, file_path) -> None:
        _TargetInfo.__init__(
            self,
            target_line="Bonds",
            target_word="bonds",
            target_column=["id", "bond-type", "atom-1", "atom-2"],
        )
        DataOpener.__init__(
            self, file_path=file_path, target_info=_TargetInfo._get_target_info(self)
        )


class Angles(DataOpener, _TargetInfo):
    def __init__(self, file_path) -> None:
        _TargetInfo.__init__(
            self,
            target_line="Angles",
            target_word="angles",
            target_column=["id", "angle-type", "atom-1", "atom-2", "atom-3"],
        )
        DataOpener.__init__(
            self, file_path=file_path, target_info=_TargetInfo._get_target_info(self)
        )


class Dihedrals(DataOpener, _TargetInfo):
    def __init__(self, file_path) -> None:
        _TargetInfo.__init__(
            self,
            target_line="Dihedrals",
            target_word="dihedrals",
            target_column=[
                "id",
                "dihedral-type",
                "atom-1",
                "atom-2",
                "atom-3",
                "atom-4",
            ],
        )
        DataOpener.__init__(
            self, file_path=file_path, target_info=_TargetInfo._get_target_info(self)
        )


class Impropers(DataOpener, _TargetInfo):
    def __init__(self, file_path) -> None:
        _TargetInfo.__init__(
            self,
            target_line="Impropers",
            target_word="impropers",
            target_column=["id", "angle-type", "atom-1", "atom-2", "atom-3", "atom-4"],
        )
        DataOpener.__init__(
            self, file_path=file_path, target_info=_TargetInfo._get_target_info(self)
        )


# 2nd Generation -> For "dump.lammpstrj"
class DumpOpener(Opener):
    def __init__(self, file_path, target_info: list[str] = ["id", "NUMBER"]) -> None:
        """Dump Opener

        Open the file, dump.lammpstrj and Get Database

        Args:
            file_path   (str)       :   file path of dump.lammpstrj
            target_info (list[str]) :   List with string, 0 = target_line, 1 = target_word

        """
        super().__init__(file_path)
        self.lines: list = super().get_lines()
        self.target_line: str = target_info[0]
        self.target_word: str = target_info[1]
        self.system_num: int = self.__get_system_num()
        self.start_idx_list: list[int] = self.__find_word_idx_list(
            word=self.target_line
        )

    # Get the database from a, b
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
    def get_columns(self) -> list[str]:
        for line in self.lines:
            if self.target_line in line:
                columns = line.split(" ")
                columns = self.__remove_other(columns)
                return columns
        return []

    # find the system size
    def get_system_size(self, dim=3, word="BOX") -> list[float]:
        size_idx = self.__find_word_idx(word=word) + 1
        system_size = self.lines[size_idx : size_idx + dim]
        system_size = super().seperate_data_in_lines(lines=system_size)
        return system_size

    # find the time step
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
