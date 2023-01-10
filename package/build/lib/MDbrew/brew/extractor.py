from ..tool.timer import timeCount
from .._base import *
from .._type import OpenerType, NumericType
from ..chemistry.atom import switch_to_atom_list, atom_info

__all__ = ["Extractor"]


def _find_data_by_keyword(data, columns, keyword) -> NDArray[np.int64]:
    keyword = keyword.lower()
    df_data = pd.DataFrame(data=data, columns=columns)
    return df_data[keyword].to_numpy(dtype=np.int64)


class __Id__(object):
    @timeCount
    def extract_id_list(self, keyword: str = "id") -> NDArray[np.int64]:
        return _find_data_by_keyword(data=self.database[0], columns=self.columns, keyword=keyword)


class __Type__(object):
    def __get_type_list(self, keyword: str = "type") -> NDArray[np.int64]:
        return _find_data_by_keyword(data=self.database[0], columns=self.columns, keyword=keyword)

    @timeCount
    def extract_type_list(self, keyword: str = "type") -> NDArray[np.int64]:
        return self.__get_type_list(keyword=keyword)

    @timeCount
    def extract_type_set(self, keyword: str = "type") -> set[np.int64]:
        return set(self.__get_type_list(keyword=keyword))

    @timeCount
    def extract_atom_list(self, dict_type: dict[int:str], keyword: str = "type") -> NDArray[np.int64]:
        return switch_to_atom_list(type_list=self.__get_type_list(keyword=keyword), dict_type=dict_type)

    @property
    def atom_info(self):
        return atom_info


class __Position__(object):
    @timeCount
    def extract_position(self, target_type: int = "All", wrapped=True) -> NDArray[np.float64]:
        """Extract position

        Extract the position in opener

        Args:
            target_type (int): your type name in type_list, default = "All"
            wrapped (bool, optional): control the is wrapped. Defaults to True.

        Returns:
            NDArray[np.float64]: data of position, shape = [frames, number_of_particle, dimension]
        """
        self.target_type = target_type
        db_position = []
        get_position = self.__check_position_method(wrapped=wrapped)
        for frame in range(self.frame_number):
            df_data = pd.DataFrame(data=self.database[frame], columns=self.columns)
            self.__df_data = self._check_is_type_none(df_data=df_data)
            position = get_position()
            db_position.append(position)
        return np.asarray(db_position, dtype=np.float64)

    def __check_position_method(self, wrapped):
        if wrapped:
            return self._wrapped_position_method
        else:
            return self._unwrapped_position_method

    def _wrapped_position_method(self) -> NDArray[np.float64]:
        return np.array(self.__df_data[self.pos_])

    def _unwrapped_position_method(self) -> NDArray[np.float64]:
        if self.__already_unwrapped:
            return self._wrapped_position_method()
        else:
            idx_ix = self.columns.index("ix")
            list_in = self.columns[idx_ix : idx_ix + self.dim]
            box_size = np.array(self.system_size)[:, 1]
            idx_position = self.__df_data[list_in] * box_size
            return np.array(idx_position) + self._wrapped_position_method()

    def _check_position(self) -> list[str]:
        for idx, column in enumerate(self.columns):
            if column in ["x", "xs"]:
                self.__already_unwrapped = False
                return self.columns[idx : idx + self.dim]
            elif column in ["xu", "xsu"]:
                self.__already_unwrapped = True
                return self.columns[idx : idx + self.dim]
        raise Exception(f"COLUMNS : {self.columns} is not normal case")

    def _check_is_type_none(self, df_data) -> NDArray[np.float64]:
        if self.target_type == "All":
            return df_data
        else:
            assert type(self.target_type) is not NumericType, f"{self.target_type} is not NumericType (int or float)"
            return df_data[df_data["type"] == self.target_type]


_Hierchy = [__Id__, __Type__, __Position__]

# Extractor of Something
class Extractor(*_Hierchy):
    def __init__(self, opener: OpenerType, dim: int = 3) -> None:
        """Extractor

        Extract easily the date from Opener (or LAMMPSOpener)

        Args:
            opener (OpenerType): instance of class in MDbrew.opener
            dim (int, optional): dimension of your data. Defaults to 3.

            >>> extracter = Extractor(opener = LAMMPSOpener, dim = 3)
            >>> type_list = extracotr.extract_type()
            >>> one_position = extractor.extract_position(type_ = 1)
            >>> un_wrapped_pos = extractor.extract_position(type_ = 1, wrapped = False)
        """
        self.dim = dim
        self.database = opener.get_database()
        self.columns = opener.get_columns()
        self.system_size = opener.get_system_size()
        self.time_step = opener.get_time_step()
        self.frame_number = len(self.database)
        self.pos_ = self._check_position()
