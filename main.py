from agent.agent import Agent
from agent.memory import MemoryManager
from agent.registry import ToolRegistry

from tools.calculator_tool import CalculatorTool
from tools.time_tool import TimeTool
from tools.weather_tool import WeatherTool
from tools.translator_tool import TranslatorTool
from tools.file_reader_tool import FileReaderTool


def build_agent() -> Agent:
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

    print("Personal Assistant Agent started. Type 'exit' to quit.")

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() == "exit":
            print("Agent: Goodbye!")
            break

        if not user_input:
            print("Agent: Please enter a message.")
            continue

        response = agent.handle_user_input(user_input)
        print(f"Agent: {response}")


if __name__ == "__main__":
    main()