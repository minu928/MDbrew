from ..tool.timer import timeCount
from ..tool.query import find_data_by_keyword
from .._base import *
from .._type import OpenerType
from ..chemistry.atom import switch_to_atom_list, atom_info

__all__ = ["Extractor"]

# Id information in database
class __Id__(object):
    @timeCount
    def extract_id_list(self, keyword: str = "id") -> NDArray[np.int64]:
        """
        Extract the id from traj file

        Args:
            keyword (str, optional): keyword of 'id' in your traj. Defaults to "id".

        Returns:
            NDArray[np.int64]: ndarray of id in sequential
        """
        return find_data_by_keyword(data=self.database[0], columns=self.columns, keyword=keyword)


# Atom information in database
class __Type__(object):
    def __get_type_list(self, keyword: str = "type") -> NDArray[np.int64]:
        return find_data_by_keyword(data=self.database[0], columns=self.columns, keyword=keyword)

    @timeCount
    def extract_type_list(self, keyword: str = "type") -> NDArray[np.int64]:
        """
        Extract the type_list

        Args:
            keyword (str, optional): atom(type) keyword of your traj file. Defaults to "type".

        Returns:
            NDArray[np.int64]: ndarray data of atom(type) list
        """
        return self.__get_type_list(keyword=keyword)

    @timeCount
    def extract_type_info(self, keyword: str = "type"):
        """
        Extract the unique data from type_list

        Args:
            keyword (str, optional): atom(type) keyword of your traj file. Defaults to "type".

        Returns:
            tuple(NDarray, NDarray): [0] = unique data of type_list, [1] = number of each type
        """
        return np.unique(self.__get_type_list(keyword=keyword), return_counts=True)

    @timeCount
    def extract_atom_list(self, dict_type: dict[int:str], keyword: str = "type") -> NDArray[np.int64]:
        """
        Extract the Atom list from your traj file

        Args:
            dict_type (dict[int:str]): dictionary data || key = number of type in traj || value = atomic name, ex) He
            keyword (str, optional): atom(type) keyword of your traj file. Defaults to "type".

        Returns:
            NDArray[np.int64]: return the atomic number list
        """
        return switch_to_atom_list(type_list=self.__get_type_list(keyword=keyword), dict_type=dict_type)

    @property
    def atom_info(self):
        """
        Load the atom_info.npz

        This data have below key
            1. atom_name_list = atom_info["atom_name"]
            2. atom_number_list = atom_info["atom_number"]
            3. atom_weight_list = atom_info["atom_weight"]
        """
        return atom_info


# Position infromation in database
class __Position__(object):
    @timeCount
    def extract_position(self, target_type: int = "all", wrapped=True) -> NDArray[np.float64]:
        """Extract position

        Extract the position in opener

        Args:
            target_type (int): your type name in type_list, default = "All"
            wrapped (bool, optional): control the is wrapped. Defaults to True.

        Returns:
            NDArray[np.float64]: data of position, shape = [frames, number_of_particle, dimension]
        """
        self.pos_ = self._check_pos_()
        get_position_from = self.__check_position_method(wrapped=wrapped)
        position_list = []
        for frame in range(self.frame_number):
            df_data = pd.DataFrame(data=self.database[frame], columns=self.columns)
            df_data = df_data if target_type == "all" else df_data[df_data["type"] == target_type]
            position = get_position_from(df_data=df_data)
            position_list.append(position)
        return np.asarray(position_list, dtype=np.float64)

    def __check_position_method(self, wrapped):
        return self._wrapped_method if wrapped else self._unwrapped_method

    def _wrapped_method(self, df_data) -> NDArray[np.float64]:
        return np.array(df_data[self.pos_])

    def _unwrapped_method(self, df_data) -> NDArray[np.float64]:
        if self.__already_unwrapped:
            return self._wrapped_method(df_data=df_data)
        else:
            idx_ix = self.columns.index("ix")
            list_in = self.columns[idx_ix : idx_ix + self.dim]
            box_size = np.array(self.system_size)[:, 1]
            idx_position = df_data[list_in] * box_size
            return np.array(idx_position) + self._wrapped_method(df_data=df_data)

    def _check_pos_(self) -> list[str]:
        for idx, column in enumerate(self.columns):
            if column in ["x", "xs"]:
                self.__already_unwrapped = False
                return self.columns[idx : idx + self.dim]
            elif column in ["xu", "xsu"]:
                self.__already_unwrapped = True
                return self.columns[idx : idx + self.dim]
        raise Exception(f"COLUMNS : {self.columns} is not normal case")


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
