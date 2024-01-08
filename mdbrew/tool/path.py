import os


def check_path(path, **kwrgs):
    path = os.path.join(os.getcwd(), path)
    assert os.path.isfile(path=path), f"Check your path || not {path}"
    return path
