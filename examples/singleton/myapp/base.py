from abc import ABC, abstractmethod


class BasePlugin(ABC):
    """Base class for our plugin."""

    @abstractmethod
    def execute(self, x: int, y: int) -> int:
        """Plugin performs operation on two integers and returns integer."""
