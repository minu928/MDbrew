from .opener import DumpOpener
from .extractor import Extractor
from .rdf import RDF
from .msd import MSD


def tester(path):
    print("\n\ttest Init \u2713 \t\n")
    data = DumpOpener(path)
    data.get_time_step()
    extractor = Extractor(data=data)
    system_size = extractor.system_size
    position = extractor.extract_position(type_=1, wrapped=True)[-10:]
    uw_position = extractor.extract_position(type_=1, wrapped=False)[-10:]
    RDF(position, position, system_size).get_rdf(r_max=10)
    MSD(uw_position).get_msd()
    print("\n\ttest Done \u2713 \t\n")
