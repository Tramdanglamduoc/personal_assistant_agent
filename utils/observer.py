from abc import ABC, abstractmethod
from typing import Any


class AgentObserver(ABC):
    """Abstract base class for all observers."""

    @abstractmethod
    def on_event(self, event_type: str, data: Any) -> None:
        pass


class LoggingObserver(AgentObserver):
    """Logs all agent events to the console."""

    def on_event(self, event_type: str, data: Any) -> None:
        if event_type == "tool_called":
            print(f"[LOG] Tool called: '{data['tool_name']}' with args: {data['args']}")
        elif event_type == "tool_result":
            print(f"[LOG] Tool result from '{data['tool_name']}': {data['result']}")
        elif event_type == "response_generated":
            print(f"[LOG] Response generated ({len(data['text'])} chars)")
        elif event_type == "error_occurred":
            print(f"[LOG] Error: {data['message']}")


class TokenUsageObserver(AgentObserver):
    """Tracks approximate token/character usage across the session."""

    def __init__(self):
        self.total_chars = 0
        self.tool_call_count = 0

    def on_event(self, event_type: str, data: Any) -> None:
        if event_type == "response_generated":
            self.total_chars += len(data["text"])
        elif event_type == "tool_called":
            self.tool_call_count += 1

    def get_summary(self) -> str:
        return (
            f"[Stats] Tool calls this session: {self.tool_call_count} | "
            f"Total response chars: {self.total_chars}"
        )