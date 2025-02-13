from abc import ABC, abstractmethod
from typing import Any, List, Dict

class MemoryInterface(ABC):
    """
    Abstract interface for managing conversational memory.
    """
    @abstractmethod
    def load_conversation(self, session_id: str) -> List[Dict[str, Any]]:
        """
        Retrieve the conversation history for a given session_id.
        Returns a list of messages, e.g.:
        [
          {"role": "user", "content": "Hello"},
          {"role": "agent", "content": "Hi there! How can I help?"}
        ]
        """
        pass

    @abstractmethod
    def save_user_message(self, session_id: str, message: str) -> None:
        """Store a user message in the conversation context."""
        pass

    @abstractmethod
    def save_agent_message(self, session_id: str, message: str) -> None:
        """Store an agent message in the conversation context."""
        pass

    @abstractmethod
    def clear_conversation(self, session_id: str) -> None:
        """Clear the conversation for a specific session."""
        pass
