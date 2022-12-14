from ..analysis import *
from ..brew import *


def do_test(path):
    print("\n\ttest Init \u2713 \t\n")
    source = LAMMPSOpener(path)
    extractor = Extractor(opener=source)
    system_size = extractor.system_size
    position = extractor.extract_position(type_=1, wrapped=True)[-10:]
    uw_position = extractor.extract_position(type_=1, wrapped=False)[-10:]
    rdf = RDF(position, position, system_size)
    rdf.result
    rdf.plot_result()
    msd = MSD(uw_position)
    msd.result
    msd.plot_result()
    print("\n\ttest Done \u2713 \t\n")
