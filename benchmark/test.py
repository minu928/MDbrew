from MDbrew.opener import DumpOpener
from MDbrew.tools import Extractor
from MDbrew.RDF import RDF
data = DumpOpener('./test.lammpstrj')
pos = Extractor(data=data).get_position_db(type_=1)
ss = data.get_system_size()
rdf = RDF(pos, pos, ss).get_rdf_all()