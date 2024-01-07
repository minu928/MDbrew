import numpy as np
from collections import defaultdict
from typing import Type
from mdbrew.main.brewery import Brewery
from mdbrew.analysis.atom import atom2mass


def make_centerofmass_data(brewery: Type[Brewery], what=["x", "y", "z"], custom2default=None):
    assert len(what) == 3
    # Cluster the Residue
    residues_masses = defaultdict(list)
    residues_data = defaultdict(list)
    columns = ["resid", "atom"]
    columns.extend(what)
    atoms_in_resname = brewery.brew(cols=columns)
    for resid, atom, *data in atoms_in_resname:
        mass = atom2mass[mass] if custom2default is None else atom2mass[custom2default[atom]]
        residues_masses[resid].append(mass)
        residues_data[resid].append(np.array(data, dtype=float))
    # Make Center of mass
    residues_centerofmass = {}
    for resname in residues_masses.keys():
        masses = np.array(residues_masses[resname])
        xyz = np.array(residues_data[resname])
        centerofmass_xyz = np.sum(masses[:, None] * xyz, axis=0) / np.sum(masses)
        residues_centerofmass[resname] = centerofmass_xyz
    return residues_centerofmass
