from ..analysis.msd import MSD
from ..analysis.rdf import RDF
from ..brewery import Brewery
from .colorfont import color


def doctor(path):
    LINE_WIDTH = 60
    sep_line = "=" * LINE_WIDTH
    print(sep_line)
    mb = Brewery(path=path)
    max_iter = 10
    coords = mb.brew(cols=["x", "y", "z"], max_iter=max_iter)
    coords = mb.brew_coords(max_iter=max_iter)
    atom_info = mb.brew_atom_info(cols=["type"])
    print(sep_line)
    rdf = RDF(coords, coords, mb.box_size).run()
    rdf.rdf
    msd = MSD(coords).run()
    msd.result
    print(sep_line)
    print(sep_line)
    print("||" + " " * 22 + " INFO " + " " * 28 + "||")
    print(sep_line)
    print(f"  [   BOX   ] : {rdf.box_size}")
    print(f"  [  FRAME  ] : {mb.frame_num}")
    print(f"  [ COLUMNS ] : {mb.columns[:3]} ...")
    print(f"  [  COORD  ] : {coords.shape}")
    print(f"  [ ATOM IF ] : {atom_info[0]} & {atom_info[1]}")
    print(sep_line)
    print(f"\t      @CopyRight by  {color.font_blue}minu928@snu.ac.kr{color.reset}")
    print(sep_line + "\n")
