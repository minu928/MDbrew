from time import time
from sys import stdout

# Check the name length
def check_name_length(name):
    sub = "\t"
    if len(name) >= 20:
        sub = ""
    return sub


# Wrapper of count the function execution time
def timeCount(func):
    def wrapper(*args, **kwargs):
        name = func.__name__
        sub = check_name_length(name=name)
        stdout.write(f" STEP (RUN ) :  {name}\r")
        start = time()
        result = func(*args, **kwargs)
        end = time()
        stdout.write(f" STEP (Done) :  {name}\t")
        stdout.write(f"{sub}-> {end - start :5.2f} s \u2705 \n")
        return result

    return wrapper
