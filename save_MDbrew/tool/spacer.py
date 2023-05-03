import numpy as np
from numpy.typing import NDArray

__all__ = ["check_dimension", "get_diff_position", "get_distance"]


# Dimension checker
def check_dimension(array: NDArray, dim: int) -> NDArray[np.float64]:
    """
    Check the dimension of array data

    Parameters
    ----------
    array : NDArray
        array which you want to check
    dim : int
        dimension of array you think

    Returns
    -------
    NDArray[np.float64]
        _description_
    """
    new_array = np.asarray(array, dtype=np.float64)
    assert new_array.ndim == dim, "[DimensionError] Check your dimension "
    return new_array


# get difference of position A & B
def get_diff_position(a_position: NDArray, b_position: NDArray) -> NDArray[np.float64]:
    """
    Calculate the different of position

    Parameters
    ----------
    a_position : NDArray
        position of a
    b_position : NDArray
        position of b

    Returns
    -------
    NDArray[np.float64]
        diff position of ab
    """
    return np.subtract(a_position, b_position, dtype=np.float64)


# get distance from difference position
def get_distance(diff_position: NDArray, axis: int = -1) -> NDArray[np.float64]:
    """
    Calcaulte the distance from different position

    Parameters
    ----------
    diff_position : NDArray
        different position data
    axis : int, optional
        axis that sum the data, by default -1

    Returns
    -------
    NDArray[np.float64]
        distance of data
    """
    return np.sqrt(np.sum(np.square(diff_position), axis=axis))
