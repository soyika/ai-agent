from abc import ABC, abstractmethod
from typing import Optional, Any


class BaseAgent(ABC):
    def __init__(self, name: str, description: str, capabilities: list[str]):
        self.name = name
        self.description = description
        self.capabilities = capabilities

    @abstractmethod
    async def execute(self, task: str, context: Optional[dict] = None) -> Any:
        pass

    def __repr__(self):
        return f"<Agent: {self.name}>"
