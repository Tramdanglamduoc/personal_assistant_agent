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
