from typing import Any, Dict
from pathlib import Path

from tools.base_tool import BaseTool


class FileReaderTool(BaseTool):
    @property
    def name(self) -> str:
        return "file_reader"

    def execute(self, args: Dict[str, Any]) -> str:
        file_path = args.get("file_path", "").strip()

        if not file_path:
            return "File reader error: 'file_path' is required."

        try:
            path = Path(file_path)

            if not path.exists():
                return f"File reader error: file '{file_path}' does not exist."

            if not path.is_file():
                return f"File reader error: '{file_path}' is not a file."

            if path.suffix.lower() not in [".txt", ".md", ".csv", ".json"]:
                return (
                    "File reader error: unsupported file type. "
                    "Supported types are .txt, .md, .csv, .json."
                )

            content = path.read_text(encoding="utf-8")

            if not content.strip():
                return f"File reader result: file '{file_path}' is empty."

            return f"Contents of '{file_path}':\n{content}"

        except UnicodeDecodeError:
            return f"File reader error: could not decode file '{file_path}' as UTF-8."
        except Exception as e:
            return f"File reader error: {str(e)}"

    def get_declaration(self) -> Dict[str, Any]:
        return {
            "name": "file_reader",
            "description": "Read the contents of a local text-based file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the local file, for example 'notes.txt'"
                    }
                },
                "required": ["file_path"]
            }
        }