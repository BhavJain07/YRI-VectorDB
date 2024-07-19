import json
from embedders.interest_embedder import InterestEmbedder
from embedders.user_info_embedder import UserInfoEmbedder
from knowledge_graph.graph_querier import KnowledgeGraphQuerier
from database.vector_db import VectorDB
from models.fine_tuned_email_generator import FineTunedEmailGenerator
from questionnaire.user_info_extractor import UserInfoExtractor

def main():
    # Load knowledge graph
    graph_querier = KnowledgeGraphQuerier("../../data/knowledge_graph.gexf")

    # Load vector database
    vector_db = VectorDB.load("../../data/vector_db")

    # Initialize embedders
    interest_embedder = InterestEmbedder()
    user_info_embedder = UserInfoEmbedder()

    # Initialize email generator
    email_generator = FineTunedEmailGenerator()

    # Extract user information
    user_info_extractor = UserInfoExtractor()
    user_info = user_info_extractor.extract_user_info()

    # Embed user information
    user_embedding = user_info_embedder.embed(user_info)

    # Search for similar professors
    similar_professors = vector_db.search(user_embedding, k=5)

    # Generate emails for similar professors
    emails = []
    for professor_info in similar_professors:
        email = email_generator.generate_email(professor_info, user_info)
        emails.append((professor_info['name'], email))

    # Print generated emails
    print("Generated Emails:")
    for professor_name, email in emails:
        print(f"Professor: {professor_name}\nEmail:\n{email}\n")

if __name__ == "__main__":
    main()
