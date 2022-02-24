# ---------------------------------------------------------------------
# Gufo Labs Loader:
# Subclass tests
# ---------------------------------------------------------------------
# Copyright (C) 2022, Gufo Labs
# ---------------------------------------------------------------------

# Python modules
from typing import Type

# Third-party modules
import pytest

# Gufo Labs modules
from gufo_loader import Loader
from .subclass.base import BasePlugin

PLUGIN_BASES = ["tests.subclass.primary", "tests.subclass.secondary"]


@pytest.fixture(scope="module")
def loader():
    return Loader[Type[BasePlugin]](bases=PLUGIN_BASES)


@pytest.mark.parametrize(
    ("name", "expected_name"),
    [
        ("a", "a"),
        ("b", "b"),
        ("c", "c"),
    ],
)
def test_getitem(name, expected_name, loader):
    kls = loader[name]
    assert issubclass(kls, BasePlugin)
    item = kls()
    assert item.get_name() == expected_name
