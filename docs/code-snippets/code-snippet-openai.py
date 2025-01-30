import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# Load environment variables from docker/.env
env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../docker/.env"))
load_dotenv(dotenv_path=env_path)

# Fetch OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError(f"OPENAI_API_KEY is not set. Please configure the API key.")

def validate_openai_connection():
    """Test OpenAI API by generating a simple response using LangChain's ChatOpenAI."""
    try:
        llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model="gpt-4o-mini")
        response = llm.invoke("Say hello!")

        print("OpenAI API Connection Successful!")
        print("Response:", response)
    except Exception as e:
        print(f"OpenAI API Connection Failed: {e}")

if __name__ == "__main__":
    print("Validating OpenAI API Connection...")
    validate_openai_connection()