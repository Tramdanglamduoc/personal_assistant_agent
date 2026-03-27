from agent.registry import ToolRegistry
from tools.calculator_tool import CalculatorTool
from tools.time_tool import TimeTool


def main():
    registry = ToolRegistry()

    print("=== Test 1: Register tools ===")
    registry.register(CalculatorTool())
    registry.register(TimeTool())
    print("Registered calculator and time tools.")

    print("\n=== Test 2: Get tool by name ===")
    print("calculator ->", registry.get_tool("calculator"))
    print("time ->", registry.get_tool("time"))
    print("weather ->", registry.get_tool("weather"))

    print("\n=== Test 3: Execute tool by name ===")
    print(registry.execute_tool("calculator", {"expression": "10 + 5"}))
    print(registry.execute_tool("time", {"timezone": "Europe/Riga"}))

    print("\n=== Test 4: Execute non-existent tool ===")
    print(registry.execute_tool("unknown", {"city": "Riga"}))


if __name__ == "__main__":
    main()