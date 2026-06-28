# ---------------------------------------------------------------------
# Gufo Loader: Base plugin class for subclass tests
# ---------------------------------------------------------------------
# Copyright (C) 2022-23, Gufo Labs
# ---------------------------------------------------------------------


class BasePlugin:
    name: str

    def get_name(self) -> str:
        raise NotImplementedError
