from tools.calculator_tool import CalculatorTool
from tools.file_reader_tool import FileReaderTool
from tools.time_tool import TimeTool
from tools.weather_tool import WeatherTool
from tools.translator_tool import TranslatorTool


def main():
    calculator = CalculatorTool()
    file_reader = FileReaderTool()
    time_tool = TimeTool()
    weather_tool = WeatherTool()
    translator = TranslatorTool()

    print(calculator.execute({"expression": "5 + 7 * 2"}))
    print(file_reader.execute({"file_path": "tests/notes.txt"}))
    print(time_tool.execute({"timezone": "Europe/Riga"}))
    print(weather_tool.execute({"city": "Riga"}))
    print(translator.execute({
        "text": "Hello",
        "source_lang": "en",
        "target_lang": "vi"
    }))


if __name__ == "__main__":
    main()