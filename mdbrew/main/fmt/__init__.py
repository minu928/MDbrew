from importlib import import_module
from pathlib import Path


HEAD = "mdbrew.main.fmt"

for fmt_folder in Path(__file__).parent.glob("*"):
    for py_file in fmt_folder.glob("*.py"):
        if not "__" in py_file.stem:
            import_module(f".{fmt_folder.stem}.{py_file.stem}", HEAD)

del import_module, Path
