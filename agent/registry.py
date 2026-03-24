from typing import Dict, Any

class ToolRegistry:
    def __init__(self):
        self._tools = {}

    def register(self, tool):
        self._tools[tool.name] = tool

    def get_tool(self, name):
        return self._tools.get(name)

    def execute_tool(self, name: str, args: Dict[str, Any]):
        tool = self.get_tool(name)
        if not tool:
            return f"Error: tool '{name}' not found."
        return tool.execute(args)

    def get_all_declarations(self):
        return [tool.get_declaration() for tool in self._tools.values()]