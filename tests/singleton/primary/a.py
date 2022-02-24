# ---------------------------------------------------------------------
# Gufo Labs Loader:
# a plugin singleton instance
# ---------------------------------------------------------------------
# Copyright (C) 2022, Gufo Labs
# ---------------------------------------------------------------------

from ..base import BasePlugin


class APlugin(BasePlugin):
    name = "a"

    def get_name(self) -> str:
        return self.name


a_singleton = APlugin()
