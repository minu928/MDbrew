from .__init__ import *


def tester(path):
    print("\n\ttest Init \u2713 \t\n")
    source = LAMMPSOpener(path)
    extractor = Extractor(opener=source)
    system_size = extractor.system_size
    position = extractor.extract_position(type_=1, wrapped=True)[-10:]
    uw_position = extractor.extract_position(type_=1, wrapped=False)[-10:]
    RDF(position, position, system_size).result
    MSD(uw_position).result
    print("\n\ttest Done \u2713 \t\n")
