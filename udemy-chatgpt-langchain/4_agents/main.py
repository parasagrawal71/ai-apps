import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain.agents import initialize_agent, AgentExecutor, AgentType
from langchain.schema import SystemMessage
from langchain.memory import ConversationBufferMemory

from tools.sql import run_query_tool, list_tables, describe_tables_tool
from tools.report import write_report_tool
from handlers.chat_model_start_handler import ChatModelStartHandler

# -- Load environment variables
load_dotenv()

# -- Set API key
API_KEY = os.getenv("GROQ_API_KEY")

# -- Initialize handlers
handler = ChatModelStartHandler()

# -- Initialize LLM
llm = ChatGroq(
    groq_api_key=API_KEY, model_name="llama-3.1-8b-instant", callbacks=[handler]
)


"""
Example,
- A user wants to know "How many open orders are there?" 
- My App sends this query to ChatGPT along with available tools. (One of the tools is to execute a query on the database)
- ChatGPT decides to use this tool and wants my app to execute a query.
- My app responds to ChatGPT with the result, i.e., 94 after query execution.
- ChatGPT responds to the user with an answer: “There are 94 open orders.”
"""

# -- Prompt
tables = list_tables()
prompt = ChatPromptTemplate(
    messages=[
        SystemMessage(
            content=(
                "You are an AI that has an access to a sqlite database.\n",
                f"The available tables in the database are: {tables}\n",
                "Do not make any assumptions about what tables exist or what columns exist. Instead, use the describe_tables function.\n",
            )
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template("{input}"),
        MessagesPlaceholder(
            variable_name="agent_scratchpad"
        ),  # IMPORTANT: must be named "agent_scratchpad". -> AIMessageForFunction + FunctionResultMessage (Not sure whether they are exactly named like this)
    ],
)

memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True,
)

# -- Agent (returns AgentExecutor internally)
"""
Agent: A chain that knows how to use tools. Will take that list of tools and convert
them into JSON function descriptions. Still has input variables, memory, prompts, 
etc - all the normal things a chain has.

AgentExecutor: Takes an agent and runs it until the response is not a function 
call. Essentially a fancy while loop.
"""
tools = [run_query_tool, describe_tables_tool] # Comment out write_report_tool
agent_executor = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    # agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION, # To use StructuredTool
    # verbose=True,
    memory=memory,
)

agent_executor.run("How many users are there in the database?")

# With Groq, it still tries to execute the query with shipping_address table
# agent_executor.run("How many users have provided a shipping address?") # sqlite3.OperationalError: no such column: shipping_address

# With STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION, write_report tool is not working well.
# agent_executor.run("Summarize the top 5 most popular products. Write the results to a report file.")


# agent_executor.run("How many orders are there?")
# agent_executor.run("Repeat the exact same process for the users.")
