# ---------------------------------------------------------------------
# Gufo Loader: Plugin base class for attribute tests
# ---------------------------------------------------------------------
# Copyright (C) 2026, Gufo Labs
# ---------------------------------------------------------------------


class BasePlugin:
    name: str

    def get_name(self) -> str:
        raise NotImplementedError
