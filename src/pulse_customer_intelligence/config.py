from dotenv import load_dotenv
from agent_framework.openai import OpenAIChatClient

load_dotenv()

def get_chat_client() -> OpenAIChatClient:
    # Reads OPENAI_API_KEY from your .env automatically.
    return OpenAIChatClient(model="gpt-4o")