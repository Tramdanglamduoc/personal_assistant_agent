from tools.calculator_tool import CalculatorTool

calculator = CalculatorTool()

print(calculator.execute({"expression": "2 + 3 * 4"}))
print(calculator.execute({"expression": "5/0"}))
print(calculator.execute({}))
print(calculator.execute({"expression": ""}))
print(calculator.execute({"expression": "2 +"}))

