from typing import List
from abc import ABCMeta, abstractmethod

__all__ = ["Opener"]


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
    def find_idxlist_by_word(self, word: str) -> List[int]:
        return [idx for idx, line in enumerate(self.lines) if word in line]

    # find the first idx
    def find_idx_by_word(self, word: str) -> int:
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
