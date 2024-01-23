import numpy as np
from mdbrew.tool.space import PeriodicCKDTree, apply_pbc, calculate_angle_between_vectors


def find_hydrogen_bonding(
    O_coords: np.ndarray,
    H_coords: np.ndarray,
    box: np.ndarray,
    *,
    donor_indexes=None,
    HOO_angle: float = 30.0,
    OO_distance: float = 3.5,
    rcut_OH: float = 1.25,
):
    donor_O_coords = O_coords if donor_indexes is None else O_coords[donor_indexes]
    near_O_indexes_from_O = PeriodicCKDTree(O_coords, bounds=box).query_ball_point(donor_O_coords, r=OO_distance)
    near_H_indexes_from_O = PeriodicCKDTree(H_coords, bounds=box).query_ball_point(donor_O_coords, r=rcut_OH)
    hydrogen_bonding_relation = np.zeros([len(donor_O_coords), len(O_coords)])
    for ith_from_O, (near_O_indexes, near_H_indexes) in enumerate(zip(near_O_indexes_from_O, near_H_indexes_from_O)):
        ith_from_O_coord = donor_O_coords[ith_from_O]
        for near_H in near_H_indexes:
            OH_vec1 = apply_pbc(H_coords[near_H] - ith_from_O_coord, box=box)
            for near_O in near_O_indexes:
                OH_vec2 = apply_pbc(O_coords[near_O] - ith_from_O_coord, box=box)
                if OH_vec2.all():
                    angle = calculate_angle_between_vectors(OH_vec1, OH_vec2)
                    if angle < HOO_angle:
                        assert hydrogen_bonding_relation[ith_from_O, near_O] == 0.0, f"One Donor OH contribute Two O.."
                        hydrogen_bonding_relation[ith_from_O, near_O] = near_H
    return hydrogen_bonding_relation


def get_HB_index_dict(hydrogen_bonding_relation):
    donnor_indexes, acceptor_indexes = np.where(hydrogen_bonding_relation != 0.0)
    return {"donor": donnor_indexes, "acceptor": acceptor_indexes}


def count_HB(hydrogen_bonding_relation, what=None):
    assert what in [None, "donor", "acceptor"], f"what should be in [None, 'donor', 'acceptor']"
    donor_numb, acceptor_numb = hydrogen_bonding_relation.shape
    HB_index_dict = get_HB_index_dict(hydrogen_bonding_relation)
    counted_HB_arr = np.zeros(donor_numb)
    for key, value in HB_index_dict.items():
        if what == None or key == what:
            indexes, counts = np.unique(value, return_counts=True)
            for index, count in zip(indexes, counts):
                counted_HB_arr[index] += count
    return counted_HB_arr
