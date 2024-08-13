from sentence_transformers import SentenceTransformer
import numpy as np
import os
import torch
import logging

logger = logging.getLogger(__name__)

class InterestEmbedder:
    def __init__(self, model_name='paraphrase-MiniLM-L3-v2'):
        try:
            logger.info(f"Initializing SentenceTransformer with model: {model_name}")
            self.model = SentenceTransformer(model_name)
            logger.info(f"Model {model_name} loaded successfully.")
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}", exc_info=True)
            raise

    def embed(self, interests):
        try:
            logger.info(f"Embedding interests: {interests}")
            embedding = self.model.encode([interests], show_progress_bar=True)
            logger.info(f"Embedding shape: {embedding.shape}")
            return embedding[0]  # Return the first (and only) embedding
        except Exception as e:
            logger.error(f"Error during embedding: {str(e)}", exc_info=True)
            raise

    def batch_embed(self, batch_interests):
        try:
            return self.model.encode(batch_interests, show_progress_bar=True)
        except Exception as e:
            logger.error(f"Error during batch embedding: {str(e)}", exc_info=True)
            raise

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        embedder = InterestEmbedder()
        interests = "machine learning, natural language processing"
        embedding = embedder.embed(interests)
        logger.info(f"Shape of embedding: {embedding.shape}")
    except Exception as e:
        logger.error(f"Error in main: {str(e)}", exc_info=True)