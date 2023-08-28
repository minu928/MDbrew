from time import time
from tqdm import tqdm
from ..tool.colorfont import color

__all__ = ["check_tab", "color_print", "color_print_verbose"]


# determine the tab
def check_tab(name: str) -> int:
    TAB_SIZE = 8
    str_number = len(name)
    tab_number = str_number // TAB_SIZE
    return 3 - tab_number


# Wrapper of count the function execution time
def color_print(name):
    def deco(func):
        def inner(*args, **kwrgs):
            print(f"[ {color.font_green}RUNN{color.reset} ] {name}", end="\r")
            start = time()
            result = func(*args, **kwrgs)
            end = time()
            end_string = f"[ {color.font_red}DONE{color.reset} ] {name}"
            end_string += "\t" * check_tab(name=name) + f" -> {end - start :5.2f} s \u2705"
            print(end_string)
            return result

        return inner

    return deco


# Wrapper of count the function execution time
def color_print_verbose(name):
    def deco(func):
        def inner(*args, **kwrgs):
            verbose = kwrgs.pop("verbose", False)
            if verbose:
                print(f"[ {color.font_green}RUNN{color.reset} ] {name}", end="\r")
                start = time()
            result = func(verbose=verbose, *args, **kwrgs)
            if verbose:
                end = time()
                end_string = f"[ {color.font_red}DONE{color.reset} ] {name}"
                end_string += "\t" * check_tab(name=name) + f" -> {end - start :5.2f} s \u2705"
                print(end_string)
            return result

        return inner

    return deco


def color_tqdm(name):
    def deco(func):
        def inner(*args, **kwrgs):
            verbose = kwrgs.pop("verbose", False)
            if verbose:
                return tqdm(func(verbose=verbose, *args, **kwrgs), desc=f"[ {color.font_magenta}{name}{color.reset} ]")
            else:
                return func(verbose=verbose, *args, **kwrgs)

        return inner

    return deco
