from .._base import *

__all__ = ["_find_data_by_keyword"]


def find_data_by_keyword(data, columns, keyword) -> NDArray[np.int64]:
    keyword = keyword.lower()
    df_data = pd.DataFrame(data=data, columns=columns)
    return df_data[keyword].to_numpy(dtype=np.int64)
