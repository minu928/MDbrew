import MDbrew as mdb
from MDbrew.tool.doctor import doctor

if __name__ == "__main__":
    path = "./benchmark/data/test.lmps"
    print(f"\n{' '*6}Version : {mdb.__version__}")
    doctor(path=path)
