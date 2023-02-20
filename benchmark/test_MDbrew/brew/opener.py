from ..tool.timer import time_count
from abc import ABCMeta, abstractmethod
from typing import List

__all__ = ["Opener", "LAMMPSOpener", "DatOpener"]


# 1st Generation
class Opener(metaclass=ABCMeta):
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        self.lines = self._get_lines()

    # Open the file and delete all empty line
    def _get_lines(self) -> List[str]:
        with open(self.file_path) as file:
            return [line.strip() for line in file if line.strip()]

    # # find the idx list of start point
    def _find_idxlist_by_word(self, word: str) -> List[int]:
        return [idx for idx, line in enumerate(self.lines) if word in line]

    # find the first idx
    def _find_idx_by_word(self, word: str) -> int:
        for idx, line in enumerate(self.lines):
            if word in line:
                return idx

    # split data in line with overall lines
    @staticmethod
    def str_to_float_list(lines: List[str]) -> List[List[float]]:
        return [list(map(float, line.split())) for line in lines]

    @abstractmethod
    def get_database(self) -> List[List[List[float]]]:
        pass

    @abstractmethod
    def get_columns(self) -> List[str]:
        pass

    @abstractmethod
    def get_system_size(self) -> List[List[float]]:
        pass

    @abstractmethod
    def get_time_step(self) -> List[int]:
        pass


# 2nd Generation -> For "dump.lammpstrj"
class LAMMPSOpener(Opener):
    def __init__(self, file_path: str, target_info: List[str] = None):
        """Dump Opener

        Open the file, dump.lammpstrj and Get Database

        Parameters
        ----------
        file_path : str
            file path of dump.lammpstrj
        target_info : list[str]
            List with string, target_line = "id", target_word = "NUMBER"

        Examples
        --------
        >>> opener      = LAMMPSOpener(file_path)
        >>> database    = opener.get_database
        >>> columns     = opener.get_columns
        >>> system_size = opener.get_system_size
        >>> time_step   = opener.get_time_step
        """
        super().__init__(file_path)
        target_info = ["id", "NUMBER"] if target_info is None else target_info
        self.system_num = int(self.lines[super()._find_idx_by_word(target_info[1]) + 1])
        self.start_idx_list: list[int] = super()._find_idxlist_by_word(target_info[0])

    # Get the database from a, b
    @time_count
    def get_database(self) -> List[List[List[float]]]:
        database: List[List[List[float]]] = []
        for idx in self.start_idx_list:
            lines = self.lines[idx + 1 : idx + 1 + self.system_num]
            lines = super().str_to_float_list(lines=lines)
            database.append(lines)
        return database

    # Find the columns data in lines
    @time_count
    def get_columns(self, erase_appendix: int = 2) -> List[str]:
        column_idx: int = self.start_idx_list[0]
        return self.lines[column_idx].split(" ")[erase_appendix:]

    # find the system size
    @time_count
    def get_system_size(self, dim: int = 3, word: str = "BOX") -> List[float]:
        size_idx = self._find_idx_by_word(word=word) + 1
        system_size = super().lines[size_idx : size_idx + dim]
        system_size = super().str_to_float_list(lines=system_size)
        return system_size

    # find the time step
    @time_count
    def get_time_step(self, word: str = "TIMESTEP") -> List[float]:
        time_step_idxlist = super()._find_idxlist_by_word(word=word)
        time_step_list = [int(super().lines[idx + 1]) for idx in time_step_idxlist]
        return time_step_list


# 2nd Generation -> For ""
class DatOpener(Opener):
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)

    def get_columns(self, column_idx: int = 1, erase_que: int = 1) -> List[str]:
        return self.lines[column_idx].split()[erase_que:]

    def get_database(self, erase_que: int = 2) -> List[str]:
        return super().str_to_float_list(self.lines[erase_que:])

    def get_system_size(self) -> List[float]:
        return len(self.lines)

    def get_time_step(self, erase_que: int = 2) -> List[float]:
        return [int(line.split()[0]) for line in self.lines[erase_que:]]
