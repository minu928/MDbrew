from ..opener import Opener
from ..writer import Writer


class xyzOpener(Opener):
    def __init__(self, path: str, *args, **kwrgs) -> None:
        super().__init__(path, *args, **kwrgs)
        self.column = ["atom", "x", "y", "z"]
        super().gen_db()

    def _make_one_frame_data(self, file):
        first_loop_line = file.readline()
        atom_num = int(first_loop_line.split()[0])
        second_line = file.readline()
        self.total_line_num = atom_num + 2
        return [file.readline().split() for _ in range(atom_num)]


class xyzWriter(Writer):
    def __init__(self, path: str, brewery, **kwrgs) -> None:
        self._fmt = "xyz"
        super().__init__(path, brewery, **kwrgs)
        self.__atoms = self._brewery.brew(self._brewery._opener._atom_keyword, dtype=str, verbose=False)

    def _write_one_frame_data(self, file, idx):
        file.write(f"\t{self._brewery.atom_num}\n")
        file.write(f" i = {idx}\n")
        xyz = self._brewery.coords
        for atom, dat in zip(self.__atoms, xyz):
            if self._requied_atom_dict:
                atom = self._atom_dict[float(atom)]
            file.write(f"{atom:>3s} {dat[0]:15.10f} {dat[1]:15.10f} {dat[2]:15.10f}\n")
