from typing import List
from .opener import Opener


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
        self.system_num = int(self.lines[super().find_idx_by_word(target_info[1]) + 1])
        self.start_idx_list: list[int] = super().find_idxlist_by_word(target_info[0])

    def get_database(self) -> List[List[List[float]]]:
        database: List[List[List[float]]] = []
        for idx in self.start_idx_list:
            lines = self.lines[idx + 1 : idx + 1 + self.system_num]
            lines = super().str_to_float_list(lines=lines)
            database.append(lines)
        return database

    def get_columns(self, erase_appendix: int = 2) -> List[str]:
        column_idx: int = self.start_idx_list[0]
        return self.lines[column_idx].split(" ")[erase_appendix:]

    def get_system_size(self, dim: int = 3, word: str = "BOX") -> List[float]:
        size_idx = super().find_idx_by_word(word=word) + 1
        system_size = self.lines[size_idx : size_idx + dim]
        system_size = super().str_to_float_list(lines=system_size)
        return system_size

    def get_time_step(self, word: str = "TIMESTEP") -> List[float]:
        time_step_idxlist = super().find_idxlist_by_word(word=word)
        time_step_list = [int(self.lines[idx + 1]) for idx in time_step_idxlist]
        return time_step_list
