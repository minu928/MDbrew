from typing import TextIO
from mdbrew.main.interface import WriterInterface


class lmpWriter(WriterInterface):
    fmt = "lmps"

    def _write_one_frame_data(self, file: TextIO, idx: int):
        lines = []
        title_line = f"Atom Count: "
        title_line += " ".join([f"{atom}:{num}" for atom, num in zip(self._brewery.atom_info[0], self._brewery.atom_info[1])])
        lines.append(title_line)
        lines.append("")
        lines.append(f"{self._brewery.atom_num} atoms")
        lines.append(f"{len(self._brewery.atom_kind)} atom types")
        lines.append("")
        for box, axis in zip(self._brewery.box_size, ["x", "y", "z"]):
            lines.append(f"0 {box} {axis}lo {axis}hi")
        lines.append("")
        lines.append("Atoms # atomic")
        lines.append("")
        type_list = self.__make_type_list()
        coords = self._brewery.coords * self._scaling
        for i, coords in enumerate(coords):
            lines.append(f"{i + 1} {type_list[i]} {coords[0]} {coords[1]} {coords[2]}")
        # write the file at once
        file.writelines("\n".join(lines))

    def _check_require_atom_dict(self):
        return self._brewery.fmt != "lammpstrj"

    def __make_type_list(self):
        if "lammpstrj" == self._brewery.fmt:
            return self._brewery.atoms
        inverse_atom_dict = {str(atom): int(idx) for idx, atom in self._atom_dict.items()}
        return [inverse_atom_dict[atom] for atom in self._brewery.atoms]
