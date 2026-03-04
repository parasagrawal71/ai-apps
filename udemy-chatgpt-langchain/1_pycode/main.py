import os
from dotenv import load_dotenv
import argparse
from pprintpp import pprint
# from langchain_openai import OpenAI
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain

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

# -- Initialize LLM
# llm = OpenAI(api_key=API_KEY)
llm = ChatGroq(
    groq_api_key=API_KEY,
    model_name="llama-3.1-8b-instant"
)

# -- Templates
code_prompt = PromptTemplate(
    template="write a very short {language} function that will {task}",
    input_variables=["language", "task"],
)
testcase_prompt = PromptTemplate(
    template="write a test case for the following {language} code:\n {code}",
    input_variables=["language", "code"],
)

# -- Chains
code_chain = LLMChain(llm=llm, prompt=code_prompt, output_key="code")
testcase_chain = LLMChain(llm=llm, prompt=testcase_prompt, output_key="testcase")

# --
chain = SequentialChain(
    chains=[code_chain, testcase_chain],
    input_variables=["language", "task"],
    output_variables=["code", "testcase"],
)

result = chain({"language": args.language, "task": args.task})
pprint(result)
# print(result["text"]) # text is 'code' now
# pprint(result["code"])
# pprint(result["testcase"])
