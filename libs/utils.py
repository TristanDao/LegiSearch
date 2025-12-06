# -*- coding: utf-8 -*-
"""
Utility functions for RAG system
"""
import os
from pathlib import Path
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Model configuration
EMBEDDING_MODEL_NAME = "keepitreal/vietnamese-sbert"
MODELS_DIR = Path(__file__).parent.parent / "models"
MODELS_DIR.mkdir(exist_ok=True)

# Global variable to store the model
_embedding_model = None


def get_embedding_model():
    """
    Load embedding model and save to models/ folder if not exists.
    Returns the SentenceTransformer model.
    """
    global _embedding_model
    
    if _embedding_model is None:
        model_path = MODELS_DIR / EMBEDDING_MODEL_NAME.replace("/", "_")
        
        # Check if model exists locally
        if model_path.exists() and any(model_path.iterdir()):
            print(f"Loading embedding model from local: {model_path}")
            _embedding_model = SentenceTransformer(str(model_path))
        else:
            print(f"Downloading embedding model: {EMBEDDING_MODEL_NAME}")
            _embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)
            # Save model to models/ folder
            print(f"Saving model to: {model_path}")
            _embedding_model.save(str(model_path))
            print("Model saved successfully!")
    
    return _embedding_model


def get_embedding(text):
    """
    Generate embedding for text using the Vietnamese SBERT model.
    
    Args:
        text: Input text to embed
        
    Returns:
        List of floats representing the embedding vector
    """
    if not text or not text.strip():
        print("Warning: Attempted to get embedding for empty text.")
        return None
    
    model = get_embedding_model()
    embedding = model.encode(text, normalize_embeddings=True)
    return embedding.tolist()


def get_mongodb_connection():
    """
    Get MongoDB connection from environment variables.
    
    Returns:
        pymongo.MongoClient: MongoDB client
    """
    import pymongo
    
    mongo_url = os.getenv("MONGODB_URL")
    if not mongo_url:
        raise ValueError(
            "MONGODB_URL not found in environment variables. "
            "Please set it in your .env file."
        )
    
    return pymongo.MongoClient(mongo_url)


def get_mongodb_collection(db_name=None, collection_name=None):
    """
    Get MongoDB collection for vector search.
    
    Args:
        db_name: Database name (default from env: MONGODB_DB_NAME)
        collection_name: Collection name (default from env: MONGODB_COLLECTION_NAME)
        
    Returns:
        pymongo.collection.Collection: MongoDB collection
    """
    client = get_mongodb_connection()
    
    db_name = db_name or os.getenv("MONGODB_DB_NAME", "VNLawsDB")
    collection_name = collection_name or os.getenv("MONGODB_COLLECTION_NAME", "VNLawsCollection")
    
    db = client[db_name]
    collection = db[collection_name]
    
    return collection

