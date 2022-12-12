from .tools import *
from .opener import Opener

# Extract the data
class Extractor(object):
    def __init__(self, opener: Opener, dim: int = 3) -> None:
        self.dim = dim
        self.database = opener.get_database()
        self.columns = opener.get_columns()
        self.system_size = opener.get_system_size()
        self.time_step = opener.get_time_step()
        self.lag_number = len(self.database)
        self.pos_ = self.__check_position()

    @timeCount
    def extract_type(self, key_word: str = "type"):
        key_word = key_word.lower()
        df_data = pd.DataFrame(data=self.database[0], columns=self.columns)
        col_type = df_data[key_word]
        return set(col_type)

    @timeCount
    def extract_position(self, type_: int, wrapped=True) -> NDArray[np.float64]:
        db_position = []
        get_position = self.__check_method(wrapped=wrapped)
        for lag in range(self.lag_number):
            df_data = pd.DataFrame(data=self.database[lag], columns=self.columns)
            self.__df_data = df_data[df_data["type"] == type_]
            position = get_position()
            db_position.append(position)
        return np.asarray(db_position, dtype=np.float64)

    def __check_method(self, wrapped):
        if wrapped:
            return self.__df_wrapped_position
        else:
            return self.__df_unwrapped_position

    def __df_wrapped_position(self) -> NDArray[np.float64]:
        return np.array(self.__df_data[self.pos_])

    def __df_unwrapped_position(self) -> NDArray[np.float64]:
        if self.__already_unwrapped:
            return self.__df_wrapped_position()
        else:
            idx_ix = self.columns.index("ix")
            list_in = self.columns[idx_ix : idx_ix + self.dim]
            box_size = np.array(self.system_size)[:, 1]
            idx_position = self.__df_data[list_in] * box_size
            return np.array(idx_position) + self.__df_wrapped_position()

    def __check_position(self) -> list[str]:
        for idx, column in enumerate(self.columns):
            if column in ["x", "xs"]:
                self.__already_unwrapped = False
                return self.columns[idx : idx + self.dim]
            elif column in ["xu", "xsu"]:
                self.__already_unwrapped = True
                return self.columns[idx : idx + self.dim]
        raise Exception(f"COLUMNS : {self.columns} is not normal case")
