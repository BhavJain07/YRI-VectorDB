import json
from embedders.interest_embedder import InterestEmbedder
from embedders.user_info_embedder import UserInfoEmbedder
from knowledge_graph.graph_querier import KnowledgeGraphQuerier
from models.fine_tuned_email_generator import FineTunedEmailGenerator
from questionnaire.user_info_extractor import UserInfoExtractor
from database import Session, University, Professor
from email_sender import send_email
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
    session = Session()

    # Load vector database
    vector_db = VectorDB.load("../data/vector_db")

    # Get user information
    user_info = user_info_extractor.extract_user_info()

    # Embed user information
    user_embedding = user_info_embedder.embed(user_info)

    # Search for similar professors
    similar_professors = vector_db.search(user_embedding, k=5)

    # Generate and send emails
    for professor_info in similar_professors:
        email_body = email_generator.generate_email(professor_info, user_info)
        send_email(professor_info['email'], "Research Inquiry", email_body)

    session.close()

if __name__ == "__main__":
    main()