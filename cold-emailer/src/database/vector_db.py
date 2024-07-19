import faiss
import numpy as np
import pickle

class VectorDB:
    def __init__(self, dimension):
        self.index = faiss.IndexFlatL2(dimension)
        self.professors = []

    def add(self, embedding, professor_info):
        self.index.add(np.array([embedding]))
        self.professors.append(professor_info)

    def search(self, query_embedding, k=5):
        distances, indices = self.index.search(np.array([query_embedding]), k)
        return [self.professors[i] for i in indices[0]]

    def save(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump((self.index, self.professors), f)

    @classmethod
    def load(cls, filename):
        with open(filename, 'rb') as f:
            index, professors = pickle.load(f)
        db = cls(index.d)
        db.index = index
        db.professors = professors
        return db

if __name__ == "__main__":
    # Create a dummy vector database
    db = VectorDB(dimension=768)  # Assuming 768-dimensional embeddings
    db.add(np.random.rand(768), {
        'name': 'Dr. John Doe',
        'email': 'john.doe@example.com',
        'interests': ['Machine Learning', 'Artificial Intelligence']
    })
    db.add(np.random.rand(768), {
        'name': 'Dr. Jane Smith',
        'email': 'jane.smith@example.com',
        'interests': ['Natural Language Processing', 'Computer Vision']
    })
    db.save("../../data/vector_db")