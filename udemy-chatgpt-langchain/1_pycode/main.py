from langchain_openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")

llm = OpenAI(api_key=API_KEY)

result = llm("write a very very short poem")
print(result)
