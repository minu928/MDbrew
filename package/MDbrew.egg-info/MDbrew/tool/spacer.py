from .._base import *

__all__ = ["check_dimension", "get_diff_position", "get_distance"]

# Dimension checker
def check_dimension(array: list, dim: int) -> NDArray[np.float64]:
    new_array = np.asarray(array, dtype=np.float64)
    assert new_array.ndim == dim, "[DimensionError] Check your dimension "
    return new_array


# get difference of position A & B
def get_diff_position(A_position: NDArray, B_position: NDArray) -> NDArray[np.float64]:
    return np.subtract(A_position, B_position, dtype=np.float64)


# get distance from difference position
def get_distance(diff_position: NDArray, axis: int = 0) -> NDArray[np.float64]:
    return np.sqrt(np.sum(np.square(diff_position), axis=axis))
