# ---------------------------------------------------------------------
# Gufo Labs Loader:
# Base plugin class for subclass tests
# ---------------------------------------------------------------------
# Copyright (C) 2022, Gufo Labs
# ---------------------------------------------------------------------


class BasePlugin(object):
    name: str

    def get_name(self) -> str:
        raise NotImplementedError
