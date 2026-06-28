# ---------------------------------------------------------------------
# Gufo Loader: c plugin spoiled by decoy classes and variables
# ---------------------------------------------------------------------
# Copyright (C) 2022-23, Gufo Labs
# ---------------------------------------------------------------------


class Trash: ...


TRASH_VAR = 1


class CPlugin:
    name = "c"

    def get_name(self) -> str:
        return self.name


class ATrash2: ...
