import sys

from gufo.loader import Loader

from .base import BasePlugin

loader = Loader[BasePlugin](base="myapp.plugins")


def main(op: str, x: int, y: int) -> None:
    item = loader[op]
    r = item.execute(x, y)
    print(r)


main(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
