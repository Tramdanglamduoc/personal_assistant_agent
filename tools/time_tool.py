from typing import Any, Dict
from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from tools.base_tool import BaseTool


class TimeTool(BaseTool):
    @property
    def name(self) -> str:
        return "time"

    def execute(self, args: Dict[str, Any]) -> str:
        timezone_name = args.get("timezone", "UTC").strip()

        if not timezone_name:
            timezone_name = "UTC"

        try:
            current_time = datetime.now(ZoneInfo(timezone_name))
            formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

            return f"Current time in {timezone_name}: {formatted_time}"

        except ZoneInfoNotFoundError:
            return (f"Time error: unknown timezone '{timezone_name}'. "
                    "Make sure 'tzdata' is installed (pip install tzdata).")
        except Exception as e:
            return f"Time error: {str(e)}"

    def get_declaration(self) -> Dict[str, Any]:
        return {
            "name": "time",
            "description": "Get the current time for a given timezone.",
            "parameters": {
                "type_": "OBJECT",
                "properties": {
                    "timezone": {
                        "type_": "STRING",
                        "description": (
                            "IANA timezone name, for example "
                            "'UTC', 'Europe/Riga', 'Asia/Tokyo', or 'America/New_York'"
                        )
                    }
                },
                "required": []
            }
        }