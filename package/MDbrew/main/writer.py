from tqdm import tqdm
from abc import abstractmethod
from ..tool.colorfont import color


class Writer(object):
    _save_path = None
    _fmt = None

    def __init__(self, path: str, brewery) -> None:
        self._save_path = path
        self._brewery = brewery
        self._print_option = f"[ {color.font_cyan}BREW{color.reset} ]  #WRITE {color.font_yellow}{self._brewery._fmt}->{self._fmt} {color.reset}"

    def write(self, start, end, step):
        frange = self._brewery.frange(start=start, end=end, step=step)
        with open(self._save_path, "w+") as f:
            for i in tqdm(frange, desc=self._print_option):
                self._write_one_frame_data(file=f, idx=i)

    @abstractmethod
    def _write_one_frame_data(self, file, idx):
        pass
