from langchain_core.tools import BaseTool
import psycopg2 as pg
from aiagent.app.interface import ToolInterface
from aiagent.config import Config

class QueryQuestDBTool(BaseTool, ToolInterface):
    """A class-based LangChain tool for QuestDB queries."""

    name: str = "QueryQuestDBTool"
    description: str = "Execute queries against QuestDB."

    def _run(self, tool_input: str) -> str:
        """
        Synced run method. 
        tool_input = your SQL query string.
        """
        try:
            with pg.connect(Config.QDB_CONN_STR) as conn:
                with conn.cursor() as cur:
                    cur.execute(tool_input)
                    rows = cur.fetchall()
                    cols = [desc[0] for desc in cur.description]
                    results = [dict(zip(cols, row)) for row in rows]
            return f"Query Results: {results}"
        except Exception as e:
            return f"Database query failed: {str(e)}"

    async def _arun(self, tool_input: str) -> str:
        """Asynchronous version if needed."""
        raise NotImplementedError("Async not implemented for QuestDBTool.")

    def execute_query(self, query: str) -> str:
        """
        A direct interface method for external calls,
        which under the hood calls `_run`.
        """
        return self._run(query)