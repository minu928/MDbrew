import numpy as np

__all__ = ["check_dimension", "get_diff_position", "get_distance"]


# Dimension checker
def check_dimension(array, dim: int, dtype :str = "float32"):
    new_array = np.asarray(array, dtype=dtype)
    assert new_array.ndim == dim, "[DimensionError] Check your dimension "
    return new_array


# get difference of position A & B
def get_diff_position(a_position, b_position, dtype :str = "float32"):
    return np.subtract(a_position, b_position, dtype=dtype)


# get distance from difference position
def get_distance(diff_position, axis: int = -1, dtype :str = "float32"):
    return np.sqrt(np.sum(np.square(diff_position), axis=axis)).astype(dtype)
