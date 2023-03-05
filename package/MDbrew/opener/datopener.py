from typing import List
from .opener import Opener


# 2nd Generation -> For ""
class DATOpener(Opener):
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
