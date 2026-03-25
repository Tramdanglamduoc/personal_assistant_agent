from typing import Any, Dict
from tools.base_tool import BaseTool

class CalculatorTool(BaseTool):
    @property
    def name(self) -> str:
        return "calculator"

    def execute(self, args):
        expression = args.get("expression", "")

        if expression is None:
            return "Error: invalid arguments for calculator."

        if not isinstance(expression, str):
            return "Error: invalid arguments for calculator."

        expression = expression.strip()
        if not expression:
            return "Error: invalid arguments for calculator."

        try:
            result = eval(expression, {"__builtins__": {}})
            return str(result)
        except Exception as e:
            return f"Calculator error: {str(e)} - invalid mathematical expression."

    def get_declaration(self):
        return {
            "name": "calculator",
            "description": "Evaluate a mathematical expression.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Mathematical expression to evaluate"
                    }
                },
                "required": ["expression"]
            }
        }