# MDbrew
<img src="https://img.shields.io/badge/Python-383b40?style=round-square&logo=Python&logoColor=#f5f5f5"/> <img src="https://img.shields.io/badge/Jupyter-383b40?style=round-square&logo=Jupyter&logoColor=#f5f5f5"/>

MDbrew is a tool for postprocessing of molecular dynamics data

- VERSION :  (2.3.0)

## How to install
~~~bash
pip install MDbrew
~~~

## Code

### Example - Load the file
~~~python
import MDbrew as mdb
my_brewery = mdb.Brewery(path=file_path, fmt="xyz", is_generator=True)
~~~

### Example - brewing something
~~~python
coords = my_brewery.coords()
atom_info = my_brewery.atom_info()
something = my_brewery.order(what="atom == 'O'")
~~~
- ! brew option is as same as pandas query

### Example - RDF
~~~python
from MDbrew import RDF
box_size = my_brewery.box_size
order_1 = my_brewery.order(what="type == 1")
order_2 = my_brewery.order(what="type == 2")
rdf = RDF(order_1, order_2, box_size).run()
rdf_result = rdf.result
rdf_cn = rdf.cn
~~~
