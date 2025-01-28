import os
from langsmith import traceable
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from aiagent.app.interface import AgentInterface
from aiagent.config import Config

class MainAgent(AgentInterface):
    def __init__(self, tools: list):
        # Initialize the underlying LLM
        openai_api_key = Config.OPENAI_API_KEY
        if not openai_api_key:
            raise ValueError("OPEN_API_KET is not set.")

        self.llm = ChatOpenAI(openai_api_key=openai_api_key, model="gpt-4o-mini")

        # Create a custom system prompt or template
        # Database schema details
        table_schema = """
        The database schema is as follows:
        Table: binance_trades
        Columns:
        - symbol (string): Trading pair symbol (e.g., "BTCUSDT").
        - trade_id (numeric): Unique identifier for the trade.
        - price (numeric): Trade price.
        - quantity (numeric): Trade quantity.
        - buyer_order_id (nullable numeric): Order ID of the buyer.
        - seller_order_id (nullable numeric): Order ID of the seller.
        - is_buyer_market_maker (boolean): Indicates if the buyer is a market maker.
        - timestamp (ISO 8601 datetime): The trade timestamp.
        """
        system_prompt = f"""
        You are an AI assistant with access to a QuestDB database. The database schema is as follows:
        {table_schema}

        Respond to user queries by generating appropriate SQL queries. Do NOT provide explanations or extra text.
        """

        # Define tools for the agent
        self._tools = tools

        # Create the agent with tools
        self.agent = create_react_agent(
            self.llm,
            self._tools,
            state_modifier=system_prompt
        )

    @traceable
    def invoke(self, user_message: str) -> str:
        """
        Process user input and return the response.
        """

        # Invoke response
        response = self.agent.invoke({"messages": [("human", user_message)]})

       # Extract final text
        return response["messages"][-1].content
