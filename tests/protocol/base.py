# ---------------------------------------------------------------------
# Gufo Labs Loader:
# Named protocol for the protocol tests
# ---------------------------------------------------------------------
# Copyright (C) 2022, Gufo Labs
# ---------------------------------------------------------------------

from typing import Protocol, runtime_checkable


@runtime_checkable
class Named(Protocol):
    def __init__(self):
        ...

    def get_name(self) -> str:
        ...
