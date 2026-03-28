from typing import Any, Dict
import os

from google import genai
from tools.base_tool import BaseTool


class TranslatorTool(BaseTool):
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")

        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables.")

        self.client = genai.Client(api_key=self.api_key)

    @property
    def name(self) -> str:
        return "translator"

    def execute(self, args: Dict[str, Any]) -> str:
        text = str(args.get("text", "")).strip()
        source_lang = str(args.get("source_lang", "auto")).strip()
        target_lang = str(args.get("target_lang", "")).strip()

        if not text:
            return "Translation error: 'text' is required."
        if not target_lang:
            return "Translation error: 'target_lang' is required."

        try:
            if source_lang.lower() == "auto":
                prompt = (
                    f"Translate the following text into {target_lang}. "
                    f"Return only the translation:\n\n{text}"
                )
            else:
                prompt = (
                    f"Translate the following text from {source_lang} to {target_lang}. "
                    f"Return only the translation:\n\n{text}"
                )

            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
            )

            translated_text = (response.text or "").strip()

            if not translated_text:
                return "Translation error: no translation was returned."

            return translated_text

        except Exception as e:
            return f"Translation error: {str(e)}"

    def get_declaration(self) -> Dict[str, Any]:
        return {
            "name": "translator",
            "description": "Translate text from one language to another.",
            "parameters": {
                "type_": "OBJECT",
                "properties": {
                    "text": {
                        "type_": "STRING",
                        "description": "The text to translate"
                    },
                    "source_lang": {
                        "type_": "STRING",
                        "description": "Source language code, for example 'en', 'vi', or 'auto'"
                    },
                    "target_lang": {
                        "type_": "STRING",
                        "description": "Target language code, for example 'en', 'vi', 'fr'"
                    }
                },
                "required": ["text", "target_lang"]
            }
        }