# MDbrew

<img src="https://img.shields.io/badge/Python-383b40?style=round-square&logo=Python&logoColor=#f5f5f5"/> <img src="https://img.shields.io/badge/Jupyter-383b40?style=round-square&logo=Jupyter&logoColor=#f5f5f5"/>

mdbrew is a package for postprocessing of molecular dynamics simulation  
Supported Format : [".xyz", "XDATCAR", ".pdb", ".gro", ".trr", ".gro]

- VERSION : (2.5.0)

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

### Example - brewing something

```python
import mdbrew as mdb
file_path = "somewhere"
mb= mdb.Brewery(path=file_path, fmt="xyz")
# Properties of Brewery
coords = mb.coords
atom_info = mb.atom_info
columns = mb.columns
frame = mb.frame
data = mb.data
# Move on to the next frame
mb.move_on_next_frame()
# Move on to frame of 100
mb.move_frame(num=100)
# iteration of mb
mb.frange(start=100, end=200, step=2) # Generator
# brew is as same as pandas query
something = mb.brew(cols=["x", "y", "z"], what="atom == 'O'")
# order
O_ = mb.order(what="atom == 'O'")
```

- ! brew option is as same as pandas query

### Example - RDF

```python
import mdbrew as mdb
file_path = "somewhere"
mb= mdb.Brewery(path=file_path, fmt="xyz")
box_size = mb.box_size
order_1 = mb.order(what="type == 1")
order_2 = mb.order(what="type == 2")
rdf = mdb.RDF(order_1, order_2, box_size).run(start=0, end=None, step=1)
rdf_radii = rdf.radii
rdf_result = rdf.result
rdf_cn = rdf.cn
```

### Example - MSD

```python
import mdbrew as mdb
file_path = "somewhere"
mb= mdb.Brewery(path=file_path, fmt="xyz")
box_size = mb.box_size
order_1 = mb.order(what="type == 1")
order_2 = mb.order(what="type == 2")
msd = mdb.MSD(order_1, fft=True, do_unwrap=True).run(start=0, end=None, step=1)
msd_result = rdf.result
```

### Example - write

```python
import mdbrew as mdb
FRAME = 1000
file_path = "somewhere"
mb= mdb.Brewery(path=file_path, fmt="xyz")
mb.write(fmt="poscar", save_path="./POSCAR", start=FRAME, end=FRAME+1)
```
