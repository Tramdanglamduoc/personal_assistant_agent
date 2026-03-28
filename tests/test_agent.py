from agent.agent import Agent
from agent.memory import MemoryManager
from agent.registry import ToolRegistry

from tools.calculator_tool import CalculatorTool
from tools.time_tool import TimeTool
from tools.weather_tool import WeatherTool
from tools.translator_tool import TranslatorTool
from tools.file_reader_tool import FileReaderTool


def build_agent():
    memory = MemoryManager()
    registry = ToolRegistry()

    registry.register(CalculatorTool())
    registry.register(TimeTool())
    registry.register(WeatherTool())
    registry.register(TranslatorTool())
    registry.register(FileReaderTool())

    return Agent(memory=memory, registry=registry)


def main():
    agent = build_agent()

    print("=== Test 1: Direct response ===")
    print(agent.handle_user_input("Hello"))

    print("\n=== Test 2: Calculator ===")
    print(agent.handle_user_input("What is 12 * 8 + 1?"))

    print("\n=== Test 3: Time ===")
    print(agent.handle_user_input("What time is it in Europe/Riga?"))

    print("\n=== Test 4: Translation ===")
    print(agent.handle_user_input("Translate 'Good night' to Vietnamese."))

    print("\n=== Test 5: File Reader ===")
    print(agent.handle_user_input("Read tests/notes.txt"))


if __name__ == "__main__":
    main()