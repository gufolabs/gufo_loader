# ---------------------------------------------------------------------
# Gufo Loader: Attribute filtering tests
# ---------------------------------------------------------------------
# Copyright (C) 2026, Gufo Labs
# ---------------------------------------------------------------------

from gufo.loader import Loader

from .attribute.base import BasePlugin
from .attribute.plugins.example import singleton


def test_loads_only_named_attribute() -> None:
    loader = Loader[BasePlugin](base="tests.attribute.plugins", attribute="singleton")

    item = loader["example"]

    assert item is singleton
    assert item.get_name() == "singleton"
