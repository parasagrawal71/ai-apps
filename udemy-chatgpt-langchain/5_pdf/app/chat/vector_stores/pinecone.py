import os
import pinecone
from dotenv import load_dotenv
from langchain.vectorstores.pinecone import Pinecone # Hosted (https://pinecone.io/)
from app.chat.embeddings.groqai import embeddings

# -- Load environment variables
load_dotenv()


pinecone.Pinecone(
    api_key=os.getenv("PINECONE_API_KEY"),
    environment=os.getenv("PINECONE_ENV_NAME"),
)

vector_store = Pinecone.from_existing_index(
    index_name=os.getenv("PINECONE_INDEX_NAME"),
    embedding=embeddings,
)
