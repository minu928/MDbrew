from typing import Dict, Type
from abc import abstractmethod, abstractproperty, ABCMeta
from tqdm import tqdm
from mdbrew.tool.colorfont import color


class WriterInterface(metaclass=ABCMeta):
    _save_path = None
    _fmt = None
    _out_name = None

    def __init__(self, path: str, brewery, **kwrgs) -> None:
        self._save_path = path
        self._brewery = brewery
        self._print_option = (
            f"[ {color.font_cyan}BREW{color.reset} ]  #WRITE {color.font_yellow}{self._brewery.fmt}->{self.fmt} {color.reset}"
        )
        self._atom_dict = kwrgs.pop("atom_dict", None)
        self._required_atom_dict = self._check_require_atom_dict()

        self.__error__()

    def __init_subclass__(cls) -> None:
        name = cls.__module__.split(".")[-1].lower()
        writer_programs[name] = cls

    def write(self, start, end, step):
        frange = self._brewery.frange(start=start, end=end, step=step)
        with open(self._save_path, "w+") as f:
            for i in tqdm(frange, desc=self._print_option):
                self._write_one_frame_data(file=f, idx=i)

    @abstractproperty
    def fmt(self) -> str:
        pass

    @abstractmethod
    def _write_one_frame_data(self, file, idx):
        pass

    def __error__(self):
        self._check_atom_dict()

    def _check_require_atom_dict(self):
        require_list = ["lmps"]
        return True if self._brewery.fmt in require_list else False

    def _check_atom_dict(self):
        if self._required_atom_dict and self._atom_dict is None:
            raise ValueError("Please input atom_dict, Ex {1 : 'Al'}")


writer_programs: Dict[str, Type[WriterInterface]] = {}