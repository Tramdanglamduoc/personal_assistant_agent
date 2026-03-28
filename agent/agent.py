import google.generativeai as genai
from typing import List

from config import GEMINI_API_KEY, MODEL_NAME
from agent.memory import MemoryManager
from agent.registry import ToolRegistry
from utils.observer import AgentObserver   # 👈 thêm


class Agent:
    def __init__(self, memory: MemoryManager, registry: ToolRegistry):
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is not set.")

        self.memory = memory
        self.registry = registry
        self._observers: List[AgentObserver] = []   # 👈 thêm

        genai.configure(api_key=GEMINI_API_KEY)

        declarations = self.registry.get_all_declarations()
        self.model = genai.GenerativeModel(
            model_name=MODEL_NAME,
            tools=declarations
        )

    # 👇 thêm 2 method này
    def add_observer(self, observer: AgentObserver) -> None:
        self._observers.append(observer)

    def _notify(self, event_type: str, data) -> None:
        for observer in self._observers:
            observer.on_event(event_type, data)

    def handle_user_input(self, user_input: str) -> str:
        try:
            self.memory.add_user_message(user_input)

            response = self.model.generate_content(self.memory.get_history())

            candidate = response.candidates[0]
            content = candidate.content

            for part in content.parts:
                if hasattr(part, "function_call") and part.function_call:
                    tool_name = part.function_call.name
                    tool_args = dict(part.function_call.args)

                    # 👇 notify khi tool được gọi
                    self._notify("tool_called", {"tool_name": tool_name, "args": tool_args})

                    tool_result = self.registry.execute_tool(tool_name, tool_args)

                    # 👇 notify khi có kết quả tool
                    self._notify("tool_result", {"tool_name": tool_name, "result": tool_result})

                    self.memory.history.append({"role": "model", "parts": [part]})
                    self.memory.history.append({
                        "role": "user",
                        "parts": [{
                            "function_response": {
                                "name": tool_name,
                                "response": {"result": tool_result}
                            }
                        }]
                    })

                    try:
                        final_response = self.model.generate_content(self.memory.get_history())
                    except Exception as e:
                        self._notify("error_occurred", {"message": str(e)})   # 👈
                        return "Sorry, the AI service is temporarily unavailable."

                    final_text = self._extract_text_response(final_response)
                    self.memory.add_model_message(final_text)

                    # 👇 notify khi có response cuối
                    self._notify("response_generated", {"text": final_text})
                    return final_text

            direct_text = self._extract_text_response(response)
            self.memory.add_model_message(direct_text)
            self._notify("response_generated", {"text": direct_text})   # 👈
            return direct_text

        except Exception as e:
            self._notify("error_occurred", {"message": str(e)})   # 👈
            return "Sorry, the AI service is temporarily unavailable."

    def _extract_text_response(self, response) -> str:
        try:
            texts = []
            for part in response.candidates[0].content.parts:
                if hasattr(part, "text") and part.text:
                    texts.append(part.text)
            return "\n".join(texts) if texts else "No text response was generated."
        except Exception as e:
            return f"Response parsing error: {str(e)}"