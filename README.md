# MDbrew

<img src="https://img.shields.io/badge/Python-383b40?style=round-square&logo=Python&logoColor=#f5f5f5"/> <img src="https://img.shields.io/badge/Jupyter-383b40?style=round-square&logo=Jupyter&logoColor=#f5f5f5"/>

mdbrew is a package for postprocessing of molecular dynamics simulation  
Supported Format : [".xyz", "XDATCAR", ".pdb", ".gro", ".trr", ".gro]

- VERSION : (2.5.2)

## How to install

```bash
pip install mdbrew
```

## Example Code For Brewery

### Example - Load the file

```python
import mdbrew as mdb
file_path = "somewhere"
mb= mdb.Brewery(path=file_path, fmt="xyz")
```

## Further Information

[MANUAL_PAGES](https://minu928.github.io/MDBREW/)
