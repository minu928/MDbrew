import os
import TEST_MDbrew as mdb
from TEST_MDbrew.tool.doctor import doctor

if __name__ == "__main__":
    c_path = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(c_path, "data/test.lmps")
    print(f"\n\t\t     Version : {mdb.__version__}\n")
    doctor(path=path)
