import os
import glob
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from src.core.llm import get_embedding_model
from src.config import VECTOR_DB_DIR, RAW_DATA_DIR, CHROMA_COLLECTION_NAME

class SunbeamKnowledgeBase:
    def __init__(self):
        self.embedding_model = get_embedding_model()
        self.vector_store = Chroma(
            persist_directory=VECTOR_DB_DIR,
            embedding_function=self.embedding_model,
            collection_name=CHROMA_COLLECTION_NAME
        )

    def get_retriever(self, k=4):
        return self.vector_store.as_retriever(search_kwargs={"k": k})

    def ingest_data(self):
        """Reads .txt files and indexes them. Uses a 'safety split' only for files that exceed model limits."""
        print(f"📂 Scanning for data in: {RAW_DATA_DIR}")
        
        # 1. SETUP SAFETY SPLITTER
        # 4096 tokens is roughly 12,000 - 16,000 characters. 
        # We set chunk_size to 10,000 chars to be safe and leave room for the prefix.
        text_splitter = RecursiveCharacterTextSplitter(
            separators=["\n\n", "\n", " ", ""],
            chunk_size=1500, 
            chunk_overlap=700,
            length_function=len,
            is_separator_regex=False
        )

        docs = []
        files = glob.glob(os.path.join(RAW_DATA_DIR, "*.txt"))

        for file_path in files:
            filename = os.path.basename(file_path)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    text = f.read()
                
                if not text.strip():
                    continue

                # 2. CHECK IF SPLIT IS NEEDED
                # If the file is small (<10k chars), this returns a list with just 1 item (the whole file).
                # If the file is huge (>10k chars), it splits it so it fits in the DB.
                chunks = text_splitter.split_text(text)
                
                for i, chunk in enumerate(chunks):
                    # Adding Nomic specific prefix
                    prefixed_text = f"search_document: {chunk}"
                    
                    # If the file wasn't split, chunk_index is 0. 
                    # If it WAS split, this metadata helps you know part 1 vs part 2.
                    docs.append(Document(
                        page_content=prefixed_text, 
                        metadata={
                            "source": filename, 
                            "chunk_index": i, 
                            "total_chunks": len(chunks),
                            "original_content": chunk
                        }
                    ))
                
                status = "kept whole" if len(chunks) == 1 else f"split into {len(chunks)} parts"
                print(f"✅ Processed: {filename} ({status})")
                
            except Exception as e:
                print(f"❌ Error reading {filename}: {e}")
        
        if docs:
            print(f"⚙️  Embedding {len(docs)} documents into ChromaDB...")
            # Using large batches can sometimes timeout, consider smaller batches if this hangs
            self.vector_store.add_documents(docs)
            print("🎉 Ingestion Complete. Database Ready.")
        else:
            print("⚠️  No data found to ingest.")