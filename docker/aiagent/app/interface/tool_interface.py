from abc import ABC, abstractmethod

class ToolInterface(ABC):
    """Abstract interface for a general-purpose tool (e.g., QuestDB, Grafana, etc.)."""

    @abstractmethod
    def execute_query(self, query: str) -> str:
        """
        Executes a query or command and returns a string result.
        """
        pass
