# ---------------------------------------------------------------------
# Gufo Loader: Plugin base class for singleton tests
# ---------------------------------------------------------------------
# Copyright (C) 2022-23, Gufo Labs
# ---------------------------------------------------------------------


class BasePlugin(object):
    name: str

    def get_name(self: "BasePlugin") -> str:
        raise NotImplementedError
