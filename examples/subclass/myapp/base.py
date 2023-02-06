class BasePlugin(object):
    """Base class for our plugin."""

    def execute(self, x: int, y: int) -> int:
        """Plugin performs operation on two integers and returns integer."""
        ...
