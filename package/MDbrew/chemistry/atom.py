from .._base import *
from pkg_resources import resource_filename

__all__ = ["switch_to_atom_list", "atom_name_list", "atom_number_list", "atom_weight_list", "periodic_table"]

file_path = resource_filename(f"{__package__}", "atom_info.npz")
del resource_filename

# Atom Values
atom_info = np.load(file_path)
atom_name_list = atom_info["atom_name"]
atom_number_list = atom_info["atom_number"]
atom_weight_list = atom_info["atom_weight"]
periodic_table = dict(zip(atom_name_list, atom_number_list))

# Functions
def switch_to_atom_list(type_list: list[int], dict_type: dict[int:str]):
    """
    switch the type(ex. 1,2) to atomic number

    Args:
        type_list (list[int]): list consisted with type (1, 2, 3)
        dict_type (dict[int:str]): dictionary data

    Returns:
        NDArray()
    """
    componet_type_list = list(set(type_list))
    assert componet_type_list == list(
        dict_type.keys()
    ), f"dict_type: {dict_type}'s keys should be same with type_list component {componet_type_list}"
    type_list = np.array(type_list, dtype=np.int32)
    for key, value in dict_type.items():
        type_list = np.where(key == type_list, periodic_table[value], type_list)
    return type_list
