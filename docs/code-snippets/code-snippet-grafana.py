import os
import requests
from dotenv import load_dotenv
import os.path

# Load environment variables from docker/.env
env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../docker/.env"))
load_dotenv(dotenv_path=env_path)

# Fetch Grafana configuration from environment variables
GRAFANA_API_URL = os.getenv("GRAFANA_API_URL", "http://192.168.1.15:3000")
GRAFANA_API_TOKEN = os.getenv("GRAFANA_API_TOKEN")

if not GRAFANA_API_TOKEN:
    raise ValueError("GRAFANA_API_TOKEN is not set. Please configure the API token.")

def validate_grafana_connection():
    """
    Validates the Grafana API connection by fetching a dashboard using its UID.
    This snippet uses a known dashboard UID. Adjust the 'uid' as needed.
    """
    uid = "MNhO0-aKk"
    url = f"{GRAFANA_API_URL}/api/dashboards/uid/{uid}"
    headers = {
        "Authorization": f"Bearer {GRAFANA_API_TOKEN}",
        "X-Grafana-Org-Id": "1"
    }
    
    try:
        # For local Docker networks with plain HTTP, certificate verification is not needed.
        # In production with HTTPS, set verify=True or provide a CA bundle.
        response = requests.get(url, headers=headers, verify=False)
        print("Status:", response.status_code)
        try:
            print("JSON:", response.json())
        except Exception as e:
            print("Failed to decode JSON:", e)
            print("Response text:", response.text)
    except Exception as e:
        print("Error while connecting to Grafana:", e)

if __name__ == "__main__":
    print("Validating Grafana API Connection...")
    validate_grafana_connection()