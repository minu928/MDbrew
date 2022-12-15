import MDbrew as mdb
from MDbrew.tool.tester import do_test

if __name__ == "__main__":
    path = "./benchmark/test.lammpstrj"
    print(f"\n{' '*6}Version : {mdb.__version__}")
    do_test(path=path)
