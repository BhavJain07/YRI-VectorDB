from scrapers.professor_scraper import ProfessorScraper
from cold_emailer import ColdEmailer
from config import OPENAI_API_KEY, GROQ_API_KEY, VECTOR_DB_PATH
from database.vector_db import VectorDB
from embedders.interest_embedder import InterestEmbedder

def main():
    api_keys = {
        'openai': OPENAI_API_KEY,
        'groq': GROQ_API_KEY
    }

    if not api_keys['openai'] or not api_keys['groq']:
        print("Error: OpenAI or Groq API key is missing. Please check your .env file.")
        return

    scraper = ProfessorScraper()
    emailer = ColdEmailer(api_keys)
    interest_embedder = InterestEmbedder()

    # Load or create VectorDB
    try:
        vector_db = VectorDB.load(VECTOR_DB_PATH)
    except FileNotFoundError:
        vector_db = VectorDB(dimension=768)  # Dimension of the InterestEmbedder output

    # Scrape professors and add to VectorDB if it's empty
    if not vector_db.professors:
        universities = ["Stanford University", "MIT", "Harvard University"]  # Add more as needed
        for university in universities:
            professors = scraper.search_professors(university)
            for professor in professors:
                embedding = interest_embedder.embed(" ".join(professor['interests']))
                vector_db.add(embedding, professor)
        vector_db.save(VECTOR_DB_PATH)

    # Get user input
    name = input("Enter your full name: ")
    interests = input("Enter your research interests: ")
    achievements = input("Enter your achievements: ")

    # Find similar professors
    interest_embedding = interest_embedder.embed(interests)
    similar_professors = vector_db.search(interest_embedding, k=5)
    print(f"Suggested professors: {[prof['name'] for prof in similar_professors]}")

    # Generate cold email for the top match
    cold_email = emailer.generate_cold_email(
        name=name,
        prof_name=similar_professors[0]['name'],
        interest=interests,
        achievements=achievements,
        publications=scraper.get_publications(similar_professors[0]['name'])[:5]
    )

    print("\nGenerated Cold Email:")
    print(cold_email)

if __name__ == "__main__":
    main()