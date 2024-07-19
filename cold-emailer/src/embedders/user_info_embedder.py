from sentence_transformers import SentenceTransformer
import numpy as np

class UserInfoEmbedder:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)

    def embed(self, user_info):
        text = f"{user_info['name']} {user_info['education']} {user_info['interests']} {user_info['reason_for_contact']}"
        return self.model.encode(text)

if __name__ == "__main__":
    embedder = UserInfoEmbedder()
    user_info = {
        "name": "John Doe",
        "education": "Bachelor's in Computer Science",
        "interests": "machine learning, natural language processing",
        "reason_for_contact": "Interested in pursuing a PhD"
    }
    embedding = embedder.embed(user_info)
    print(f"Shape of embedding: {embedding.shape}")