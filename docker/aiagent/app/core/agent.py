import os
from typing import Optional
from langsmith import traceable
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from aiagent.app.interface import AgentInterface, MemoryInterface
from aiagent.config import Config
from aiagent.app.core.memory import WindowMemoryManager

class MainAgent(AgentInterface):
    def __init__(
        self,
        tools: list,
        memory: Optional[MemoryInterface] = None,
        model_name: str = "gpt-4o-mini",
        window_size: int = 10
    ):
        """
        :param tools: List of LangChain tools (e.g., [QueryQuestDBTool()])
        :param memory: A MemoryInterface implementation for conversation.
        :param model_name: Name of the LLM.
        :param window_size: If no memory object is passed, we create a default WindowMemoryManager with this size.
        """

        # Initialize or default to ephemeral window memory
        self.memory = memory or WindowMemoryManager(window_size)

        # Initialize the underlying LLM
        openai_api_key = Config.OPENAI_API_KEY
        if not openai_api_key:
            raise ValueError("OPEN_API_KET is not set.")

        self.llm = ChatOpenAI(
            openai_api_key=openai_api_key,
            model=model_name)

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

        # Create the ReAct agent
        self.agent = create_react_agent(
            self.llm,
            tools,
            state_modifier=system_prompt
        )

    @traceable
    def invoke(self, session_id: str, user_message: str) -> str:
        """
        Process user input with conversation context from memory.
        :param session_id: Unique identifier for the conversation/session.
        :param user_message: The latest user query.
        :return: The final agent response.
        """

        # Load existing conversation from memory
        conversation_history = self.memory.load_conversation(session_id)

        # Convert conversation history into langgraph's input format
        # Typically: [("human", "message1"), ("assistant", "message2"), ...]
        past_messages = []
        for msg in conversation_history:
            role = "human" if msg["role"] == "user" else "assistant"
            past_messages.append((role, msg["content"]))

        # Add the new user message to the "human" messages
        past_messages.append(("human", user_message))

        # Save user message to memory (so it's available for the next turn)
        self.memory.save_user_message(session_id, user_message)

        # Invoke the chain
        response = self.agent.invoke({"messages": past_messages})

        # Extract final text from the agent response
        final_text = response["messages"][-1].content

        # Save agent response into memory
        self.memory.save_agent_message(session_id, final_text)

        return final_text
