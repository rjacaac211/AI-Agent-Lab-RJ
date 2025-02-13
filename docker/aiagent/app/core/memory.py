from typing import List, Dict, Any
from aiagent.app.interface import MemoryInterface

class WindowMemoryManager(MemoryInterface):
    """
    An ephemral, in-memory conversation store with a fixed window size.
    Stores up to `window_size * 2` messages (i.e., user+assistant pairs).
    """

    def __init__(self, window_size: int = 10):
        self.window_size = window_size
        # Dictionary: {session_id: [ {role: "...", content: "..."}, ... ] }
        self._storage: Dict[str, List[Dict[str, Any]]] = {}

    def load_conversation(self, session_id: str) -> List[Dict[str, Any]]:
        # Return a *copy* of the conversation to avoid external mutations
        return list (self._storage.get(session_id, []))

    def save_user_message(self, session_id: str, message: str) -> None:
        conv = self._storage.setdefault(session_id, [])
        conv.append({"role": "user", "content": message})
        self._prune(session_id)

    def save_agent_message(self, session_id: str, message: str) -> None:
        conv = self._storage.setdefault(session_id, [])
        conv.append({"role": "agent", "content": message})
        self._prune(session_id)

    def clear_conversation(self, session_id: str) -> None:
        if session_id in self._storage:
            del self._storage[session_id]
    
    def _prune(self, session_id: str) -> None:
        """
        Ensures the conversation doesn't exceed window_size*2 messages.
        """
        conv = self._storage[session_id]
        max_messages = self.window_size * 2
        if len(conv) > max_messages:
            overflow = len(conv) - max_messages
            self._storage[session_id] = conv[overflow:]