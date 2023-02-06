# ---------------------------------------------------------------------
# Gufo Loader: Singleton tests
# ---------------------------------------------------------------------
# Copyright (C) 2022-23, Gufo Labs
# ---------------------------------------------------------------------

# Third-party modules
import pytest

# Gufo Labs modules
from gufo.loader import Loader

from .singleton.base import BasePlugin

PLUGIN_BASES = ["tests.singleton.primary", "tests.singleton.secondary"]
LoaderType = Loader[BasePlugin]


@pytest.fixture(scope="module")
def loader() -> LoaderType:
    return Loader[BasePlugin](bases=PLUGIN_BASES)


@pytest.mark.parametrize(
    ("name", "expected_name"),
    [
        ("a", "a"),
        ("b", "b"),
        ("c", "c"),
    ],
)
def test_getitem(name: str, expected_name: str, loader: LoaderType) -> None:
    item = loader[name]
    assert isinstance(item, BasePlugin)
    assert item.get_name() == expected_name
