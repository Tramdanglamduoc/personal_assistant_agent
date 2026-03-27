from tools.translator_tool import TranslatorTool


def main():
    translator = TranslatorTool()

    print("=== Test 1: Valid translation (English to Vietnamese) ===")
    result1 = translator.execute({
        "text": "Good morning, how are you today?",
        "source_lang": "en",
        "target_lang": "vi"
    })
    print(result1)

    print("\n=== Test 2: Missing target language ===")
    result2 = translator.execute({
        "text": "Hello"
    })
    print(result2)

    print("\n=== Test 3: Empty text ===")
    result3 = translator.execute({
        "text": "",
        "target_lang": "vi"
    })
    print(result3)

    print("\n=== Test 4: English to Latvian ===")
    result4 = translator.execute({
        "text": "Hello",
        "source_lang": "en",
        "target_lang": "lv"
    })
    print(result4)

    print("\n=== Test 5: Latvian to English ===")
    result5 = translator.execute({
        "text": "Labrīt",
        "source_lang": "lv",
        "target_lang": "en"
    })
    print(result5)


if __name__ == "__main__":
    main()