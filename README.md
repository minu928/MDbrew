# MDbrew
<img src="https://img.shields.io/badge/Python-383b40?style=round-square&logo=Python&logoColor=#f5f5f5"/> <img src="https://img.shields.io/badge/Jupyter-383b40?style=round-square&logo=Jupyter&logoColor=#f5f5f5"/>

MDbrew is a tool for postprocessing of LAMMPS data or lammpstrj(dump)

- VERSION :  (2.1.0)

## How to install
~~~bash
pip install MDbrew
~~~

## Code

### Example - Open the file
~~~python
from MDbrew import LAMMPSOpener
path = "file_path"
opener = LAMMPSOpener(path)
database = data.get_database()
column = data.get_column()
system_size = data.get_system_size()
~~~

### Example - MDbrew.Extractor
~~~python
from MDbrew import Extractor
extractor = Extractor(opener=opener)
wrapped_position = extractor.extract_position(target_type=1, wrapped=True)
unwrapped_position = extractor.extract_position(target_type=1, wrapped=False)

type_list = extractor.extract_type_list()
type_info = extractor.extract_type_info()

atom_list = extractor.extract_atom_list()
~~~

### Example - RDF
~~~python
from MDbrew import RDF
rdf = RDF(wrapped_position, wrapped_position, system_size)
rdf_result = rdf.result
rdf_cn = rdf.cn
~~~

### Example - MSD
~~~python
from MDbrew import MSD
msd = MSD(unwrapped_position)
msd.result
~~~
