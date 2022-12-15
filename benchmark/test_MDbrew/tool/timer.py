from time import time
from sys import stdout

__all__ = ["timeCount"]

# determine the tab
def check_tab(name: str) -> int:
    TAB_SIZE = 8
    str_number = len(name)
    tab_number = str_number // TAB_SIZE
    return 3 - tab_number


# Wrapper of count the function execution time
def timeCount(func):
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
