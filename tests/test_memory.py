from agent.memory import MemoryManager


def main():
    memory = MemoryManager()

    print("=== Test 1: Initial history ===")
    print(memory.get_history())

    print("\n=== Test 2: Add user and model messages ===")
    memory.add_user_message("Hello")
    memory.add_model_message("Hi there!")
    memory.add_user_message("What is my name?")
    memory.add_model_message("I do not know your name yet.")
    print(memory.get_history())

    print("\n=== Test 3: Clear memory ===")
    memory.clear()
    print(memory.get_history())


if __name__ == "__main__":
    main()