from flask import Blueprint, jsonify
import psycopg2 as pg
from aiagent.config import Config

# Initialize Blueprint
health_bp = Blueprint("health_bp", __name__)

@health_bp.route('', methods=['GET'])
def health():
    """
    Health check endpoint to verify the service and database connectivity.
    """
    try:
        # Test QuestDB connection
        with pg.connect(Config.QDB_CONN_STR) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
    except Exception as e:
        return jsonify({"status": "unhealthy", "error": str(e)}), 500

    return jsonify({"status": "healthy"}), 200
