# ---------------------------------------------------------------------
# Gufo Loader: c plugin spoiled by decoy classes and variables
# ---------------------------------------------------------------------
# Copyright (C) 2022-23, Gufo Labs
# ---------------------------------------------------------------------


class Trash(object):
    ...


TRASH_VAR = 1


class CPlugin(object):
    name = "c"

    def get_name(self: "CPlugin") -> str:
        return self.name


class ATrash2(object):
    ...
