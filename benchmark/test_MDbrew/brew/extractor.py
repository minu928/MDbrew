from ..tool.timer import time_count
from ..tool.query import find_data_by_keyword
from .._base import *
from .._type import OpenerType
from ..chemistry.atom import switch_to_atom_list, atom_info


__all__ = ["Extractor"]


# id information in database
class __Id__(object):
    def __init__(self, database, columns):
        self.database = database
        self.columns = columns

    def extract_list(self, keyword: str = "id") -> NDArray[np.int64]:
        """
        Extract the id from traj file

        Parameters
        ---------
        keyword : str, optional
            keyword of 'id' in your traj. Defaults to "id".

        Returns
        -------
        NDArray[np.int64]
            ndarray of id in sequential
        """
        return find_data_by_keyword(data=self.database[0], columns=self.columns, keyword=keyword)


# Atom information in database
class __Atom__(object):
    def __init__(self, database, columns):
        self.database = database
        self.columns = columns

    def __get_type_list(self, keyword: str = "type") -> NDArray[np.int64]:
        return find_data_by_keyword(data=self.database[0], columns=self.columns, keyword=keyword)

    def extract_type_list(self, keyword: str = "type") -> NDArray[np.int64]:
        """
        Extract the type_list

        Parameters
        ----------
        keyword : str, optional
            atom(type) keyword of your traj file. Defaults to "type".

        Returns
        -------
        NDArray[np.int64]
            ndarray data of atom(type) list
        """
        return self.__get_type_list(keyword=keyword)

    def extract_type_info(self, keyword: str = "type"):
        """
        Extract the unique data from type_list

        Parameters
        ----------
        keyword : str, optional
            atom(type) keyword of your traj file. Defaults to "type".

        Returns
        -------
        tuple(NDArray, NDArray)[0] = unique data of type_list, [1] = number of each type
        """
        return np.unique(self.__get_type_list(keyword=keyword), return_counts=True)

    def extract_atom_list(self, dict_type: dict[int:str], keyword: str = "type") -> NDArray[np.int64]:
        """
        Extract the Atom list from your traj file

        Parameters
        ----------
        dict_type : dict[int:str]
            dictionary data || key = number of type in traj || value = atomic name, ex) He
        keyword : str, optional
            atom(type) keyword of your traj file. Defaults to "type".

        Returns
        -------
        NDArray[np.int64]
            return the atomic number list
        """
        return switch_to_atom_list(type_list=self.__get_type_list(keyword=keyword), dict_type=dict_type)


# Position information in database
class __Position__(object):
    def __init__(self, dim, system_size, database, frame_number, columns):
        self.dim = dim
        self.system_size = system_size
        self.database = database
        self.frame_number = frame_number
        self.columns = columns
        self.pos_ = None

    def extract(self, target_type: int = "all", wrapped=True) -> NDArray[np.float64]:
        """
        Extract position

        Extract the position in opener

        Parameters
        ----------
        target_type : int
            your type name in type_list, default = "All"
        wrapped : bool, optional
            control the is wrapped. Defaults to True.

        Returns
        -------
        NDArray[np.float64]
            data of position, shape = [frames, number_of_particle, dimension]
        """
        self.pos_ = self._check_pos_()
        get_position_from = self.__check_position_method(wrapped=wrapped)
        position_list = []
        for frame in range(self.frame_number):
            df_data = pd.DataFrame(data=self.database[frame], columns=self.columns)
            df_data = df_data if target_type == "all" else df_data[df_data["type"] == target_type]
            position = get_position_from(df_data)
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


# Extractor of Something
class Extractor(object):
    def __init__(self, opener: OpenerType, dim: int = 3) -> None:
        """Extractor

        Extract easily the date from Opener (or LAMMPSOpener)

        Parameters
        ----------
        opener : (OpenerType)
            instance of class in MDbrew
        dim : (int, optional)
            dimension of your data. Defaults to 3.

        >>> extractor = Extractor(opener = LAMMPSOpener, dim = 3)
        >>> type_list = extractor.extract_type()
        >>> one_position = extractor.extract_position(type_ = 1)
        >>> un_wrapped_pos = extractor.extract_position(type_ = 1, wrapped = False)
        """

        self.dim = dim
        self.database = opener.get_database()
        self.columns = opener.get_columns()
        self.system_size = opener.get_system_size()
        self.time_step = opener.get_time_step()
        self.frame_number = len(self.database)
        self.position = __Position__(
            dim=dim,
            system_size=self.system_size,
            database=self.database,
            frame_number=self.frame_number,
            columns=self.columns,
        )
        self.atoms = __Atom__(database=self.database, columns=self.columns)
        self.id_ = __Id__(database=self.database, columns=self.columns)

    @time_count
    def extract_position(self, target_type: int = "all", wrapped=True) -> NDArray[np.float64]:
        """
        Extract position

        Extract the position in opener

        Parameters
        ----------
        target_type (int)
            your type name in type_list, default = "All"
        wrapped (bool, optional)
            control the is wrapped. Defaults to True.

        Returns
        ----------
        NDArray[np.float64],
            data of position, shape = [F, N, dim]

        """
        return self.position.extract(target_type=target_type, wrapped=wrapped)

    @time_count
    def extract_type_list(self, keyword: str = "type") -> NDArray[np.int64]:
        """
        Extract the type_list

        Parameters
        ----------
        keyword (str, optional)
            atom(type) keyword of your traj file. Defaults to "type".

        Returns
        ----------
        NDArray[np.int64]
            ndarray data of atom(type) list
        """
        return self.atoms.extract_type_list(keyword=keyword)

    @time_count
    def extract_type_info(self, keyword: str = "type"):
        """
        Extract the unique data from type_list

        Parameters
        ----------
        keyword : str, optional
            atom(type) keyword of your traj file. Defaults to "type".

        Returns
        -------
        tuple(NDArray, NDArray)[0] = unique data of type_list, [1] = number of each type
        """
        return self.atoms.extract_type_info(keyword=keyword)

    @time_count
    def extract_atom_list(self, dict_type: dict[int:str], keyword: str = "type") -> NDArray[np.int64]:
        """
        Extract the Atom list from your traj file

        Parameters
        ----------
        dict_type : dict[int:str]
            dictionary data || key = number of type in traj || value = atomic name, ex) He
        keyword : str, optional
            atom(type) keyword of your traj file. Defaults to "type".

        Returns
        -------
        NDArray[np.int64]
            return the atomic number list
        """
        return self.atoms.extract_atom_list(dict_type=dict_type, keyword=keyword)

    @time_count
    def extract_id_list(self, keyword: str = "id") -> NDArray[np.int64]:
        """
        Extract the id from traj file

        Parameters
        ---------
        keyword : str, optional
            keyword of 'id' in your traj. Defaults to "id".

        Returns
        -------
        NDArray[np.int64]
            ndarray of id in sequential
        """
        return self.id_.extract_list(keyword=keyword)

    @property
    def atom_info(self):
        """
        Load the atom_info.npz

        Keys
        -------
        - atom_name_list = atom_info["atom_name"]
        - atom_number_list = atom_info["atom_number"]
        - atom_weight_list = atom_info["atom_weight"]
        """
        return atom_info
