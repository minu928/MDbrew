# MDbrew
<img src="https://img.shields.io/badge/Python-383b40?style=round-square&logo=Python&logoColor=#f5f5f5"/> <img src="https://img.shields.io/badge/Jupyter-383b40?style=round-square&logo=Jupyter&logoColor=#f5f5f5"/>

MDbrew is a tool for postprocessing of LAMMPS data or lammpstrj(dump)

~~~zsh
pip install MDbrew
~~~
- VERSION :  (1.3.5)

## Package

### Opener  
- DumpOpener : for dump file (ex. dump.lammpstrj)  
- DataOpener : for data file (ex. data.lammps)  
### tools  
- timeCount : decorator for get execute time
### linalg
- LinearRegression : Class for linear regression  
### Extractor
- Extractor : class for extract the data form of Opener
### MSD  
- MSD : Class for get MSD data with position data [ lagtime, Number of Particle, pos ]  
### RDF  
- RDF : Class for get RDF data with position data [ lagtime, Number of Particle, pos ]  

## Code

### Example - Open the file
~~~python
from MDbrew.opener import DumpOpener
path = "file_paht"
data = DumpOpener(path)
database = data.get_database()
column = data.get_column()
system_size = data.get_system_size()
~~~

### Example - MDbrew.Extractor
~~~python
from MDbrew.Extractor import Extractor
database_position = Extractor(data=data).get_position_db(type_=1, pos_=["x", "y", "z"])
~~~

### Example - RDF
~~~python
from MDbrew.RDF import RDF
rdf = RDF(database_position, database_position, system_size)
rdf_data = rdf.get_rdf()
rdf_radii = rdf.get_radii()
~~~

### Example - MSD
~~~python
from MDbrew.MSD import MSD
msd = MSD(database_position)
msd.get_msd(method="window", fft=True)
~~~
