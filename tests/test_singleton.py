# ---------------------------------------------------------------------
# Gufo Labs Loader:
# Singleton tests
# ---------------------------------------------------------------------
# Copyright (C) 2022, Gufo Labs
# ---------------------------------------------------------------------

# Third-party modules
import pytest

# Gufo Labs modules
from gufo.loader import Loader
from .singleton.base import BasePlugin

PLUGIN_BASES = ["tests.singleton.primary", "tests.singleton.secondary"]


@pytest.fixture(scope="module")
def loader():
    return Loader[BasePlugin](bases=PLUGIN_BASES)


@pytest.mark.parametrize(
    ("name", "expected_name"),
    [
        ("a", "a"),
        ("b", "b"),
        ("c", "c"),
    ],
)
def test_getitem(name, expected_name, loader):
    item = loader[name]
    assert isinstance(item, BasePlugin)
    assert item.get_name() == expected_name
