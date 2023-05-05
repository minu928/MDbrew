import numpy as np

__all__ = ["check_dimension", "get_diff_position", "get_distance"]


# Dimension checker
def check_dimension(array, dim: int):
    new_array = np.asarray(array, dtype=np.float64)
    assert new_array.ndim == dim, "[DimensionError] Check your dimension "
    return new_array


# get difference of position A & B
def get_diff_position(a_position, b_position):
    return np.subtract(a_position, b_position, dtype=np.float64)


# get distance from difference position
def get_distance(diff_position, axis: int = -1):
    return np.sqrt(np.sum(np.square(diff_position), axis=axis))
