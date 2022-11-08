import numpy as np
import pandas as pd
from .tools import timeCount

# Extract the data
class Extractor(object):
    def __init__(self, data, pos_: list[str] = None) -> None:
        self.data = data
        self.database = data.get_database()
        self.column = data.get_columns()
        self.system_size = self.data.get_system_size()
        self.lag_number = len(self.database)
        self.pos_ = self.__check_position(pos_=pos_)

    @timeCount
    def extract_position(self, type_: int, wrapped=True):
        db_position = []
        get_position = self.__check_method(wrapped=wrapped)
        for lag in range(self.lag_number):
            df_data = pd.DataFrame(data=self.database[lag], columns=self.column)
            self.df_data = df_data[df_data["type"] == type_]
            position = get_position()
            db_position.append(position)
        return np.asarray(db_position, dtype=np.float64)

    def __check_method(self, wrapped):
        if wrapped:
            return self.__df_wrapped_position
        else:
            return self.__df_unwrapped_position

    def __df_wrapped_position(self):
        return self.df_data[self.pos_]

    def __df_unwrapped_position(self):
        if self.pos_ == ["xu", "yu", "zu"] or self.pos_ == ["xsu", "ysu", "zsu"]:
            return np.array(self.__df_wrapped_position())
        else:
            box_size = np.array(self.system_size)[:, 1]
            idx_position = self.df_data[["ix", "iy", "iz"]] * box_size
            return np.array(idx_position) + np.array(self.__df_wrapped_position())

    def __check_position(self, pos_): 
        if pos_ == None:
            return ["x", "y", "z"]
        else:
            return pos_