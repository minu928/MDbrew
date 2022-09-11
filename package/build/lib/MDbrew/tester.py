from .opener import DumpOpener
from .Extractor import Extractor
from .RDF import RDF
from .MSD import MSD


def tester(path):
    print("\n\ttest Init \u2713 \t\n")
    data = DumpOpener(path)
    extractor = Extractor(data=data)
    pos = extractor.get_position_db(type_=1)[-10:]
    uw_pos = extractor.get_unwrapped_position(type_=1)[-10:]
    ss = data.get_system_size()
    data.get_columns()
    data.get_time_step()
    RDF(pos, pos, ss).get_rdf()
    MSD(uw_pos).get_msd()
    print("\n\ttest Done \u2713 \t\n")
