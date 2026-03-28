from typing import Any, Dict
from pathlib import Path

from tools.base_tool import BaseTool


class FileReaderTool(BaseTool):
    ALLOWED_EXTENSIONS = {".txt", ".md", ".csv", ".json"}
    MAX_FILE_SIZE_BYTES = 100_000  # about 100 KB

    @property
    def name(self) -> str:
        return "file_reader"

    def execute(self, args: Dict[str, Any]) -> str:
        file_path = args.get("file_path")

        if file_path is None:
            return "Error: invalid arguments for file reader."

        if not isinstance(file_path, str):
            return "Error: invalid arguments for file reader."

        file_path = file_path.strip()
        if not file_path:
            return "Error: invalid arguments for file reader."

        try:
            path = Path(file_path).resolve()

            # Optional safety check: block parent traversal patterns
            if ".." in Path(file_path).parts:
                return "Error: parent directory traversal is not allowed."

            if not path.exists():
                return f"Error: file '{file_path}' does not exist."

            if not path.is_file():
                return f"Error: '{file_path}' is not a file."

            if path.suffix.lower() not in self.ALLOWED_EXTENSIONS:
                allowed_list = ", ".join(sorted(self.ALLOWED_EXTENSIONS))
                return (
                    f"Error: unsupported file type. Supported types are {allowed_list}."
                )

            file_size = path.stat().st_size
            if file_size > self.MAX_FILE_SIZE_BYTES:
                return (
                    "Error: file is too large to read safely. "
                    "Please use a smaller text file."
                )

            content = path.read_text(encoding="utf-8")

            if not content.strip():
                return f"Error: file '{file_path}' is empty."

            return f"Contents of '{file_path}':\n{content}"

        except UnicodeDecodeError:
            return f"Error: could not decode file '{file_path}' as UTF-8."
        except PermissionError:
            return f"Error: permission denied when reading '{file_path}'."
        except OSError as e:
            print(f"[FileReaderTool OSError] {e}")
            return "Error: file reader failed during execution."
        except Exception as e:
            print(f"[FileReaderTool Error] {e}")
            return "Error: file reader failed during execution."

    def get_declaration(self) -> Dict[str, Any]:
        return {
            "name": "file_reader",
            "description": "Read the contents of a local text-based file.",
            "parameters": {
                "type_": "OBJECT",
                "properties": {
                    "file_path": {
                        "type_": "STRING",
                        "description": "Path to a local file such as 'notes.txt'"
                    }
                },
                "required": ["file_path"]
            }
        }