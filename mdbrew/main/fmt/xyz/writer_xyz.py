from mdbrew.main.interface import WriterInterface


class xyzWriter(WriterInterface):
    fmt = "xyz"

    def __init__(self, path: str, brewery, scaling: float = 1, **kwrgs) -> None:
        super().__init__(path, brewery, scaling, **kwrgs)

    def _write_one_frame_data(self, file, idx):
        file.write(f"\t{self._brewery.atom_num}\n")
        file.write(f" i = {idx}\n")
        xyz = self._brewery.coords * self._scaling
        for atom, dat in zip(self._brewery.atoms, xyz):
            if self._required_atom_dict:
                atom = self._atom_dict[float(atom)]
            file.write(f"{atom:>3s} {dat[0]:15.10f} {dat[1]:15.10f} {dat[2]:15.10f}\n")
