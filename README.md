# Agent Workflow (Reason–Act–Observe)

This project implements an intelligent agent that follows a Reason–Act–Observe (ReAct) loop. Instead of responding directly to user input, the agent dynamically decides whether to answer or to use external tools.

## Workflow Overview
```
User Input
   ↓
Memory stores input
   ↓
Gemini receives prompt + tools
   ↓
Gemini decides:
   - respond directly
   - OR call a tool
   ↓
If tool is called:
   ToolRegistry executes tool
   ↓
Tool result returned to Gemini
   ↓
Gemini generates final response
   ↓
Memory stores the final response
```

## Setup Instructions

### Install dependencies:
```bash
pip install -r requirements.txt
```

`requirements.txt` includes:

- `requests` 
Used to send HTTP requests to external web services or APIs. In this project, it is useful for tools that need to communicate with online services, such as weather APIs or other external endpoints.

- - `google-genai`  
Official Google Gen AI SDK for accessing Gemini models from Python. In this project, it is used by the `TranslatorTool` to send text to the Gemini API and receive translated output.

- `tzdata`.
Provides time zone database support. This is required on some systems (especially Windows), where `Python’s zoneinfo module` depends on external timezone data.

## Gemini API Key Setup (Windows PowerShell)

You must set the `GEMINI_API_KEY` environment variable before running the main program.

### Set the API key permanently
Run this once in PowerShell:

```powershell
set GEMINI_API_KEY "YOUR_API_KEY"
```

**Notes: "YOUR_API_KEY" can get Gemini API key from Google AI Studio**

Then do all of the following
- Close all VS Code windows.
- Open VS Code again.
- Open a new terminal.

Check whether the key is available:
```powershell
echo $env:GEMINI_API_KEY
```

If the terminal prints your API key, then the key is now available for future terminals.

## Step-by-Step Explanation
### 1. User Input

The process begins when the user sends a message to the agent.

```bash
user_input = input("You: ")
response = agent.handle_user_input(user_input)
```

### 2. Memory Storage

The agent stores the user message to maintain conversation context.

```bash
self.memory.add_user_message(user_input)
```

This allows the agent to handle multi-turn conversations.

### 3. Gemini Processing

The agent sends:
- conversation history
- available tool declarations
to Gemini for reasoning.

```bash
response = self.model.generate_content(self.memory.get_history())
```

### 4. Decision Making (Reason)

Gemini decides between:

#### A. Direct Response

If no tool is needed:
```bash
User: Hello
→ Gemini: Hi! How can I help you?
```

#### B. Tool Invocation

If external information is needed:
```bash
User: What is 45 * 12?
→ Gemini decides to call calculator
```

### 5. Tool Execution (Act)

The agent uses the ToolRegistry to execute the tool:

```bash
tool_result = self.registry.execute_tool(tool_name, tool_args)
```

This design avoids hardcoded logic and follows the **Registry Pattern**.

### 6. Observation (Observe)

The tool result is sent back to Gemini as part of the conversation:
```bash
{
  "function_response": {
    "name": tool_name,
    "response": {"result": tool_result}
  }
}
```
This allows Gemini to continue reasoning.

### 7. Final Response Generation

Gemini is called again to generate the final natural-language answer:
```bash
final_response = self.model.generate_content(self.memory.get_history())
```

### 8. Memory Update

The final response is stored:
```bash
self.memory.add_model_message(final_text)
```
This ensures context is preserved for future interactions.

## Why Gemini May Be Called Twice

When tools are used:
1. First call → decide whether to use a tool
2. Tool executes
3. Second call → generate final answer

## Example: Weather Query

User:
```bash
What is the weather in Riga?
```

Flow:

1. Gemini decides to call weather(city="Riga")
2. Tool returns weather data
3. Gemini generates final answer using tool result


## Running tests

This project includes simple manual test files for checking whether the implemented tools work correctly.

---

### Manual Test: Run ToolRegistry checks
```powershell
python -m tests.test_registry
```

This test checks:
- registering tools correctly
- retrieving tools by name
- executing tools by name
- handling non-existent tools

Example output:
- === Test 1: Register tools ===
Registered calculator and time tools.
- === Test 2: Get tool by name ===
calculator -> <CalculatorTool object>
time -> <TimeTool object>
weather -> None
- === Test 3: Execute tool by name === <br>
15 <br>
Current time in Europe/Riga: <dynamic> <br>
- === Test 4: Execute non-existent tool ===
Error: requested tool 'weather' not found.

**Notes:**
**- The object memory addresses (e.g., <CalculatorTool object at ...>) may differ each run.**
**- The time value is dynamic and will change depending on when the test is executed.**
**- The goal of this test is to verify correct tool management behavior inside the registry.**

<br>
<br>

### Manual Test: Run all basic tool checks

```powershell
python -m tests.test_tools
```

This test runs sample checks for:
- CalculatorTool
- FileReaderTool
- TimeTool
- WeatherTool
- TranslatorTool

Example output:
- 19
- Contents of 'tests/notes.txt': Hello, this txt is for test_tools.
- Current time in Europe/Riga: <dynamic>
- Current weather in Riga, Latvia: <dynamic>
- Xin chào

**Note: the time and weather values may change depending on when the test is executed.**

---

### Manual Test: Run calculator-only checks
```powershell
python -m tests.test_calculator_tool
```

This test checks:
- valid expression handling
- missing argument handling
- empty expression handling
- invalid mathematical expression handling

Example output:
- 14
- Error: invalid arguments for calculator.
- Error: invalid arguments for calculator.
- Calculator error: invalid syntax (<string>, line 1) - invalid mathematical expression.

---

### Manual Test: Run file reader checks
```powershell
python -m tests.test_file_reader_tool
```

This test checks:
- reading a valid text file
- handling non-existing file paths
- handling empty file path input
- handling invalid data types
- rejecting unsupported file extensions

Example output:
- Contents of 'tests/notes.txt': Hello, this txt is for test_tools.
- Error: file 'tests/abcxyz.txt' does not exist.
- Error: invalid arguments for file reader.
- Error: invalid arguments for file reader.
- Error: unsupported file type. Supported types are .csv, .json, .md, .txt.

**Note: make sure the file `tests/notes.txt` exists and contains sample text.**

---

### Manual Test: Run time tool checks
```powershell
python -m tests.test_time_tool
```

This test checks:
- valid timezone handling
- default timezone behavior (UTC)
- handling of invalid timezone input

Example output:
- Current time in Europe/Riga: <dynamic>
- Current time in UTC: <dynamic>
- Time error: unknown timezone 'Mars/Unknown'. Make sure 'tzdata' is installed (pip install tzdata).

**Note: the time values will change depending on when the test is executed.**

---

### Manual Test: Run weather tool checks
```powershell
python -m tests.test_weather_tool
```

This test checks:
- valid city input (e.g., "Riga")
- handling of empty city input
- handling of non-existent or invalid city names

Example output:
- Current weather in Riga, Latvia: <dynamic>
- Weather error: 'city' is required.
- Weather error: could not find location 'asdkjasdkjasd'.

**Note: the weather values (temperature, wind speed, and description) may change depending on when the test is executed and API responses.**

---

### Manual Test: Run TranslatorTool test
```powershell
python -m tests.test_translator_tool
```

Test cases

This test checks:
- Valid translation (English → Vietnamese)
- Missing target language
- Empty text input
- English → Latvian translation
- Latvian → English translation

Example output:
- === Test 1: Valid translation (English to Vietnamese) === 
Chào buổi sáng, hôm nay bạn thế nào?


- === Test 2: Missing target language ===
Translation error: 'target_lang' is required.

- === Test 3: Empty text ===
Translation error: 'text' is required.

- === Test 4: English to Latvian ===
Labrīt

- === Test 5: Latvian to English ===
Good morning

**Notes:**
**The translation results may vary depending on the external API. Minor differences in translated text are expected.**
**The main goal is to verify:**
**- The tool runs without errors**
**- Proper error handling is implemented**
**- Valid translations return non-empty results**

## Key Design Concepts
- ReAct Pattern (Reason–Act–Observe)
- Tool-based architecture
- Registry Pattern (ToolRegistry)
- Memory-based context handling
- Separation of concerns

## Summary
```bash
Input → Memory → Gemini → Tool? → Tool Execution → Gemini → Final Answer → Memory
```
