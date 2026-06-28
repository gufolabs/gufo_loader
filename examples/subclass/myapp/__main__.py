import sys

from gufo.loader import Loader

from .base import BasePlugin

loader = Loader[type[BasePlugin]](base="myapp.plugins")


def main(op: str, x: int, y: int) -> None:
    kls = loader[op]
    item = kls()
    r = item.execute(x, y)
    print(r)


main(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
