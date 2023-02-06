# ---------------------------------------------------------------------
# Gufo Loader: b plugin class
# ---------------------------------------------------------------------
# Copyright (C) 2022-23, Gufo Labs
# ---------------------------------------------------------------------


from ..base import BasePlugin


class BPlugin(BasePlugin):
    name = "b"

    def get_name(self: "BPlugin") -> str:
        return self.name
