import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy.typing import NDArray

__all__ = ["np", "pd", "plt", "NDArray"]

""" How to use

## ZERO. import MDbrew as mdb


## First. Openr your file
>>> file_path = './test.lammpstrj'
>>> opener = mdb.LAMMPSOpener('./test.lammpstrj')


## Second. Extract your data
>>> extractor = mdb.Extractor(opener=opener)
>>> system_size = extractor.system_size
>>> type_ = extractor.extract_type()
>>> one_position = extractor.extract_position(type_=1.0)
>>> two_position = extractor.extract_position(type_=2.0)

>>> one_position_unwrapped = extractor.extract_position(type_=1.0, wrapped=False)


## Third. analyze the data 

### RDF
>>> rdf = mdb.RDF(one_position, two_position, system_size)
>>> rdf_result = rdf.result
>>> rdf.plot_result()

### MSD
>>> msd = mdb.MSD(one_position_unwrapped)
>>> msd_result = msd.result
>>> msd.plot_result()

"""
