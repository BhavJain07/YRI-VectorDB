import json
from embedders.interest_embedder import InterestEmbedder
from embedders.user_info_embedder import UserInfoEmbedder
from knowledge_graph.graph_querier import KnowledgeGraphQuerier
from models.fine_tuned_email_generator import FineTunedEmailGenerator
from questionnaire.user_info_extractor import UserInfoExtractor
from database.vector_db import VectorDB

def load_professors(university_name):
    with open(f"../data/professors/{university_name}.json", "r") as f:
        return json.load(f)

def main():
    # Initialize components
    interest_embedder = InterestEmbedder()
    user_info_embedder = UserInfoEmbedder()
    graph_querier = KnowledgeGraphQuerier("../data/knowledge_graph.gexf")
    email_generator = FineTunedEmailGenerator()
    user_info_extractor = UserInfoExtractor()
    vector_db = VectorDB.load("../data/professor_db")

    # Get user information
    user_info = user_info_extractor.extract_user_info()

    # Embed user interests
    user_embedding = user_info_embedder.embed(user_info)

    # Find similar professors
    similar_professors = vector_db.search(user_embedding, k=5)

    # Generate emails for each similar professor
    for professor in similar_professors:
        professor_info = graph_querier.get_professor_info(professor['name'])
        email = email_generator.generate_email(professor_info, user_info)
        print(f"\nGenerated email for {professor['name']}:")
        print(email)
        print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    main()
