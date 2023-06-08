import numpy as np
from ..opener import Opener
from ..writer import Writer


class vaspOpener(Opener):
    def __init__(self, path: str, *args, **kwrgs) -> None:
        super().__init__(path, *args, **kwrgs)
        self.skip_head = 7
        self.column = ["atom", "x", "y", "z"]
        self._set_box_and_atom(path=path)
        super().gen_db()

    def _make_one_frame_data(self, file):
        first_loop_line = file.readline()
        step = first_loop_line.split()[-1]
        num_atom = sum(self.atom_kind_num)
        self.total_line_num = num_atom + 1
        database = []
        c_atom_num = 0
        pointer = 0
        for _ in range(num_atom):
            if c_atom_num >= self.atom_kind_num[pointer]:
                pointer += 1
                c_atom_num = 0
            c_atom_num += 1
            line = [self.atom_kind[pointer]]
            line.extend(file.readline().split())
            database.append(line)
        return database

    def _set_box_and_atom(self, path):
        with open(path, "r") as raw_file:
            for i in range(2):
                raw_file.readline()
            for i in range(3):
                line = raw_file.readline().split()
                box_size = float(line[i])
                self.box_size.append(box_size)
            self.atom_kind = raw_file.readline().split()
            self.atom_kind_num = [int(data) for data in raw_file.readline().split()]


class POSCARWriter(Writer):
    _fmt = "POSCAR"

    def __init__(self, path: str, brewery, **kwrgs) -> None:
        super().__init__(path, brewery, **kwrgs)

    def _write_one_frame_data(self, file, idx):
        atom_list = self._brewery.atom_kind
        atom_list = [self._atom_dict[int(float(kind))] for kind in atom_list] if self._requied_atom_dict else atom_list
        file.write(" ".join(atom_list) + "\n")
        file.write(f" {1.0:15.10f}\n")
        file.write(f"\t{self._brewery.box_size[0]:15.10f}{0.0:15.10f}{0.0:15.10f}\n")
        file.write(f"\t{0.0:15.10f}{self._brewery.box_size[1]:15.10f}{0.0:15.10f}\n")
        file.write(f"\t{0.0:15.10f}{0.0:15.10f}{self._brewery.box_size[2]:15.10f}\n")
        for i in atom_list:
            file.write(f" {i:3s}")
        file.write("\n")
        for i in self._brewery.atom_info[1]:
            file.write(f"{i:6d}")
        file.write("\n")
        file.write("Cartesian\n")
        xyz_arr = self._sort_xyz()
        for xyz in xyz_arr:
            file.write(f"{xyz[0]:24.16f}{xyz[1]:24.16f}{xyz[2]:24.16f}\n")

    def _sort_xyz(self):
        atom_list = self._brewery.brew(self._brewery._opener._atom_keyword, dtype="str")
        sorted_xyz = np.zeros((1, 3), dtype="float")
        for atom in self._brewery.atom_kind:
            atom_idx = np.where(atom == atom_list)
            sorted_xyz = np.concatenate((sorted_xyz, self._brewery.coords[atom_idx]))
        return sorted_xyz[1:]
