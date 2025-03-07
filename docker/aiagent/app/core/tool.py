import requests
import psycopg2 as pg
from langchain_core.tools import BaseTool

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

    def execute_tool(self, query: str) -> str:
        """
        A direct interface method for external calls,
        which under the hood calls `_run`.
        """
        return self._run(query)


class GrafanaDashboardTool(BaseTool, ToolInterface):
    """A tool for interacting with Grafana dashboards via its HTTP API.
    
    Supports:
      - Creating a new dashboard.
      - Deleting a dashboard by UID or by Name.
    """
    name: str = "GrafanaDashboardTool"
    description: str = "Manage Grafana dashboards (create and delete)."

    def create_dashboard(self, new_title: str) -> dict:
        """
        Creates a new dashboard with the provided title.
        """
        dashboard_payload = {
            "id": None,
            "uid": None,
            "title": new_title,
            "tags": [],
            "timezone": "browser",
            "schemaVersion": 38,
            "refresh": "5s"
        }
        payload = {
            "dashboard": dashboard_payload,
            "folderId": 0,
            "message": "Dashboard created via AI Agent",
            "overwrite": False
        }
        url = f"{Config.GRAFANA_API_URL}/api/dashboards/db"
        headers = {
            "Authorization": f"Bearer {Config.GRAFANA_API_TOKEN}",
            "Content-Type": "application/json",
            "X-Grafana-Org-Id": "1"
        }
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()

    def fetch_dashboard(self, uid: str) -> dict:
        """Fetch a dashboard by its UID."""
        url = f"{Config.GRAFANA_API_URL}/api/dashboards/uid/{uid}"
        headers = {
            "Authorization": f"Bearer {Config.GRAFANA_API_TOKEN}",
            "Content-Type": "application/json",
            "X-Grafana-Org-Id": "1"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def delete_dashboard_by_uid(self, uid: str) -> dict:
        """Delete a dashboard by its UID."""
        url = f"{Config.GRAFANA_API_URL}/api/dashboards/uid/{uid}"
        headers = {
            "Authorization": f"Bearer {Config.GRAFANA_API_TOKEN}",
            "Content-Type": "application/json",
            "X-Grafana-Org-Id": "1"
        }
        response = requests.delete(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def search_dashboard_by_name(self, dashboard_name: str) -> dict:
        """
        Search for a dashboard by its name using Grafana's search API.
        Returns the first dashboard whose title matches (case-insensitive).
        """
        url = f"{Config.GRAFANA_API_URL}/api/search?query={dashboard_name}"
        headers = {
            "Authorization": f"Bearer {Config.GRAFANA_API_TOKEN}",
            "Content-Type": "application/json",
            "X-Grafana-Org-Id": "1"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        results = response.json()
        for item in results:
            # Check that the item represents a dashboard and the title matches case-insensitively.
            if item.get("type") == "dash-db" and item.get("title", "").lower() == dashboard_name.lower():
                return item
        return None

    def _run(self, tool_input: str) -> str:
        """
        Expects tool_input in one of the following formats:
          - "create:<new_title>" to create a new dashboard.
          - "delete:<uid>" to delete an existing dashboard by UID.
          - "deleteByName:<dashboard_name>" to delete a dashboard by searching its name.
        """
        if tool_input.startswith("create:"):
            try:
                _, new_title = tool_input.split(":", 1)
                new_title = new_title.strip()
                create_result = self.create_dashboard(new_title)
                return f"Dashboard created: {create_result}"
            except Exception as e:
                return f"Failed to create dashboard: {str(e)}"
        elif tool_input.startswith("delete:"):
            try:
                _, uid = tool_input.split(":", 1)
                uid = uid.strip()
                delete_result = self.delete_dashboard_by_uid(uid)
                return f"Dashboard deleted: {delete_result}"
            except Exception as e:
                return f"Failed to delete dashboard: {str(e)}"
        elif tool_input.startswith("deleteByName:"):
            try:
                _, dashboard_name = tool_input.split(":", 1)
                dashboard_name = dashboard_name.strip()
                search_result = self.search_dashboard_by_name(dashboard_name)
                if not search_result:
                    return f"Dashboard named '{dashboard_name}' not found."
                uid = search_result.get("uid")
                if not uid:
                    return f"Dashboard named '{dashboard_name}' not found."
                delete_result = self.delete_dashboard_by_uid(uid)
                return f"Dashboard deleted: {delete_result}"
            except Exception as e:
                return f"Failed to delete dashboard by name: {str(e)}"
        else:
            return ("Invalid Grafana command. Use one of the following formats:\n"
                    "  create:<new_title>\n"
                    "  delete:<uid>\n"
                    "  deleteByName:<dashboard_name>")

    async def _arun(self, tool_input: str) -> str:
        raise NotImplementedError("Async not implemented for GrafanaDashboardTool.")

    def execute_tool(self, query: str) -> str:
        return self._run(query)


class VSCodeIntegrationTool(BaseTool, ToolInterface):
    """
    A tool for integrating the AI Agent with VSCode via a WebSocket interface.
    Supported Commands:
      - "create:<filepath>:<content>" to create a file.
      - "delete:<filepath>" to delete a file.
    """

    name: str = "VSCodeIntegrationTool"
    description: str = "Integrates with VSCode via WebSocket to manage files."

    def _run(self, tool_input: str) -> str:
        ws_url = Config.VSCODE_WS_URL
        try:
            # If tool_input is not a string, convert it to JSON.
            if not isinstance(tool_input, str):
                tool_input = json.dumps(tool_input)
            ws = websocket.create_connection(ws_url, timeout=10)
            ws.send(tool_input)
            response = ws.recv()
            ws.close()
            return response
        except Exception as e:
            return f"VSCode WebSocket error: {str(e)}"
    
    async def _arun(self, tool_input: str) -> str:
        raise NotImplementedError("Async not implemented for VSCodeIntegrationTool.")

    def execute_tool(self, query: str) -> str:
        return self._run(query)