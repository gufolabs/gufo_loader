# ---------------------------------------------------------------------
# Gufo Loader: a plugin class
# ---------------------------------------------------------------------
# Copyright (C) 2022-23, Gufo Labs
# ---------------------------------------------------------------------


from ..base import BasePlugin


class APlugin(BasePlugin):
    name = "a"

    def get_name(self: "APlugin") -> str:
        return self.name
