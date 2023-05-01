#!/usr/bin/env python3
import numpy as np
from tqdm import tqdm
from scipy import constants
from ..brewery import Brewery
from ..tool.colorfont import color
from ..tool.decorator import color_print


class BrewCP2K(object):
    tqmd_option = {"ascii": " #"}
    printing_option = {
        "2array": f" #CONVERT  {color.font_yellow}List2Array{color.reset}",
        "2a.u": f" #CONVERT  {color.font_yellow}Atomic Unit{color.reset}",
        "save": f" #SAVE  {color.font_yellow}THE DATA{color.reset}",
        "kind2type": f" #CONVERT  {color.font_yellow}KIND2TYPE{color.reset}",
    }

    def __init__(self, xyz_file, log_file, type_map: list["str"]) -> None:
        self._type_map = type_map
        self._brew_xyzfile(xyz_file=xyz_file)
        self._brew_logfile(log_file=log_file)
        self.__error__()
        self._covert_kind2type()
        self._change2array()
        self._convert_unit()

    @property
    def virials(self):
        return self._virial_list

    @property
    def forces(self):
        return self._force_list

    @property
    def coords(self):
        return self._coord_list

    @property
    def cells(self):
        return self._cell_list

    @property
    def energies(self):
        return self._energy_list

    @property
    def types(self):
        return self._type_list

    @property
    def type_dict(self):
        return self._type_dict

    def __str__(self) -> str:
        LINE_WIDTH = 60
        sep_line = "=" * LINE_WIDTH
        print("")
        print(sep_line)
        print("||" + " " * 22 + " INFO " + " " * 28 + "||")
        print(sep_line)
        print(f"\t[  CELL  ] : {self.is_contain_cell} || SHAPE {self.cells.shape}")
        print(f"\t[ FORCES ] : {self.is_contain_force} || SHAPE {self.forces.shape}")
        print(f"\t[ VIRIAL ] : {self.is_contain_stress} || SHAPE {self.virials.shape}")
        print(f"\t[ COORDS ] : {self.is_contain_coord} || SHAPE {self.coords.shape}")
        print(f"\t[ ENERGY ] : {self.is_contain_energy} || SHAPE {self.energies.shape}")
        print(sep_line)
        return f"\t @CopyRight by  {color.font_blue}minu928@snu.ac.kr{color.reset}\n"

    def __error__(self):
        F_energy = len(self._energy_list)
        F_stress = len(self._stress_list) / 3
        F_coords = len(self._coord_list)
        assert (
            F_energy == F_stress == F_coords
        ), f"Frame of Energy {F_energy}, Frame of Stress {F_stress} , Frame of Coords {F_coords}"
        self._num_frame = F_energy
        self._num_atom = len(self._force_list) / F_energy

    @color_print(name=printing_option["save"])
    def save_data(self, folder: str = "./", mode: str = "dpdata"):
        folder = folder if folder[-1] == "/" else folder + "/"
        mode_list = ["dpdata", "raw"]
        mode = mode.lower()
        assert mode in mode_list, f"[ ERROR ] mode should be dpata, raw || Not {mode}"
        if mode == "dpdata":
            np.save(folder + "energy.npy", self.energies)
            np.save(folder + "box.npy", self.cells.reshape(self._num_frame, 9))
            np.save(folder + "virial.npy", self.virials.reshape(self._num_frame, 9))
            np.save(
                folder + "force.npy",
                self.forces.reshape(self._num_frame, int(self._num_atom * 3)),
            )
            np.save(
                folder + "coord.npy",
                self.coords.reshape(self._num_frame, int(self._num_atom * 3)),
            )
        elif mode == "raw":
            np.save(folder + "energy.npy", self.energies)
            np.save(folder + "virial.npy", self.virials)
            np.save(folder + "force.npy", self.forces)
            np.save(folder + "coord.npy", self.coords)
            np.save(folder + "box.npy", self.cells)
        np.savetxt(folder + "type.raw", self.types, fmt="%d")
        np.savetxt(folder + "type_map.raw", self._type_map, fmt="%s")

    def _brew_xyzfile(self, xyz_file):
        xyz_brewer = Brewery(path=xyz_file).brew(cols=["x", "y", "z"], dtype="float64")
        line_range = tqdm(
            xyz_brewer,
            desc=f"[ {color.font_cyan}BREW{color.reset} ]  #{color.font_green}XYZ{color.reset} ",
            **self.tqmd_option,
        )
        self._coord_list = [data for data in line_range]
        self.is_contain_coord = True

    def _brew_logfile(self, log_file):
        # BASE for brewing
        ## CELL
        cell_keyword = "CELL| Vector "
        self.is_contain_cell = False
        self._cell_list = []
        ## STRESS
        stress_keyword = "STRESS| Analytical stress"
        self.is_contain_stress = False
        self._stress_list = []
        ## ENERGY
        energy_keyword = "ENERGY|"
        self.is_contain_energy = False
        self._energy_list = []
        ## FORCE
        force_keyword = " Atom   Kind "
        self.is_contain_force = False
        self._force_list = []
        force_stop_keyword = "SUM OF ATOMIC FORCES"
        force_iter_on = False
        ## KIND
        kind_keyword = " Atom  Kind "
        self.is_contain_kind = False
        self._kind_list = []
        kind_stop_keyword = "\n"
        kind_iter_on = False
        # ITERATION
        with open(log_file, "r") as f:
            line_range = enumerate(
                tqdm(
                    f,
                    **self.tqmd_option,
                    desc=f"[ {color.font_cyan}BREW{color.reset} ]  #{color.font_green}LOG{color.reset} ",
                )
            )
            for idx, line in line_range:
                # CELL
                if len(self._cell_list) < 3:
                    if cell_keyword in line:
                        self.is_contain_cell = True
                        self._cell_list.append(line.split()[4:7])
                        continue
                # STRESS
                if stress_keyword in line:
                    self.is_contain_stress = True
                    stress_idx = idx
                if self.is_contain_stress and stress_idx + 5 > idx > stress_idx + 1:
                    self._stress_list.append(line.split()[2:5])
                    continue
                # ENERGY
                if energy_keyword in line:
                    self.is_contain_energy = True
                    self._energy_list.append(line.split()[8])
                    continue
                # FORCE
                if force_keyword in line:
                    force_idx = idx
                    self.is_contain_force = True
                    force_iter_on = True
                    continue
                if force_stop_keyword in line:
                    force_iter_on = False
                if force_iter_on and idx > force_idx:
                    self._force_list.append(line.split()[3:6])
                    continue
                # TYPE
                if kind_keyword in line:
                    kind_idx = idx
                    self.is_contain_kind = True
                    kind_iter_on = True
                    continue
                if kind_iter_on and kind_stop_keyword == line:
                    kind_iter_on = False
                if kind_iter_on and idx > kind_idx:
                    self._kind_list.append(line.split()[2])
                    continue

    @color_print(name=printing_option["2array"])
    def _change2array(self, data_type: str = "float32"):
        F = int(self._num_frame)
        N = int(self._num_atom)
        self._stress_list = np.array(self._stress_list).astype(data_type).reshape(F, 3, 3)
        self._force_list = np.array(self._force_list).astype(data_type).reshape(F, N, 3)
        self._cell_list = np.tile(self._cell_list, (self._num_frame, 1)).astype(data_type).reshape(F, 3, 3)
        self._energy_list = np.array(self._energy_list).astype(data_type)
        self._coord_list = np.array(self._coord_list).astype(data_type)
        self._type_list = np.array(self._type_list).astype("int32")

    @color_print(name=printing_option["2a.u"])
    def _convert_unit(self):
        ELE_CHG = constants.elementary_charge  # Elementary Charge, in C
        HARTREE = constants.value("atomic unit of energy")  # Hartree, in Jole
        BOHR = constants.value("atomic unit of length")  # Bohr, in m

        eV = ELE_CHG  # eV
        hatree2eV = HARTREE / ELE_CHG  # eV
        J2eV = 1  # eV

        angstrom = 1  # angstrom
        m2angstrom = 1e-10 * angstrom  # angstrom
        bohr2angstrom = BOHR / m2angstrom  # angstrom
        GPa2eVangstorm = 1e-9 * J2eV / (m2angstrom**3) * eV  # eV / angstrom^3

        self._energy_list *= hatree2eV
        self._cell_list = self._cell_list
        self._force_list *= hatree2eV / bohr2angstrom
        volume = np.linalg.det(self._cell_list[0])
        self._virial_list = self._stress_list * volume / GPa2eVangstorm
        self._coord_list = self._coord_list

    @color_print(name=printing_option["kind2type"])
    def _covert_kind2type(self):
        self._type_dict = {kind: idx for idx, kind in enumerate(self._type_map)}
        self._type_list = [self._type_dict[kind] for kind in self._kind_list]
