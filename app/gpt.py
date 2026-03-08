import os
from openai import OpenAI
from dotenv import load_dotenv


def init_ai_client():
    load_dotenv()
    openaiApiKey = os.getenv("OPENAI_API_KEY")
    return OpenAI(api_key=openaiApiKey)
