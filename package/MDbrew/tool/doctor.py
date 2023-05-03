from ..analysis.msd import MSD
from ..analysis.rdf import RDF
from ..main.brewery import Brewery
from .colorfont import color


def doctor(path):
    LINE_WIDTH = 60
    sep_line = "=" * LINE_WIDTH
    print(sep_line)
    mb = Brewery(path=path, is_generator=True)
    coords = mb.coords
    atom_info = mb.atom_info
    order1 = mb.order(what="type == 1")
    order2 = mb.order(what="type == 2")
    print(sep_line)
    position = order1.reorder().coords
    ixiyiz = order1.reorder().brew(cols=["ix", "iy", "iz"])
    unwrapped_position = [pos + ixyz for pos, ixyz in zip(position, ixiyiz)]
    rdf = RDF(order1, order2, mb.box_size, max_frame=100).run()
    rdf.result
    msd = MSD(unwrapped_position).run()
    msd.result
    print(sep_line)
    print(mb)
