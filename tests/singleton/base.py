# ---------------------------------------------------------------------
# Gufo Labs Loader:
# Plugin base class for singleton tests
# ---------------------------------------------------------------------
# Copyright (C) 2022, Gufo Labs
# ---------------------------------------------------------------------


class BasePlugin(object):
    name: str

    def get_name(self) -> str:
        raise NotImplementedError
