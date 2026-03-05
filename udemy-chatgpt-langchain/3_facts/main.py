import os
from dotenv import load_dotenv


# -- Load environment variables
load_dotenv()

# -- Set API key
API_KEY = os.getenv("GROQ_API_KEY")
