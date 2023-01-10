from ..analysis import *
from ..brew import *


def do_test(path):
    print("\n\ttest Init \u2713 \t\n")
    source = LAMMPSOpener(path)
    extractor = Extractor(opener=source)
    system_size = extractor.system_size
    position = extractor.extract_position(target_type=1, wrapped=True)[-10:]
    uw_position = extractor.extract_position(target_type=1, wrapped=False)[-10:]
    id_list = extractor.extract_id_list()
    type_list = extractor.extract_type_list()
    dict_type = {1: "O", 2: "N"}
    atom_list = extractor.extract_atom_list(dict_type=dict_type)
    rdf = RDF(position, position, system_size)
    rdf.result
    msd = MSD(uw_position)
    msd.result
    print("\n\ttest Done \u2713 \t\n")
