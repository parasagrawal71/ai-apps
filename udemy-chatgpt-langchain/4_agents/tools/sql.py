import sqlite3
import ast
from pydantic.v1 import BaseModel
from typing import List
from langchain.tools import Tool

conn = sqlite3.connect("db.sqlite")

# Define a function to run a sqlite query
def run_sqlite_query(query):
    c = conn.cursor()
    try:
        c.execute(query)
        return c.fetchall()
    except sqlite3.OperationalError as err:
        return f"The following error occurred: {str(err)}"

class RunQueryArgsSchema(BaseModel):
    query: str

run_query_tool = Tool(
    name="run_query",
    description="Run a sqlite query.",
    func=run_sqlite_query,
    args_schema=RunQueryArgsSchema,
)


# list all tables in the database
def list_tables():
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    rows = c.fetchall()
    return "\n".join(row[0] for row in rows if row[0] is not None)


# Define a function to describe the tables
def describe_tables(table_names):
    if isinstance(table_names, str):
        table_names = ast.literal_eval(table_names)
    elif isinstance(table_names, dict):
        table_names = table_names.get("table_names", [])

    c = conn.cursor()
    tables = ", ".join("'" + table_name + "'" for table_name in table_names)
    rows = c.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name IN ({tables});")
    return "\n".join(row[0] for row in rows if row[0] is not None)

class DescribeTablesArgsSchema(BaseModel):
    table_names: List[str]

describe_tables_tool = Tool(
    name="describe_tables",
    description="Given a list of table names, returns the schema of those tables.",
    func=describe_tables,
    args_schema=DescribeTablesArgsSchema,
)
