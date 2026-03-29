# File: src/vector_db.py
import numpy as np
from sentence_transformers import SentenceTransformer

class RestaurantVectorDB:
    def __init__(self, model_name):
        self.model = SentenceTransformer(model_name)
        self.embeddings = None
        self.metadata = []
    
    def build_from_dataframe(self, df):
        """Create vector database from DataFrame"""
        texts = df['search_text'].tolist()
        self.metadata = df.to_dict('records')
        self.embeddings = self.model.encode(texts)
        
    def search(self, query, top_k=3):
        """Semantic search implementation"""
        query_embed = self.model.encode(query)
        scores = np.dot(self.embeddings, query_embed)
        top_indices = np.argsort(scores)[-top_k:][::-1]
        return [self.metadata[i] for i in top_indices]
