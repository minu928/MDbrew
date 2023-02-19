from .._base import *

__all__ = ["find_data_by_keyword"]


def find_data_by_keyword(data, columns: list, keyword: str) -> NDArray[np.int64]:
    """
    Find the data by datafream search by keyword

    Parameters
    ----------
    data : list or NDArray
        wanted data
    columns : list
        target column suitable for data
    keyword : str
        target_keyword

    Returns:
        NDArray[np.int64]
            data from finded by keyword
    """
    keyword = keyword.lower()
    df_data = pd.DataFrame(data=data, columns=columns)
    return df_data.loc[:, keyword].to_numpy(dtype=np.int64)
