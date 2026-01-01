import os

# Base Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Pointing to your EXISTING scraped_data folder
RAW_DATA_DIR = os.path.join(BASE_DIR, "scrapers", "scraped_data")

# New location for the Vector Database
VECTOR_DB_DIR = os.path.join(BASE_DIR, "data", "vector_store")

# Model Configuration (Matches your existing embedding.py)
LLM_BASE_URL = "http://127.0.0.1:1234/v1"
LLM_API_KEY = "not-needed"
EMBEDDING_MODEL_NAME = "text-embedding-nomic-embed-text-v1.5"
CHROMA_COLLECTION_NAME = "sunbeam_data"