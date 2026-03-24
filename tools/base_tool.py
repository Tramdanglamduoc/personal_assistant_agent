from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseTool(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def execute(self, args: Dict[str, Any]) -> str:
        pass

    @abstractmethod
    def get_declaration(self) -> Dict[str, Any]:
        pass