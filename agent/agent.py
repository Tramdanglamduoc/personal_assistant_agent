import google.generativeai as genai

from config import GEMINI_API_KEY, MODEL_NAME
from agent.memory import MemoryManager
from agent.registry import ToolRegistry


class Agent:
    def __init__(self, memory: MemoryManager, registry: ToolRegistry):
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is not set.")

        self.memory = memory
        self.registry = registry

        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel(
            model_name=MODEL_NAME,
            tools=self.registry.get_all_declarations()
        )

    def handle_user_input(self, user_input: str) -> str:
        try:
            self.memory.add_user_message(user_input)

            response = self.model.generate_content(
                self.memory.get_history()
            )

            candidate = response.candidates[0]
            content = candidate.content

            for part in content.parts:
                if hasattr(part, "function_call") and part.function_call:
                    tool_name = part.function_call.name
                    tool_args = dict(part.function_call.args)

                    tool_result = self.registry.execute_tool(tool_name, tool_args)

                    self.memory.history.append({
                        "role": "model",
                        "parts": [part]
                    })

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
                        final_response = self.model.generate_content(
                            self.memory.get_history()
                        )

                    except Exception as e:
                        print(f"[Gemini Final Response Error] {e}")
                        return "Sorry, the AI service is temporarily unavailable."
                    
                    final_text = self._extract_text_response(final_response)
                    self.memory.add_model_message(final_text)
                    return final_text

            direct_text = self._extract_text_response(response)
            self.memory.add_model_message(direct_text)
            return direct_text

        except Exception as e:
            print(f"[Agent Error] {e}")
            return "Sorry, the AI service is temporarily unavailable."

    def _extract_text_response(self, response) -> str:
        try:
            texts = []

            for part in response.candidates[0].content.parts:
                if hasattr(part, "text") and part.text:
                    texts.append(part.text)

            if texts:
                return "\n".join(texts)

            return "No text response was generated."

        except Exception as e:
            return f"Response parsing error: {str(e)}"