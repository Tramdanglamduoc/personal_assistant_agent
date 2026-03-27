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

`requirements.txt` includes `tzdata`.

This is required on some systems (especially Windows), where `Python’s zoneinfo module` depends on external timezone data.


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

### Run all basic tool checks

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
