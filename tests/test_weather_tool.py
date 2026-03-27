from tools.weather_tool import WeatherTool


def main():
    weather_tool = WeatherTool()

    print("=== Test 1: Valid city ===")
    result1 = weather_tool.execute({"city": "Riga"})
    print(result1)

    print("\n=== Test 2: Empty city ===")
    result2 = weather_tool.execute({"city": ""})
    print(result2)

    print("\n=== Test 3: Fake city ===")
    result3 = weather_tool.execute({"city": "asdkjasdkjasd"})
    print(result3)


if __name__ == "__main__":
    main()