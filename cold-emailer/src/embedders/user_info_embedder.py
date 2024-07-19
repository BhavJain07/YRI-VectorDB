from sentence_transformers import SentenceTransformer
import numpy as np

class UserInfoEmbedder:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)

    def embed(self, user_info):
        # Combine user info into a single string
        combined_info = " ".join([f"{k}: {v}" for k, v in user_info.items()])
        return self.model.encode(combined_info)

if __name__ == "__main__":
    embedder = UserInfoEmbedder()
    user_info = {
        "name": "John Doe",
        "interests": "Machine Learning, Natural Language Processing",
        "education": "BS in Computer Science",
        "location": "New York, USA"
    }
    embedding = embedder.embed(user_info)
    print(f"Shape of embedding: {embedding.shape}")
