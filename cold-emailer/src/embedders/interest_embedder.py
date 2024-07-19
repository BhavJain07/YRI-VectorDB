from sentence_transformers import SentenceTransformer
import numpy as np

class InterestEmbedder:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)

    def embed(self, interests):
        return self.model.encode(interests)

    def batch_embed(self, batch_interests):
        return self.model.encode(batch_interests)

if __name__ == "__main__":
    embedder = InterestEmbedder()
    interests = ["machine learning", "natural language processing"]
    embeddings = embedder.batch_embed(interests)
    print(f"Shape of embeddings: {embeddings.shape}")