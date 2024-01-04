from .opener import opener_programs, OpenerInterface
from .writer import writer_programs, WriterInterface


__all__ = [
    "get_opener",
    "get_writer",
    "opener_programs",
    "writer_programs",
    "OpenerInterface",
    "WriterInterface",
]


def get_opener(fmt: str):
    assert fmt in opener_programs, f"'{fmt}' is not supported yet, Support fmt: {tuple(opener_programs.keys())}"
    return opener_programs[fmt]


def get_writer(fmt: str):
    assert fmt in writer_programs, f"'{fmt}' is not supported yet, Support fmt: {tuple(writer_programs.keys())}"
    return writer_programs[fmt]
