# Database configuration
DATABASE_URL = "sqlite:///cold_emailer.db"

# OpenAI API configuration
OPENAI_API_KEY = "your-api-key-here"

# Email configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "your-email@gmail.com"
SENDER_PASSWORD = "your-app-password-here"

# Scraping configuration
SCRAPING_DELAY = 2  # seconds between requests
MAX_PROFESSORS_PER_UNIVERSITY = 100

# Model configuration
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
EMAIL_GENERATION_MODEL = "gpt-3.5-turbo-0613"