# ---------------------------------------------------------------------
# Gufo Loader: Plugin with a fixed singleton attribute
# ---------------------------------------------------------------------
# Copyright (C) 2026, Gufo Labs
# ---------------------------------------------------------------------

from ..base import BasePlugin


class ExamplePlugin(BasePlugin):
    name = "singleton"

    def get_name(self) -> str:
        return self.name


class DecoyPlugin(BasePlugin):
    name = "decoy"

    def get_name(self) -> str:
        return self.name


singleton = ExamplePlugin()
decoy = DecoyPlugin()
