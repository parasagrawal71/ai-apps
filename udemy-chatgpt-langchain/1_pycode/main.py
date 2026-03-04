import os
from dotenv import load_dotenv
import argparse
# from langchain_openai import OpenAI
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# -- Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("--task", default="add two numbers")
parser.add_argument("--language", default="python")
args = parser.parse_args()

# -- Load environment variables
load_dotenv()

# -- Set API key
# API_KEY = os.getenv("OPENAI_API_KEY")
API_KEY = os.getenv("GROQ_API_KEY")

# llm = OpenAI(api_key=API_KEY)
llm = ChatGroq(
    groq_api_key=API_KEY,
    model_name="llama-3.1-8b-instant"
)

code_prompt = PromptTemplate(
    template="write a very short {language} function that will {task}",
    input_variables=["language", "task"],
)

code_chain = LLMChain(llm=llm, prompt=code_prompt)

result = code_chain({"language": args.language, "task": args.task})
# print(result)
print(result["text"])
