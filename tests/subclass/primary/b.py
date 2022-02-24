# ---------------------------------------------------------------------
# Gufo Labs Loader:
# b plugin class
# ---------------------------------------------------------------------
# Copyright (C) 2022, Gufo Labs
# ---------------------------------------------------------------------


from ..base import BasePlugin


class BPlugin(BasePlugin):
    name = "b"

    def get_name(self) -> str:
        return self.name
