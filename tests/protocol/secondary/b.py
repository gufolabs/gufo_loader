# ---------------------------------------------------------------------
# Gufo Loader: b plugin spoiler. Must be overriden from primary/b.py
# ---------------------------------------------------------------------
# Copyright (C) 2022-23, Gufo Labs
# ---------------------------------------------------------------------


class BPlugin(object):
    name = "b?"

    def get_name(self: "BPlugin") -> str:
        return self.name
