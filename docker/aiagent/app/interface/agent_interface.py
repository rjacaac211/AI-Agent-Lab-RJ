from abc import ABC, abstractmethod

class AgentInterface(ABC):
    """Abstract interface for a single AI agent."""

    @abstractmethod
    def invoke(self, user_message: str) -> str:
        """
        Process user input (a string) and return a final string response.
        """
        pass