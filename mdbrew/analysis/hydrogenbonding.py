import numpy as np
from mdbrew.tool.space import PeriodicCKDTree, apply_pbc, calculate_angle_between_vectors


__all__ = ["search_relation", "get_HB_index_dict", "count_HB"]


def search_relation(
    O_coords: np.ndarray,
    H_coords: np.ndarray,
    box: np.ndarray,
    *,
    donor_indexes=None,
    HOO_angle: float = 30.0,
    OO_distance: float = 3.5,
    rcut_OH: float = 1.20,
    dtype: str = "U16",
    return_acceptor: bool = False,
):
    donor_O_coords = O_coords if donor_indexes is None else O_coords[donor_indexes]
    O_ckdtree = PeriodicCKDTree(O_coords, bounds=box)
    H_ckdtree = PeriodicCKDTree(H_coords, bounds=box)
    hydrogenbonding_relation = np.empty([len(donor_O_coords), len(O_coords)], dtype=dtype)

    for ith_donor_O, (near_O_indexes, near_H_indexes) in enumerate(
        zip(O_ckdtree.query_ball_point(donor_O_coords, r=OO_distance), H_ckdtree.query_ball_point(donor_O_coords, r=rcut_OH))
    ):
        ith_donor_O_coords = donor_O_coords[ith_donor_O]
        OO_vec_arr = apply_pbc(O_coords[near_O_indexes] - ith_donor_O_coords, box=box)
        OH_vec_arr = apply_pbc(H_coords[near_H_indexes] - ith_donor_O_coords, box=box)
        # Delete Self Index
        is_not_self_index = np.all(OO_vec_arr != 0.0, axis=1)
        near_O_indexes = np.array(near_O_indexes)[is_not_self_index]
        OO_vec_arr = OO_vec_arr[is_not_self_index]
        # Loop the each H
        for ith, OH_vec in enumerate(OH_vec_arr):
            angle = calculate_angle_between_vectors(v1=OH_vec, v2=OO_vec_arr)
            hydrogenbonded_O_indexes = near_O_indexes[angle < HOO_angle]
            hydrogenbonded_H_indexes = near_H_indexes[ith]
            if hydrogenbonded_O_indexes.size:
                assert np.any(hydrogenbonding_relation[ith_donor_O, hydrogenbonded_O_indexes] == ""), f"One Donor OH to Two O"
                hydrogenbonding_relation[ith_donor_O, hydrogenbonded_O_indexes] = hydrogenbonded_H_indexes
    if return_acceptor and donor_indexes is not None:
        acceptor_relation = np.empty([len(donor_O_coords), len(O_coords)], dtype=dtype)
        near_O_indexes_list = O_ckdtree.query_ball_point(donor_O_coords, r=OO_distance)
        for ith_donor_O, near_O_indexes in enumerate(near_O_indexes_list):
            for ith_near_O, H_indices in zip(near_O_indexes, H_ckdtree.query_ball_point(O_coords[near_O_indexes], r=rcut_OH)):
                ith_near_O_coords = O_coords[ith_near_O]
                OO_vec = apply_pbc(donor_O_coords[ith_donor_O] - ith_near_O_coords, box=box)
                if np.all(OO_vec == 0):
                    continue
                OH_vec = apply_pbc(H_coords[H_indices] - ith_near_O_coords, box=box)
                angle = calculate_angle_between_vectors(OH_vec, OO_vec)
                hydrogenbonded_H_indices = np.array(H_indices)[angle < HOO_angle]
                if size := hydrogenbonded_H_indices.size:
                    assert size == 1, f"One Oxygen Gives Two H in One Oxygen"
                    acceptor_relation[ith_donor_O, ith_near_O] = hydrogenbonded_H_indices[0]
        return {"donor": hydrogenbonding_relation, "acceptor": acceptor_relation}
    return hydrogenbonding_relation


def get_HB_index_dict(hydrogen_bonding_relation):
    donnor_indexes, acceptor_indexes = np.where(hydrogen_bonding_relation != "")
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
