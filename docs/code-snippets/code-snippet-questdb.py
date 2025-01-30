import psycopg2
import requests
import os

def validate_postgres_connection():
    """Validate connection to QuestDB via PostgreSQL interface."""
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("QUESTDB_DB", "qdb"),
            user=os.getenv("QUESTDB_USER", "admin"),
            password=os.getenv("QUESTDB_PASSWORD", "quest"),
            host=os.getenv("QUESTDB_HOST", "localhost"),
            port=os.getenv("QUESTDB_PORT", "8812")
        )
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"PostgreSQL Connection Successful: {version}")
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"PostgreSQL Connection Failed: {e}")

def validate_rest_api_connection():
    """Validate connection to QuestDB via REST API."""
    try:
        questdb_rest_url = f"http://{os.getenv('QUESTDB_HOST', 'localhost')}:9000/exec?query=SELECT+NOW();"
        response = requests.get(questdb_rest_url)
        if response.status_code == 200:
            print(f"REST API Connection Successful: {response.json()}")
        else:
            print(f"REST API Connection Failed: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"REST API Connection Failed: {e}")

if __name__ == "__main__":
    print("Validating QuestDB Connections...")
    validate_postgres_connection()
    validate_rest_api_connection()