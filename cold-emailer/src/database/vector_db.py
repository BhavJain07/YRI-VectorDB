import faiss
import numpy as np
import pickle

class VectorDB:
    def __init__(self, dimension):
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)
        self.professors = []

    def add(self, embedding, professor_info):
        if len(embedding) != self.dimension:
            raise ValueError(f"Embedding dimension mismatch. Expected {self.dimension}, got {len(embedding)}")
        self.index.add(np.array([embedding], dtype=np.float32))
        self.professors.append(professor_info)

    def search(self, query_embedding, k=5):
        if len(query_embedding) != self.dimension:
            raise ValueError(f"Query embedding dimension mismatch. Expected {self.dimension}, got {len(query_embedding)}")
        distances, indices = self.index.search(np.array([query_embedding], dtype=np.float32), k)
        return [self.professors[i] for i in indices[0]]

    def save(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump((self.index, self.professors, self.dimension), f)

    @classmethod
    def load(cls, filename):
        with open(filename, 'rb') as f:
            index, professors, dimension = pickle.load(f)
        db = cls(dimension)
        db.index = index
        db.professors = professors
        return db

if __name__ == "__main__":
    # Create a dummy vector database
    db = VectorDB(dimension=768)  # Assuming 768-dimensional embeddings
    db.add(np.random.rand(768).astype(np.float32), {
        'name': 'Dr. John Doe',
        'email': 'john.doe@example.com',
        'interests': ['Machine Learning', 'Artificial Intelligence']
    })
    db.add(np.random.rand(768).astype(np.float32), {
        'name': 'Dr. Jane Smith',
        'email': 'jane.smith@example.com',
        'interests': ['Natural Language Processing', 'Computer Vision']
    })
    db.save("../../data/vector_db")