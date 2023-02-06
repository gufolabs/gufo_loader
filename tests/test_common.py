# ---------------------------------------------------------------------
# Gufo Loader: Common tests
# ---------------------------------------------------------------------
# Copyright (C) 2022-23, Gufo Labs
# ---------------------------------------------------------------------

# Python modules
from typing import List, Tuple, Type

# Third-party modules
import pytest

# Gufo Labs modules
from gufo.loader import Loader

from .subclass.base import BasePlugin

PLUGIN_BASES = ["tests.subclass.primary", "tests.subclass.secondary"]
LoaderType = Loader[Type[BasePlugin]]


@pytest.fixture(scope="module")
def loader() -> LoaderType:
    return Loader[Type[BasePlugin]](bases=PLUGIN_BASES)


@pytest.fixture(scope="module")
def exc_loader() -> LoaderType:
    return Loader[Type[BasePlugin]](bases=PLUGIN_BASES, exclude=["d"])


def test_base() -> None:
    loader = Loader[Type[BasePlugin]](base=PLUGIN_BASES[0])
    kls = loader["a"]
    assert issubclass(kls, BasePlugin)


def test_no_base() -> None:
    with pytest.raises(RuntimeError):
        Loader[Type[BasePlugin]]()


def test_both_bases() -> None:
    with pytest.raises(RuntimeError):
        Loader[Type[BasePlugin]](base=PLUGIN_BASES[0], bases=PLUGIN_BASES[1:])


def test_strict_miss() -> None:
    with pytest.raises(RuntimeError):
        Loader[Type[BasePlugin]](
            bases=[*PLUGIN_BASES, ".nonexistent"], strict=True
        )


def test_no_strict_miss() -> None:
    Loader[Type[BasePlugin]](bases=[*PLUGIN_BASES, ".nonexistent"])


def test_no_paths() -> None:
    with pytest.raises(RuntimeError):
        Loader[Type[BasePlugin]](bases=[".nonexistent1", ".nonexistent2"])


def test_get_none(loader: LoaderType) -> None:
    kls = loader.get("z")
    assert kls is None


class DefaultPlugin(BasePlugin):
    name = "default"

    def get_name(self: "DefaultPlugin") -> str:
        return self.name


def test_get_default(loader: LoaderType) -> None:
    kls = loader.get("z", DefaultPlugin)
    assert kls is DefaultPlugin


def test_key_error(loader: LoaderType) -> None:
    with pytest.raises(KeyError):
        loader["z"]


def test_get_exclude() -> None:
    loader = Loader[Type[BasePlugin]](bases=PLUGIN_BASES, exclude=["b"])
    kls = loader["a"]
    assert issubclass(kls, BasePlugin)
    with pytest.raises(RuntimeError):
        kls = loader["b"]


def test_cached_get() -> None:
    loader = Loader[Type[BasePlugin]](bases=PLUGIN_BASES)
    kls1 = loader["a"]
    assert issubclass(kls1, BasePlugin)
    kls2 = loader["a"]
    assert issubclass(kls2, BasePlugin)
    assert kls2 is kls1


def test_keys(exc_loader: LoaderType) -> None:
    keys = list(exc_loader.keys())
    assert keys == ["a", "b", "c"]


def test_values(exc_loader: LoaderType) -> None:
    values: List[str] = []
    for kls in exc_loader.values():
        values += [kls().get_name()]
    assert values == ["a", "b", "c"]


def test_items(exc_loader: LoaderType) -> None:
    items: List[Tuple[str, str]] = []
    for name, kls in exc_loader.items():
        items += [(name, kls().get_name())]
    assert items == [("a", "a"), ("b", "b"), ("c", "c")]
