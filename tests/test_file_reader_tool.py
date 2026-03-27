from tools.file_reader_tool import FileReaderTool


def main():
    file_reader = FileReaderTool()

    print("=== Normal case ===")
    print(file_reader.execute({"file_path": "tests/notes.txt"}))
    print()

    print("=== File does not exist ===")
    print(file_reader.execute({"file_path": "tests/abcxyz.txt"}))
    print()

    print("=== Empty path ===")
    print(file_reader.execute({"file_path": ""}))
    print()

    print("=== Wrong data type ===")
    print(file_reader.execute({"file_path": 123}))
    print()

    print("=== Unsupported extension ===")
    print(file_reader.execute({"file_path": "tests/image.png"}))
    print()


if __name__ == "__main__":
    main()