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