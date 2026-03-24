class CalculatorTool(BaseTool):
    @property
    def name(self) -> str:
        return "calculator"

    def execute(self, args):
        expression = args.get("expression", "")
        try:
            result = eval(expression, {"__builtins__": {}})
            return str(result)
        except Exception as e:
            return f"Calculator error: {str(e)}"

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