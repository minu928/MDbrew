from .._base import *
from pkg_resources import resource_filename

__all__ = ["switch_to_atom_list"]
file_path = resource_filename("MDbrew.chemistry", "atom_info.npz")
atom_info = np.load(file_path)
atom_name_list = atom_info["atom_name"]
atom_number_list = atom_info["atom_number"]
atom_weight_list = atom_info["atom_weight"]
periodic_table = dict(zip(atom_name_list, atom_number_list))
del resource_filename


def switch_to_atom_list(type_list: list, dict_type: dict[int:str]):
    componet_type_list = list(set(type_list))
    assert componet_type_list == list(
        dict_type.keys()
    ), f"dict_type: {dict_type}'s keys should be same with type_list component {componet_type_list}"
    type_list = np.array(type_list, dtype=np.int32)
    for key, value in dict_type.items():
        type_list = np.where(key == type_list, periodic_table[value], type_list)
    return type_list
