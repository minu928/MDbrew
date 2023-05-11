from ..analysis.msd import MSD
from ..analysis.rdf import RDF
from ..main.brewery import Brewery
from .colorfont import color


def doctor(path):
    LINE_WIDTH = 60
    sep_line = "=" * LINE_WIDTH
    print(sep_line)
    mb = Brewery(trj_file=path, fmt="lmps")
    coords = mb.coords
    atom_info = mb.atom_info
    order1 = mb.order(what="type == 1")
    order2 = mb.order(what="type == 2")
    print(sep_line)
    position = order1.coords
    ixiyiz = order1.brew(cols=["ix", "iy", "iz"])
    unwrapped_position = [position + ixiyiz for _ in order1.frange()]
    rdf = RDF(order1, order2, mb.box_size).run(start=2, end=100, step=2)
    rdf.result
    msd = MSD(unwrapped_position).run()
    msd.result
    print(sep_line)
    print(mb)
