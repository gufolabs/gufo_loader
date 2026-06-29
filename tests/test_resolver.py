# ---------------------------------------------------------------------
# Gufo Loader: Resolver tests
# ---------------------------------------------------------------------
# Copyright (C) 2022-26, Gufo Labs
# ---------------------------------------------------------------------

# Python modules
from collections.abc import Callable

# Third-party modules
import pytest

# Gufo Labs modules
from gufo.loader import ImportPathResolver
from gufo.loader.resolver import _sentinel

INVALID_PATH = "tests.test_resolver.invalid"


def add(x: int, y: int) -> int:
    return x + y


def sub(x: int, y: int) -> int:
    return x - y


ResolverType = ImportPathResolver[Callable[[int, int], int]]


@pytest.fixture(scope="module")
def resolver() -> ResolverType:
    return ImportPathResolver[Callable[[int, int], int]]()


@pytest.mark.parametrize(
    ("path", "x", "y", "expected"),
    [
        ("tests.test_resolver.add", 1, 2, 3),
        ("tests.test_resolver.sub", 3, 2, 1),
    ],
)
def test_resolver(
    path: str, x: int, y: int, expected: int, resolver: ResolverType
) -> None:
    fn = resolver(path)
    r = fn(x, y)
    assert isinstance(r, int)
    assert r == expected


def test_invalid_path(resolver: ResolverType) -> None:
    with pytest.raises(ImportError):
        resolver(INVALID_PATH)


def test_invalid_format(resolver: ResolverType) -> None:
    with pytest.raises(ValueError):
        resolver("add")


def test_negative_caching() -> None:
    # Fresh resolver
    resolver = ImportPathResolver[Callable[[int, int], int]]()
    # Must not be in cache
    assert INVALID_PATH not in resolver._cache
    # Load and populate the cache
    with pytest.raises(ImportError):
        resolver(INVALID_PATH)
    # The sentinel must be in cache
    assert INVALID_PATH in resolver._cache
    assert resolver._cache[INVALID_PATH] is _sentinel
    # The sentinel triggrer an error from cache
    with pytest.raises(ImportError):
        resolver(INVALID_PATH)


def test_no_negative_caching() -> None:
    # Fresh resolver
    resolver = ImportPathResolver[Callable[[int, int], int]](
        cache_negative=False
    )
    # Must not be in cache
    assert INVALID_PATH not in resolver._cache
    # Repeat twice
    for _ in range(2):
        # Force error
        with pytest.raises(ImportError):
            resolver(INVALID_PATH)
        # The sentinel must not be in cache
        assert INVALID_PATH not in resolver._cache


def test_passthrough() -> None:
    resolver = ImportPathResolver[Callable[[int, int], int]]()
    # Cache is clean
    assert not resolver._cache
    # Check passthrough
    fn = resolver(add)
    assert fn is add
    # Cache is clean
    assert not resolver._cache
