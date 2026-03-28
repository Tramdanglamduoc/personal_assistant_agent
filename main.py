from agent.agent import Agent
from agent.memory import MemoryManager
from agent.registry import ToolRegistry

from tools.calculator_tool import CalculatorTool
from tools.time_tool import TimeTool
from tools.weather_tool import WeatherTool
from tools.translator_tool import TranslatorTool
from tools.file_reader_tool import FileReaderTool

from utils.observer import LoggingObserver, TokenUsageObserver   # 👈 thêm


def build_agent() -> Agent:
    memory = MemoryManager()
    registry = ToolRegistry()

    registry.register(CalculatorTool())
    registry.register(TimeTool())
    registry.register(WeatherTool())
    registry.register(TranslatorTool())
    registry.register(FileReaderTool())

    agent = Agent(memory=memory, registry=registry)

    agent.add_observer(LoggingObserver())
    token_observer = TokenUsageObserver()
    agent.add_observer(token_observer)

    return agent, token_observer   


def main():
    agent, token_observer = build_agent()

    print("Personal Assistant Agent started. Type 'exit' to quit.")

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() == "exit":
            print("Agent: Goodbye!")
            print(token_observer.get_summary())   
            break

        if not user_input:
            print("Agent: Please enter a message.")
            continue

        response = agent.handle_user_input(user_input)
        print(f"Agent: {response}")


if __name__ == "__main__":
    main()