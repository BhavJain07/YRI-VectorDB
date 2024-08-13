from scrapers.professor_scraper import ProfessorScraper
from cold_emailer import ColdEmailer
from config import OPENAI_API_KEY, GROQ_API_KEY, VECTOR_DB_PATH
from database.vector_db import VectorDB
from embedders.interest_embedder import InterestEmbedder
import pickle
import os
os.environ['TOKENIZERS_PARALLELISM'] = 'false'

def test_professor_scraper():
    scraper = ProfessorScraper()
    professors = scraper.search_professors("Stanford University", max_professors=5)
    print("ProfessorScraper test successful")
    return professors

def test_interest_embedder():
    try:
        print("Initializing InterestEmbedder...")
        embedder = InterestEmbedder()
        print("InterestEmbedder initialized successfully.")
        
        print("Embedding test interest...")
        embedding = embedder.embed("Machine Learning")
        print(f"Embedding shape: {embedding.shape}")
        print("InterestEmbedder test successful")
        return embedding
    except Exception as e:
        print(f"Error in test_interest_embedder: {str(e)}")
        import traceback
        traceback.print_exc()
        return None
    
def test_vector_db():
    vector_db = VectorDB(dimension=768)
    embedding = [0.1] * 768  # Dummy embedding
    vector_db.add(embedding, {"name": "Test Professor", "interests": ["Machine Learning"]})
    print("VectorDB test successful")

def test_cold_emailer():
    try:
        api_keys = {'openai': OPENAI_API_KEY}
        print("Initializing ColdEmailer...")
        emailer = ColdEmailer(api_keys)
        print("ColdEmailer initialized successfully.")
        
        print("Generating cold email...")
        email = emailer.generate_cold_email(
            name="John Doe",
            prof_name="Dr. Smith",
            interest="Machine Learning",
            achievements="Published a paper on NLP",
            publications=["Title: AI Advances"]
        )
        print("Cold email generated successfully.")
        print("ColdEmailer test successful")
    except Exception as e:
        print(f"Error in test_cold_emailer: {str(e)}")
        import traceback
        traceback.print_exc()

def main():
    tests = [
        ("ProfessorScraper", test_professor_scraper),
        ("InterestEmbedder", test_interest_embedder),
        ("VectorDB", test_vector_db),
        ("ColdEmailer", test_cold_emailer)
    ]

    for name, test_func in tests:
        print(f"Testing {name}...")
        try:
            test_func()
            print(f"{name} test completed successfully")
        except Exception as e:
            print(f"{name} error: {str(e)}")
            import traceback
            traceback.print_exc()
        print("--------------------")

    print("All tests completed")

if __name__ == "__main__":
    main()