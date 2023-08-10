import numpy as np

__all__ = [
    "check_dimension",
    "calculate_diff_position",
    "calculate_distance",
    "wrap_position",
    "unwrap_position",
    "calculate_angle_between_vectors",
    "apply_pbc",
]


# Dimension checker
def check_dimension(array, dim: int, dtype: str = float):
    new_array = np.asarray(array, dtype=dtype)
    assert new_array.ndim == dim, "[DimensionError] Check your dimension "
    return new_array


# get difference of position A & B
def calculate_diff_position(a_position, b_position, dtype: str = float):
    return np.subtract(a_position, b_position, dtype=dtype)


# get distance from difference position
def calculate_distance(diff_position, axis: int = -1, dtype: str = float):
    return np.sqrt(np.sum(np.square(diff_position), axis=axis)).astype(dtype)


# calculate the angle between vectors
def calculate_angle_between_vectors(v1, v2):
    dot_product = np.sum(v1 * v2, axis=-1)
    norm_v1 = np.linalg.norm(v1, axis=-1)
    norm_v2 = np.linalg.norm(v2, axis=-1)
    return np.arccos(dot_product / (norm_v1 * norm_v2)) * 180.0 / np.pi


# wrap the position data
def wrap_position(position, box):
    box = np.asarray(box, dtype=float)
    position = np.where(position > box, position - box, position)
    position = np.where(position < 0, position + box, position)
    return position


# unwrap the position data
def unwrap_position(position, pre_position, box, ixyz=None, return_ixyz=False):
    box = np.asarray(box, dtype=float)
    if ixyz is None:
        ixyz = np.zeros(position.shape)

    delta_position = position - pre_position
    ixyz += np.where(delta_position < -box * 0.5, 1, 0)
    ixyz -= np.where(delta_position > box * 0.5, 1, 0)
    unwrapped_position = position + ixyz * box

    if return_ixyz:
        return unwrapped_position, ixyz
    else:
        return unwrapped_position


# do pbc
def apply_pbc(diff_position, box):
    box = np.array(box, dtype=float)
    diff_position = np.where(diff_position > box * 0.5, diff_position - box, diff_position)
    diff_position = np.where(diff_position < -box * 0.5, diff_position + box, diff_position)
    return diff_position
