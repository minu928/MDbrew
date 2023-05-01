from time import time
from sys import stdout
from ..tool.colorfont import ColorFont

color = ColorFont()

__all__ = ["time_count", "check_tab"]


# determine the tab
def check_tab(name: str) -> int:
    TAB_SIZE = 8
    str_number = len(name)
    tab_number = str_number // TAB_SIZE
    return 3 - tab_number


# Wrapper of count the function execution time
def time_count(func):
    def wrapper(*args, **kwargs):
        name = func.__name__
        stdout.write(f" STEP (RUN ) :  {name}\r")
        start = time()
        result = func(*args, **kwargs)
        end = time()
        stdout.write(f" STEP (Done) :  {name}")
        stdout.write("\t" * check_tab(name=name))
        stdout.write(f"-> {end - start :5.2f} s \u2705 \n")
        return result

    return wrapper

def color_print(name):
    def deco(func):
        def inner(*args, **kwrgs):
            stdout.write(f"[ {color.font_green}RUNN{color.reset} ] {name}")
            start = time()
            result = func(*args, **kwrgs)
            end = time()
            stdout.write(f"\r[ {color.font_red}DONE{color.reset} ] {name}")
            stdout.write("\t" * check_tab(name=name))
            stdout.write(f"-> {end - start :5.2f} s \u2705 \n")
            return result

        return inner

    return deco
