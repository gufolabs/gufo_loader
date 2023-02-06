# ---------------------------------------------------------------------
# Gufo Loader: b plugin class spoiler. Must be overriden by primary/a.py
# ---------------------------------------------------------------------
# Copyright (C) 2022-23, Gufo Labs
# ---------------------------------------------------------------------


from ..base import BasePlugin


class BPlugin(BasePlugin):
    name = "b?"

    def get_name(self: "BPlugin") -> str:
        return self.name
