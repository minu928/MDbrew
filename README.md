# MDbrew
<img src="https://img.shields.io/badge/Python-383b40?style=round-square&logo=Python&logoColor=#f5f5f5"/> <img src="https://img.shields.io/badge/Jupyter-383b40?style=round-square&logo=Jupyter&logoColor=#f5f5f5"/>

MDbrew is a tool for postprocessing of LAMMPS data or lammpstrj(dump)

~~~zsh
pip install MDbrew
~~~
- VERSION :  (2.0.2)

## Package

### Opener  
- LAMMPSOpener : for dump file (ex. dump.lammpstrj)  
### tools  
- timeCount : decorator for get execute time
### linalg
- LinearRegression : Class for linear regression  
### extractor
- Extractor : class for extract the data form of Opener
### msd  
- MSD : Class for get MSD data with position data [ lagtime, Number of Particle, pos ]  
### rdf  
- RDF : Class for get RDF data with position data [ lagtime, Number of Particle, pos ]  

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
wrapped_position = extractor.extract_position(type_=1, wrapped=True)
unwrapped_position = extractor.extract_position(type_=1, wrapped=False)
type_list = extractor.extract_type()
system_size = extractor.system_size
fff
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
