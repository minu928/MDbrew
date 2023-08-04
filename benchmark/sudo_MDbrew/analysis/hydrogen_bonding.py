import numpy as np
from ..spatial import PeriodicCKDTree, calculate_angle_between_vectors


def analyse_hydrogen_bonding(O_position, H_position, box):
    threshold_angle = 30.0
    threshold_distance = 1.2
    H_tree = PeriodicCKDTree(H_position, bounds=box)
    O_tree = PeriodicCKDTree(O_position, bounds=box)

    # Precompute the second O positions for each O atom
    second_O_list = O_tree.query_ball_point(O_position, r=3.5)

    # Constants for optimization
    INF_IDX = len(H_position)

    hydrogen_bonding_angle_list = []
    hydrogen_bonding_distance_list = []
    # Loop through O atoms and find corresponding H atoms
    for this_O_position, this_H2_idxes, second_O in zip(
        O_position, H_tree.query(O_position, k=3, p=2, distance_upper_bound=threshold_distance)[1], second_O_list
    ):
        vec1_arr = O_position[second_O] - this_O_position
        vec1_arr = vec1_arr[~np.all(vec1_arr == 0, axis=1)]
        vec2_arr = this_O_position - H_position[this_H2_idxes[this_H2_idxes != INF_IDX]]

        angles = calculate_angle_between_vectors(vec1_arr, vec2_arr)
        idx_of_hydrogen_bonding = np.where(angles < threshold_angle)
        dist = np.linalg.norm(vec1_arr[idx_of_hydrogen_bonding[0]])
        if dist:
            hydrogen_bonding_distance_list.append(dist)
            hydrogen_bonding_angle_list.append(angles[idx_of_hydrogen_bonding])
    return {"distance": np.array(hydrogen_bonding_distance_list), "angle": np.concatenate(hydrogen_bonding_angle_list)}
