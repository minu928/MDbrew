import numpy as np
from mdbrew.main.interface import WriterInterface


class POSCARWriter(WriterInterface):
    fmt: str = "POSCAR"

    def _write_one_frame_data(self, file, idx):
        atom_list = self._brewery.atom_kind
        atom_list = [self._atom_dict[int(float(kind))] for kind in atom_list] if self._required_atom_dict else atom_list
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
        xyz_arr = self._sort_xyz() * self._scaling
        for xyz in xyz_arr:
            file.write(f"{xyz[0]:24.16f}{xyz[1]:24.16f}{xyz[2]:24.16f}\n")

    def _sort_xyz(self):
        atom_list = self._brewery.brew(self._brewery.opener.atom_keyword, dtype="str")
        sorted_xyz = np.zeros((1, 3), dtype="float")
        for atom in self._brewery.atom_kind:
            atom_idx = np.where(atom == atom_list)
            sorted_xyz = np.concatenate((sorted_xyz, self._brewery.coords[atom_idx]))
        return sorted_xyz[1:]
