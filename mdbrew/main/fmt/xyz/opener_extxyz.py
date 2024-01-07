import re
from mdbrew.main.interface import OpenerInterface


box_compiler = re.compile(
    r"Lattice=\"(?P<xx>\S+)\s+(?P<xy>\S+)\s+(?P<xz>\S+)\s+(?P<yx>\S+)\s+(?P<yy>\S+)\s+(?P<yz>\S+)\s+(?P<zx>\S+)\s+(?P<zy>\S+)\s+(?P<zz>\S+)"
)
col_matcher = re.compile(r"Properties=(?P<info>\S+)")


class extxyzOpener(OpenerInterface):
    fmt: str = "extxyz"

    def __init__(self, path: str, *args, **kwrgs) -> None:
        super().__init__(path, *args, **kwrgs)

    def _make_one_frame_data(self, file):
        first_loop_line = file.readline()
        atom_num = int(first_loop_line.strip())
        self.total_line_num = atom_num + 2
        info_line = file.readline()
        self.__update_information(info_line=info_line)
        return [file.readline().split() for _ in range(atom_num)]

    def __update_information(self, info_line: str):
        if not self.column:
            assert (box_idx := info_line.find("Lattice")) >= 0, "Properties should be included"
            assert (property_idx := info_line.find("Properties")) >= 0, "Properties should be included"
            box = re.match(box_compiler, info_line[box_idx:])
            self.box_size.extend([box["xx"], box["yy"], box["zz"]])
            properties = re.match(col_matcher, info_line[property_idx:])["info"]
            if "species" in properties:
                self.column.append("atom")
            if "pos" in properties:
                self.column.extend(["x", "y", "z"])
            if "force" in properties:
                self.column.extend(["fx", "fy", "fz"])
            if "vel" in properties:
                self.column.extend(["vx", "vy", "vz"])
