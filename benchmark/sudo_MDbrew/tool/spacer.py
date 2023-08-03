import numpy as np

__all__ = ["check_dimension", "get_diff_position", "get_distance", "wrap_position", "unwrap_position"]


# Dimension checker
def check_dimension(array, dim: int, dtype: str = float):
    new_array = np.asarray(array, dtype=dtype)
    assert new_array.ndim == dim, "[DimensionError] Check your dimension "
    return new_array


# get difference of position A & B
def get_diff_position(a_position, b_position, dtype: str = float):
    return np.subtract(a_position, b_position, dtype=dtype)


# get distance from difference position
def get_distance(diff_position, axis: int = -1, dtype: str = float):
    return np.sqrt(np.sum(np.square(diff_position), axis=axis)).astype(dtype)


# wrap the position data
def wrap_position(position, box):
    box = np.asarray(box, dtype=float)
    position = np.where(position > box, position - box, position)
    position = np.where(position < 0, position + box, position)
    return position


# unwrap the position data
def unwrap_position(position, pre_postion, box):
    box = np.asarray(box, dtype=float)
    delta_position = position - pre_postion
    position = np.where(delta_position < box * 0.5, position + box, position)
    position = np.where(delta_position > box * 0.5, position - box, position)
    return position
