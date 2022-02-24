# ---------------------------------------------------------------------
# Gufo Labs Loader:
# b plugin singleton instance. Must be overloaded
# by primary/b.py
# ---------------------------------------------------------------------
# Copyright (C) 2022, Gufo Labs
# ---------------------------------------------------------------------


from ..base import BasePlugin


class BPlugin(BasePlugin):
    name = "b?"

    def get_name(self) -> str:
        return self.name


b_singleton = BPlugin()
