from tools.time_tool import TimeTool


def main():
    time_tool = TimeTool()

    print("=== Test 1: Valid timezone ===")
    result1 = time_tool.execute({"timezone": "Europe/Riga"})
    print(result1)

    print("\n=== Test 2: Default timezone ===")
    result2 = time_tool.execute({})
    print(result2)

    print("\n=== Test 3: Invalid timezone ===")
    result3 = time_tool.execute({"timezone": "Mars/Unknown"})
    print(result3)


if __name__ == "__main__":
    main()