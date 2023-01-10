import os
import test_MDbrew as mdb
from test_MDbrew.tool.tester import do_test

if __name__ == "__main__":
    c_path = os.getcwd()
    path = c_path + "/test.lammpstrj"
    print(f"\n{' '*6}Version : {mdb.__version__}")
    do_test(path=path)
