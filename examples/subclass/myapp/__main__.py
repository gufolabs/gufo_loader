import sys
from typing import Type
from gufo_loader import Loader
from .base import BasePlugin

loader = Loader[Type[BasePlugin]](base="myapp.plugins")


def main(op: str, x: int, y: int) -> None:
    kls = loader[op]
    item = kls()
    r = item.execute(x, y)
    print(r)


main(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
