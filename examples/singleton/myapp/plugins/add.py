from ..base import BasePlugin


class AddPlugin(BasePlugin):
    def execute(self, x: int, y: int) -> int:
        return x + y


add_plugin = AddPlugin()
