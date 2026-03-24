from typing import Any, Dict
import requests

from tools.base_tool import BaseTool


class TranslatorTool(BaseTool):
    @property
    def name(self) -> str:
        return "translator"

    def execute(self, args: Dict[str, Any]) -> str:
        text = args.get("text", "").strip()
        source_lang = args.get("source_lang", "auto").strip()
        target_lang = args.get("target_lang", "").strip()

        if not text:
            return "Translation error: 'text' is required."
        if not target_lang:
            return "Translation error: 'target_lang' is required."

        try:
            url = "https://api.mymemory.translated.net/get"
            params = {
                "q": text,
                "langpair": f"{source_lang}|{target_lang}"
            }

            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            translated_text = (
                data.get("responseData", {})
                .get("translatedText", "")
                .strip()
            )

            if not translated_text:
                return "Translation error: no translation was returned."

            return translated_text

        except requests.RequestException as e:
            return f"Translation API error: {str(e)}"
        except Exception as e:
            return f"Translation error: {str(e)}"

    def get_declaration(self) -> Dict[str, Any]:
        return {
            "name": "translator",
            "description": "Translate text from one language to another.",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The text to translate"
                    },
                    "source_lang": {
                        "type": "string",
                        "description": "Source language code, for example 'en', 'vi', or 'auto'"
                    },
                    "target_lang": {
                        "type": "string",
                        "description": "Target language code, for example 'en', 'vi', 'fr'"
                    }
                },
                "required": ["text", "target_lang"]
            }
        }