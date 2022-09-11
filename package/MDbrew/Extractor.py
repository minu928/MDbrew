import numpy as np
import pandas as pd
from .tools import timeCount

# Extract the data
class Extractor(object):
    def __init__(self, data) -> None:
        self.database = data.get_database()
        self.column = data.get_columns()
        self.lag_number = len(self.database)
        self.box_size = np.array(data.get_system_size())[:, 1] * 2.0

    @timeCount
    def get_position_db(self, type_: int, pos_: list[str] = ["x", "y", "z"]):
        db_position = []
        for lag in range(self.lag_number):
            df_data = pd.DataFrame(data=self.database[lag], columns=self.column)
            df_type = df_data[df_data["type"] == type_]
            unit_position = df_type[pos_]
            db_position.append(unit_position)
        return np.array(db_position)

    @timeCount
    def get_unwrapped_position(self, type_: int, pos_: list[str] = ["x", "y", "z"]):
        if "ix" not in self.column:
            raise ValueError(f"[ ix iy iz ] is not in your column {self.column}")
        else:
            db_idx_position = []
            db_position = []
            for lag in range(self.lag_number):
                df_data = pd.DataFrame(data=self.database[lag], columns=self.column)
                df_type = df_data[df_data["type"] == type_]
                unit_position = df_type[pos_]
                idx_position = df_type[["ix", "iy", "iz"]] * self.box_size
                db_position.append(unit_position)
                db_idx_position.append(idx_position)
            return np.array(db_position) + np.array(db_idx_position)
