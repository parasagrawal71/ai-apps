import os
from dotenv import load_dotenv
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores.chroma import Chroma
from langchain.chains import RetrievalQA
from langchain_groq import ChatGroq
from redundant_filter_retriever import RedundantFilterRetriever
import langchain

langchain.debug = True

# -- Load environment variables
load_dotenv()

# -- Set API key
API_KEY = os.getenv("GROQ_API_KEY")

# -- Initialize LLM
llm = ChatGroq(groq_api_key=API_KEY, model_name="llama-3.1-8b-instant")

# -- Embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# -- Chroma DB: No setup or no re-create embeddings
db = Chroma(
    persist_directory="emb",
    embedding_function=embeddings,
)

# results = db.similarity_search_with_score(
#     "What is an interesting fact about the English language?", k=2
# )

# for result in results:
#     print("\n")
#     print(result[1]) # similarity score
#     print(result[0].page_content)

# -- RetrievalQA
# retriever = db.as_retriever()
retriever = RedundantFilterRetriever(embeddings=embeddings, chroma=db)
chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)

result = chain.run("What is an interesting fact about the English language?")
print(result)
