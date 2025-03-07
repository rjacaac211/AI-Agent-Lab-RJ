from abc import ABC, abstractmethod

class ToolInterface(ABC):
    """Abstract interface for a general-purpose tool (QuestDB, Grafana, VSCode, etc.)."""

    @abstractmethod
    def execute_tool(self, query: str) -> str:
        """
        Executes a tool and returns a string result.
        """
        pass
