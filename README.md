# MDbrew
<img src="https://img.shields.io/badge/Python-383b40?style=round-square&logo=Python&logoColor=#f5f5f5"/> <img src="https://img.shields.io/badge/Jupyter-383b40?style=round-square&logo=Jupyter&logoColor=#f5f5f5"/>

MDbrew is a tool for postprocessing of molecular dynamics data

- VERSION :  (2.2.2)

## How to install
~~~bash
pip install MDbrew
~~~

## Code

### Example - Load the file
~~~python
import MDbrew as mdb
my_brewery = mdb.Brewery(path=file_path)
~~~

### Example - brewing something
~~~python
coords = my_brewery.brew_coords()
atom_info = my_brewery.brew_atom_info()
something = my_brewery.brew(ment="atom == 'O'")
~~~
- ! brew option is as same as pandas query

### Example - RDF
~~~python
from MDbrew import RDF
box_size = my_brewery.box_size
rdf = RDF(wrapped_position, wrapped_position, box_size)
rdf_result = rdf.rdf
rdf_cn = rdf.cn
~~~

### Example - MSD
~~~python
from MDbrew import MSD
msd = MSD(unwrapped_position)
msd.result
~~~
