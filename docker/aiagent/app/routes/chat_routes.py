from flask import Blueprint, request, jsonify
from aiagent.app.core.agent import MainAgent
from aiagent.app.core.tool import QueryQuestDBTool

# Initialize Blueprint
chat_bp = Blueprint("chat_bp", __name__)

# Create an instance of your new agent
tools = [QueryQuestDBTool()]
agent = MainAgent(tools=tools)

@chat_bp.route('', methods=['POST'])
def chat():
    """
    Chat endpoint for handling user queries.
    """

    # Process user input
    data = request.get_json()
    user_message = data.get('message', '').strip()

    # Input validation
    if not user_message:
        return jsonify({"error": "Message cannot be empty"}), 400
    try:
        agent_response = agent.invoke(user_message)
        return jsonify({"response": agent_response}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
