import sys
from collections.abc import Callable

from gufo.loader import ImportPathResolver

resolver = ImportPathResolver[Callable[[int, int], int]]()
OPS = {
    "add": "myapp.ops.add",
    "sub": "myapp.ops.sub",
}


def main(op: str, x: int, y: int) -> None:
    fn = resolver(OPS[op])
    r = fn(x, y)
    print(r)


main(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
