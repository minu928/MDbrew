from test_MDbrew.opener import DumpOpener
from test_MDbrew.tools import Extractor
from test_MDbrew.RDF import RDF
from test_MDbrew.MSD import MSD


def tester(path):
    print("\n\ttest Init \u2713 \t\n")
    data = DumpOpener(path)
    pos = Extractor(data=data).get_position_db(type_=1)[-2:]
    ss = data.get_system_size()
    data.get_columns()
    data.get_time_step()
    RDF(pos, pos, ss).get_rdf()
    MSD(pos).get_msd()
    print("\n\ttest Done \u2713 \t\n")
