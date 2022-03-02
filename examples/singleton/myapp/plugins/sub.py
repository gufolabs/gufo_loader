from ..base import BasePlugin


class SubPlugin(BasePlugin):
    def execute(self, x: int, y: int) -> int:
        return x - y


sub_plugin = SubPlugin()
