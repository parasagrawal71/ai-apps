import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate, MessagesPlaceholder
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory

# -- Load environment variables
load_dotenv()

# -- Set API key
API_KEY = os.getenv("GROQ_API_KEY")

# -- Initialize LLM
llm = ChatGroq(groq_api_key=API_KEY, model_name="llama-3.1-8b-instant")

# -- Memory
memory = ConversationBufferMemory(memory_key="messages", return_messages=True)

# -- Prompt
prompt = ChatPromptTemplate(
    input_variables=["content", "messages"],
    messages=[
        MessagesPlaceholder(variable_name="messages"),
        HumanMessagePromptTemplate.from_template("{content}"),
    ],
)

# -- Chain
chain = LLMChain(llm=llm, prompt=prompt, memory=memory)

while True:
    content = input(">> ")

    # print(f"You entered: {content}")

    result = chain({"content": content})

    print(result["text"])
