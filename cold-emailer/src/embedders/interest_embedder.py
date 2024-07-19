from sentence_transformers import SentenceTransformer
import numpy as np

class UserInfoEmbedder:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)

    def embed(self, user_info):
        return self.model.encode(user_info)

    def batch_embed(self, batch_user_info):
        return self.model.encode(batch_user_info)

if __name__ == "__main__":
    embedder = UserInfoEmbedder()
    user_info = ["I'm a software engineer with 5 years of experience in machine learning", "I'm a researcher in the field of natural language processing"]
    embeddings = embedder.batch_embed(user_info)
    print(f"Shape of embeddings: {embeddings.shape}")
