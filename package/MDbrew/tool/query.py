from .._base import *

__all__ = ["_find_data_by_keyword"]


def find_data_by_keyword(data, columns: list, keyword: str) -> NDArray[np.int64]:
    """
    Find the data by datafream search by keyword

    Args:
        data (list or NDArray): wanted data
        columns (list): target column suitable for data
        keyword (str): target_keyword

    Returns:
        NDArray[np.int64]: ndarray data
    """
    keyword = keyword.lower()
    df_data = pd.DataFrame(data=data, columns=columns)
    return df_data[keyword].to_numpy(dtype=np.int64)
