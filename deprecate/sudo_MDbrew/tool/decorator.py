from time import time
from ..tool.colorfont import color

__all__ = ["time_count", "check_tab"]


# determine the tab
def check_tab(name: str) -> int:
    TAB_SIZE = 8
    str_number = len(name)
    tab_number = str_number // TAB_SIZE
    return 3 - tab_number


# Wrapper of count the function execution time
def color_print(name, verbose: bool = True):
    def deco(func):
        def inner(*args, **kwrgs):
            if verbose:
                print(f"[ {color.font_green}RUNN{color.reset} ] {name}", end="\r")
                start = time()
            result = func(*args, **kwrgs)
            if verbose:
                end = time()
                end_string = f"[ {color.font_red}DONE{color.reset} ] {name}"
                end_string += "\t" * check_tab(name=name) + f" -> {end - start :5.2f} s \u2705"
                print(end_string)
            return result

        return inner

    return deco
