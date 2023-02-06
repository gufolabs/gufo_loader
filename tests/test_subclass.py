# ---------------------------------------------------------------------
# Gufo Loader: Subclass tests
# ---------------------------------------------------------------------
# Copyright (C) 2022-23, Gufo Labs
# ---------------------------------------------------------------------

# Python modules
from typing import Type

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


@pytest.mark.parametrize(
    ("name", "expected_name"),
    [
        ("a", "a"),
        ("b", "b"),
        ("c", "c"),
    ],
)
def test_getitem(name: str, expected_name: str, loader: LoaderType) -> None:
    kls = loader[name]
    assert issubclass(kls, BasePlugin)
    item = kls()
    assert item.get_name() == expected_name
