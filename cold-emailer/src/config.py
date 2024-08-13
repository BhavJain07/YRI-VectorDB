import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = "sqlite:///cold_emailer.db"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT"))
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
SCRAPING_DELAY = 2
MAX_PROFESSORS_PER_UNIVERSITY = 100
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
EMAIL_GENERATION_MODEL = "gpt-3.5-turbo-0613"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
VECTOR_DB_PATH = "../data/vector_db"

# Get the absolute path of the project root directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VECTOR_DB_PATH = os.path.join(PROJECT_ROOT, "data", "vector_db")

# Ensure the data directory exists
os.makedirs(os.path.dirname(VECTOR_DB_PATH), exist_ok=True)
