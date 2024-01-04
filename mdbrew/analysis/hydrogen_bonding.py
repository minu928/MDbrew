import numpy as np
from mdbrew.tool.space import PeriodicCKDTree, calculate_angle_between_vectors, apply_pbc


__all__ = ["search_in_H2O", "distribute_OHn"]


def search_in_H2O(O_position, H_position, box, hb_angle: float = 30.0, hb_distance: float = 3.5, OH_n: int = 2):
    idxes_O_in_H = PeriodicCKDTree(H_position, bounds=box).query(O_position, k=3, distance_upper_bound=1.25)[1]
    idxes_O_in_O = PeriodicCKDTree(O_position, bounds=box).query_ball_point(O_position, r=hb_distance)
    assert OH_n in [1, 2, 3], ValueError(f"Something is Wrong..., OH_n should be in [1, 2, 3] not {OH_n}")
    if OH_n in [1, 3]:
        raise AttributeError(f"Sorry, we are not supported {OH_n} case yet..")
    elif OH_n == 2:
        hydrogen_bonding_donor_list = []
        O_idxes = distribute_OHn(idxes_O_in_H=idxes_O_in_H)[OH_n]
        H2_position_in_H2O = H_position[idxes_O_in_H[:, :OH_n]]  # [N_O, 2, 3]
        O_position_in_H2O = O_position[O_idxes][:, None, :]
        OH_vec = apply_pbc(H2_position_in_H2O - O_position_in_H2O, box)
        for this_O_idx, idxes_O in enumerate(idxes_O_in_O):
            idxes_O = np.array(idxes_O)
            idxes_O = idxes_O[np.where(idxes_O != this_O_idx)]
            OO_vec = apply_pbc(O_position[idxes_O] - O_position[this_O_idx], box)
            this_H_connected_with_other_O = []
            for i in range(OH_n):
                thi_OH_vec = OH_vec[this_O_idx, i, :]
                anlge_one = calculate_angle_between_vectors(OO_vec, thi_OH_vec)
                this_H_connected_with_other_O.append(idxes_O[np.where((anlge_one <= hb_angle) & (anlge_one >= 0))])
            hydrogen_bonding_donor_list.append(np.concatenate(this_H_connected_with_other_O))
        return hydrogen_bonding_donor_list


def distribute_OHn(idxes_O_in_H):
    """
    is water is a OHn?

    Args:
        idxes_O_in_H (NDArray): [[0, 1, 125], ... , ] [125, 3]

    Returns:
        Dict[1 : [], 2: [], 3:[]] : Dictionary for each 1, 2, 3 means that n of OH_n
    """
    max_idx_num = np.max(idxes_O_in_H)
    OHn_list = {1: [], 2: [], 3: []}
    for i, idxes in enumerate(idxes_O_in_H):
        idx, num = np.unique(idxes, return_counts=True)
        key = num[idx == max_idx_num]
        n = int(3 - key)
        assert n >= 0, ValueError("Something is wrong of n")
        OHn_list[n].append(i)
    return OHn_list


def count_hydrogen_bonding_from_donor(donor_idx_arr):
    acceptor_idx, acceptor_num = np.unique(np.concatenate(donor_idx_arr), return_counts=True)
    donor_num_arr = np.array([len(i) for i in donor_idx_arr])
    donor_num_arr[acceptor_idx] += acceptor_num
    return donor_num_arr
