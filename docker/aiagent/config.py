import os
import requests

class Config:
    """
    Centralized configuration for the AI Agent.
    """
    # Flask Secret Key
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default_secret_key')

    # QuestDB Configuration
    QDB_PG_USER = os.environ.get('QDB_PG_USER', 'admin')
    QDB_PG_PASSWORD = os.environ.get('QDB_PG_PASSWORD', 'quest')
    QDB_PG_NAME = os.environ.get('QDB_PG_NAME', 'qdb')
    QDB_PG_HOST = os.environ.get('QDB_PG_HOST', 'localhost')
    QDB_PG_PORT = os.environ.get('QDB_PG_PORT', '8812')

    # Construct QuestDB conenction string
    QDB_CONN_STR = (
        f"user={QDB_PG_USER} password={QDB_PG_PASSWORD} "
        f"host={QDB_PG_HOST} port={QDB_PG_PORT} dbname={QDB_PG_NAME}"
    )

    # OpenAI API Key
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

    # Grafana Configuration
    # Use internal Docker address for Grafana
    GRAFANA_API_URL = os.environ.get('GRAFANA_API_URL', 'http://grafana:3000')
    GRAFANA_API_TOKEN = os.environ.get('GRAFANA_API_TOKEN')

    # VSCode Configuration
    PASSWORD = os.environ.get("PASSWORD")
    VSCODE_API_URL = os.environ.get('VSCODE_API_URL')
    VSCODE_WS_URL = os.environ.get("VSCODE_WS_URL")

    # Other Configurations
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024 # Maximum upload size (50 MB)
    