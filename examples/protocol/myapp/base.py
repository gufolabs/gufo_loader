from typing import Protocol, runtime_checkable


@runtime_checkable
class PluginProtocol(Protocol):
    """
    Protocol for our plugin
    """

    def __init__(self) -> None:
        ...

    def execute(self, x: int, y: int) -> int:
        """
        Plugin performs operation on two integers and returns integer
        """
        ...
