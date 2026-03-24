import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# -- Load environment variables
load_dotenv()

# -- Set API key
API_KEY = os.getenv("GROQ_API_KEY")

def build_llm(chat_args):
    return ChatGroq(
        groq_api_key=API_KEY,
        model_name="llama-3.1-8b-instant",
    )
