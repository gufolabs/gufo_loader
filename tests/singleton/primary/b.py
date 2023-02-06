# ---------------------------------------------------------------------
# Gufo Loader: b plugin singleton instance
# ---------------------------------------------------------------------
# Copyright (C) 2022-23, Gufo Labs
# ---------------------------------------------------------------------


from ..base import BasePlugin


class BPlugin(BasePlugin):
    name = "b"

    def get_name(self: "BPlugin") -> str:
        return self.name


b_singleton = BPlugin()
