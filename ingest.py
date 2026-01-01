from src.core.vector_db import SunbeamKnowledgeBase

if __name__ == "__main__":
    print("Starting Data Ingestion...")
    kb = SunbeamKnowledgeBase()
    kb.ingest_data()