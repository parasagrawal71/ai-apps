import os
from dotenv import load_dotenv
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores.chroma import Chroma

# -- Load environment variables
load_dotenv()

# -- Set API key
API_KEY = os.getenv("GROQ_API_KEY")

# -- Text Splitter
text_splitter = CharacterTextSplitter(separator="\n", chunk_size=200, chunk_overlap=0)

# -- Loader
loader = TextLoader("facts.txt")
# docs = loader.load()
docs = loader.load_and_split(text_splitter=text_splitter)
# print(docs)

# for doc in docs:
# print(doc.page_content)
# print("\n")


# -- Embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
# For Example
# emb = embeddings.embed_query("The quick brown fox jumps over the lazy dog.")
# print(emb)

# -- Chroma DB
db = Chroma.from_documents(
    documents=docs,
    embedding=embeddings,
    persist_directory="emb"
)

results = db.similarity_search_with_score(
    "What is an interesting fact about the English language?", k=2
)

for result in results:
    print("\n")
    print(result[1]) # similarity score
    print(result[0].page_content)
