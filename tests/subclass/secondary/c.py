# ---------------------------------------------------------------------
# Gufo Labs Loader:
# c plugin class spoiled by decoy classes and variables
# ---------------------------------------------------------------------
# Copyright (C) 2022, Gufo Labs
# ---------------------------------------------------------------------

from ..base import BasePlugin


class Trash(object):
    ...


TRASH_VAR = 1


class CPlugin(BasePlugin):
    name = "c"

    def get_name(self) -> str:
        return self.name


class ATrash2(object):
    ...
