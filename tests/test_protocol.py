# ---------------------------------------------------------------------
# Gufo Loader: Protocol tests
# ---------------------------------------------------------------------
# Copyright (C) 2022-23, Gufo Labs
# ---------------------------------------------------------------------

# Third-party modules
import pytest

# Gufo Labs modules
from gufo.loader import Loader

from .protocol.base import Named

PLUGIN_BASES = ["tests.protocol.primary", "tests.protocol.secondary"]
LoaderType = Loader[Named]


@pytest.fixture(scope="module")
def loader() -> LoaderType:
    return Loader[Named](bases=PLUGIN_BASES)


@pytest.mark.parametrize(
    ("name", "expected_name"),
    [
        ("a", "a"),
        ("b", "b"),
        ("c", "c"),
    ],
)
def test_getitem(name: str, expected_name: str, loader: LoaderType) -> None:
    item: Named = loader[name]
    assert isinstance(item, Named)
    assert item().get_name() == expected_name
