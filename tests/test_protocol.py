# ---------------------------------------------------------------------
# Gufo Labs Loader:
# Protocol tests
# ---------------------------------------------------------------------
# Copyright (C) 2022, Gufo Labs
# ---------------------------------------------------------------------

# Python modules
from typing import Type

# Third-party modules
import pytest

# Gufo Labs modules
from gufo.loader import Loader
from .protocol.base import Named

PLUGIN_BASES = ["tests.protocol.primary", "tests.protocol.secondary"]


@pytest.fixture(scope="module")
def loader():
    return Loader[Named](bases=PLUGIN_BASES)


@pytest.mark.parametrize(
    ("name", "expected_name"),
    [
        ("a", "a"),
        ("b", "b"),
        ("c", "c"),
    ],
)
def test_getitem(name, expected_name, loader):
    item: Named = loader[name]
    assert isinstance(item, Named)
    assert item().get_name() == expected_name
